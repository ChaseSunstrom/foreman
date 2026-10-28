"""fm scene shade (T-1846): a GLSL ES 3.00 fragment-shader subset, compiled to Python and run per pixel on the CPU.

A shader card previews offline: no browser, no GPU. What's outside the subset is refused naming its line.
Values: scalars are Python numbers, vectors tuples, matrices flat column-major tuples. User names are
mangled (l_ u_ g_ a_ f_) and literals re-emitted, so no shader text reaches the Python source as written.
"""
import math
import operator
import re

M = 0xFFFFFFFF
LIMIT = 100000  # loop turns and calls in one pixel before the render stops: a GPU would hang there too
TOTAL = 100_000_000  # and in the whole render: the busiest card fits at 512x512 (20 s); a runaway stops inside a minute
DERIVS = 64  # dFdx/dFdy/fwidth calls in one pixel
TOKEN = re.compile(r"""(?P<skip>[ \t\r\n]+|//[^\n]*|/\*.*?\*/)
 |(?P<num>0[xX][0-9a-fA-F]+[uU]?|(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?[fF]?|\d+[eE][+-]?\d+[fF]?|\d+[uU]?)
 |(?P<id>[A-Za-z_]\w*)
 |(?P<pp>\#[^\n]*)
 |(?P<op><<=|>>=|\+\+|--|[-+*/%&|^]=|==|!=|<=|>=|&&|\|\||\^\^|<<|>>|[-+*/%&|^!~<>=?:(){}\[\],;.])""",
                   re.S | re.X | re.ASCII)
PREC = {"||": 1, "^^": 2, "&&": 3, "|": 4, "^": 5, "&": 6, "==": 7, "!=": 7, "<": 8, ">": 8, "<=": 8, ">=": 8,
        "<<": 9, ">>": 9, "+": 10, "-": 10, "*": 11, "/": 11, "%": 11}
OPN = {"+": "add", "-": "sub", "*": "mul", "/": "div", "%": "mod", "&": "and", "|": "or", "^": "xor",
       "<<": "shl", ">>": "shr"}
ASSIGN = ("=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=")
PRECISION = ("highp", "mediump", "lowp")
TYPES = {"void": ("void", 0), "float": ("float", 1), "int": ("int", 1), "uint": ("uint", 1), "bool": ("bool", 1)}
for _n in (2, 3, 4):
    TYPES.update({f"vec{_n}": ("float", _n), f"ivec{_n}": ("int", _n), f"uvec{_n}": ("uint", _n),
                  f"bvec{_n}": ("bool", _n), f"mat{_n}": ("float", _n * _n)})
SHADERTOY = {"iResolution": "vec3", "iTime": "float", "iFrame": "int", "iMouse": "vec4"}  # declared on first use
NOT_HERE = ("texture", "texture2D", "textureLod", "texelFetch", "transpose", "inverse", "determinant", "refract",
            "faceforward", "outerProduct", "matrixCompMult")
# Preview values for the shader cards' uniforms (cards/looks/shader-*.md); any other float is 1, vec2 (0.5, 0.5),
# vec3 the colour ramp in declaration order. ponytail: a table, not parsed from the cards' prose ranges.
PREVIEW = {"uHem": 0.35, "uCount": 8.0, "uProgress": 0.5, "uPixel": 4.0, "uGrain": 0.08, "uCell": 8.0,
           "uAngle": 0.2618, "uReach": 0.8, "uSpread": 0.6, "uSoft": 0.15}
RAMP = ((0.09, 0.1, 0.13), (0.93, 0.91, 0.86), (0.85, 0.42, 0.24), (0.27, 0.56, 0.72))  # dark, light, accents


class ShadeError(ValueError):
    pass


class _Undef(Exception):
    """discard, or a function falling off its end: that pixel is black and counted"""


def vtype(base, n):
    return base if n == 1 else {"float": "", "int": "i", "uint": "u", "bool": "b"}[base] + f"vec{n}"


def shape(t):
    return "m" if t.startswith("mat") else "v" if "vec" in t else "s"


def lit(v):
    s = "True" if v is True else "False" if v is False else repr(v)
    return f"({s})" if s.startswith("-") else s


def zero(t):
    base, n = TYPES[t]
    z = {"float": "0.0", "int": "0", "uint": "0", "bool": "False"}[base]
    return z if n == 1 else "(" + ", ".join([z] * n) + ")"


class E:
    __slots__ = ("c", "t", "k", "lv")

    def __init__(self, c, t, k=None, lv=None):
        self.c, self.t, self.k, self.lv = c, t, k, lv


# --- runtime: what the generated code calls ---
def _wi(x):
    return ((x + 0x80000000) & M) - 0x80000000


def _idiv(a, b):
    q = abs(a) // abs(b)
    return _wi(q if (a < 0) == (b < 0) else -q)


def _ss(a, b, x):
    if a == b:  # a zero-width edge: a step, as a GPU's inf clamps to
        return 0.0 if x < a else 1.0
    t = min(max((x - a) / (b - a), 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


def _L(f, *a):  # f applied componentwise, scalars broadcast
    n = max(len(x) for x in a if type(x) is tuple)
    return tuple(map(f, *[x if type(x) is tuple else (x,) * n for x in a]))


def _mv(n, m, v):
    if n == 2:
        return (m[0] * v[0] + m[2] * v[1], m[1] * v[0] + m[3] * v[1])
    return tuple([sum([m[c * n + r] * v[c] for c in range(n)]) for r in range(n)])


def _vm(n, v, m):
    return tuple([sum([v[r] * m[c * n + r] for r in range(n)]) for c in range(n)])


def _mm(n, a, b):
    return tuple([sum([a[k * n + r] * b[c * n + k] for k in range(n)]) for c in range(n) for r in range(n)])


def _mk(n, conv, *args):
    out = []
    for a in args:
        out.extend(a) if type(a) is tuple else out.append(a)
    return tuple(map(conv, out[:n])) if conv else tuple(out[:n])


def _set(v, idx, val):
    v = list(v)
    for i, x in zip(idx, val):
        v[i] = x
    return tuple(v)


def _norm(v):
    d = math.hypot(*v)
    return tuple([x / d for x in v])


def _dot(a, b):
    return sum(map(operator.mul, a, b))


def _reflect(i, n):
    d = 2.0 * (_dot(i, n) if type(i) is tuple else i * n)
    return tuple([x - d * y for x, y in zip(i, n)]) if type(i) is tuple else i - d * n


SC = dict(radians=math.radians, degrees=math.degrees, sin=math.sin, cos=math.cos, tan=math.tan, asin=math.asin,
          acos=math.acos, atan=math.atan, atan2=math.atan2, exp=math.exp, log=math.log, exp2=lambda x: 2.0 ** x,
          log2=math.log2, sqrt=math.sqrt, inversesqrt=lambda x: 1.0 / math.sqrt(x), floor=lambda x: x // 1.0,
          ceil=lambda x: -(-x // 1.0), trunc=lambda x: float(math.trunc(x)), round=lambda x: (x + 0.5) // 1.0,
          fract=lambda x: x % 1.0, abs=abs, sign=lambda x: type(x)((x > 0) - (x < 0)), pow=math.pow,
          mod=lambda x, y: x % y, min=min, max=max, clamp=lambda x, a, b: min(max(x, a), b),
          mix=lambda a, b, t: a * (1.0 - t) + b * t, step=lambda e, x: 0.0 if x < e else 1.0, smoothstep=_ss)
RUNTIME = {"__builtins__": {}, "abs": abs, "min": min, "max": max, "tuple": tuple, "map": map, "float": float,
           "int": int, "bool": bool, "_L": _L, "_mv": _mv, "_vm": _vm, "_mm": _mm, "_mk": _mk, "_set": _set,
           "_Undef": _Undef, "_norm": _norm, "_dot": _dot, "_reflect": _reflect, "_hypot": math.hypot,
           "_dist": math.dist, "_wi": _wi,
           "_sw": lambda v, idx: tuple([v[i] for i in idx]),
           "_vs": lambda f, a, s: tuple([f(x, s) for x in a]), "_sv": lambda f, s, a: tuple([f(s, x) for x in a]),
           "_neg": lambda v: tuple([-x for x in v]),
           "_cross": lambda a, b: (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]),
           "_diag": lambda n, x: tuple([x if c == r else 0.0 for c in range(n) for r in range(n)]),
           "_to_float": float, "_to_int": lambda x: _wi(int(x)), "_to_uint": lambda x: int(x) & M,
           "_to_bool": bool}
RUNTIME.update({f"_b_{k}": f for k, f in SC.items()})
_shl = lambda a, b: a << (b & 31)  # noqa: E731
_shr = lambda a, b: a >> (b & 31)  # noqa: E731
for _k, _f in dict(add=operator.add, sub=operator.sub, mul=operator.mul, div=operator.truediv).items():
    RUNTIME[f"_o_float_{_k}"] = _f
for _k, _f in dict(add=operator.add, sub=operator.sub, mul=operator.mul, shl=_shl).items():
    RUNTIME[f"_o_int_{_k}"] = lambda a, b, f=_f: _wi(f(a, b))
    RUNTIME[f"_o_uint_{_k}"] = lambda a, b, f=_f: f(a, b) & M
for _k, _f in dict(**{"and": operator.and_, "or": operator.or_, "xor": operator.xor}, shr=_shr).items():
    RUNTIME[f"_o_int_{_k}"] = RUNTIME[f"_o_uint_{_k}"] = _f
RUNTIME.update(_o_int_div=_idiv, _o_int_mod=lambda a, b: _wi(a - b * _idiv(a, b)),
               _o_uint_div=operator.floordiv, _o_uint_mod=operator.mod)
# builtins: allowed bases (f float, i int, u uint), argument patterns (T the genType, s its scalar), result
BUILT = {n: ("f", "T", "T") for n in "radians degrees sin cos tan asin acos exp log exp2 log2 sqrt inversesqrt "
         "floor ceil trunc round fract normalize dFdx dFdy fwidth".split()}
BUILT.update(abs=("fi", "T", "T"), sign=("fi", "T", "T"), atan=("f", "T TT", "T"), pow=("f", "TT", "T"),
             mod=("f", "TT Ts", "T"), min=("fiu", "TT Ts", "T"), max=("fiu", "TT Ts", "T"),
             clamp=("fiu", "TTT Tss", "T"), mix=("f", "TTT TTs", "T"), step=("f", "TT sT", "T"),
             smoothstep=("f", "TTT ssT", "T"), length=("f", "T", "s"), distance=("f", "TT", "s"),
             dot=("f", "TT", "s"), cross=("f", "TT", "T"), reflect=("f", "TT", "T"))
INLINE = {"floor": "({0} // 1.0)", "fract": "({0} % 1.0)", "mod": "({0} % {1})", "abs": "abs({0})",
          "min": "min({0}, {1})", "max": "max({0}, {1})"}


def _tokens(src, first):
    out, pos, line = [], 0, first
    while pos < len(src):
        if src.startswith("/*", pos) and src.find("*/", pos + 2) < 0:
            raise ShadeError(f"line {line}: a /* comment never ends")
        m = TOKEN.match(src, pos)
        if not m:
            raise ShadeError(f"line {line}: {src[pos]!r} is outside the subset")
        if m.lastgroup == "pp":
            word = re.match(r"#\s*(\w*)", m.group()).group(1)
            if word not in ("version", "extension") or src[src.rfind("\n", 0, pos) + 1:pos].strip():
                raise ShadeError(f"line {line}: #{word} is outside the subset")
        elif m.lastgroup != "skip":
            out.append((m.lastgroup, m.group(), line))
        line, pos = line + m.group().count("\n"), m.end()
    return out + [("end", "the end", line)]


class _Compiler:
    def __init__(self, src, first):
        self.toks, self.i = _tokens(src, first), 0
        self.scopes = [{"gl_FragCoord": ("_fc", "vec4", True)}]
        self.funcs, self.uniforms, self.out, self.code = {}, {}, [], []
        self.outvar, self.fn, self.loops, self.n, self.sites = None, None, 0, 0, []  # sites: each derivative's line

    # tokens
    def peek(self, o=0):
        return self.toks[min(self.i + o, len(self.toks) - 1)]

    def take(self):
        t = self.peek()
        if t[0] == "end":
            self.fail(t, "the shader ends early")
        self.i += 1
        return t

    def at(self, s):
        return self.peek()[1] == s and self.peek()[0] != "end"

    def eat(self, s):
        return self.at(s) and bool(self.take())

    def want(self, s):
        t = self.take()
        if t[1] != s or t[0] == "end":
            self.fail(t, f"expected {s!r}, found {t[1]!r}")
        return t

    def name(self):
        t = self.take()
        if t[0] != "id":
            self.fail(t, f"expected a name, found {t[1]!r}")
        return t

    def fail(self, tok, msg):
        raise ShadeError(f"line {tok[2]}: {msg}")

    def emit(self, ind, s):
        self.out.append("    " * ind + s)

    def type(self):
        while self.peek()[1] in PRECISION:
            self.take()
        t = self.take()
        if t[1] not in TYPES or t[0] != "id":
            self.fail(t, f"{t[1]} is outside the subset")
        return t[1]

    def declare(self, tok, ty, ro, py=None):
        if tok[1] in self.scopes[-1]:
            self.fail(tok, f"{tok[1]} is already declared here")
        self.n += 1
        py = py or f"l_{tok[1]}_{self.n}"
        self.scopes[-1][tok[1]] = (py, ty, ro)
        return py

    # top level
    def run(self):
        while self.peek()[0] != "end":
            self.top()
        entry = next((o[0][2] for n in ("main", "mainImage") for o in [self.funcs.get(n)] if o), None)
        if not entry:
            raise ShadeError("no main() or mainImage(): nothing to run")
        return "\n".join(self.code) + "\n", entry

    def top(self):
        t = self.peek()
        if t[1] in ("precision", "layout"):
            while not self.eat(";" if t[1] == "precision" else ")"):
                self.take()
            return
        qual = self.take()[1] if t[1] in ("uniform", "in", "out", "const", "varying") else None
        ty = self.type()
        tok = self.name()
        if qual is None and self.at("("):
            return self.function(ty, tok)
        if qual is None:
            self.fail(tok, "a global variable is outside the subset: make it const, or move it into a function")
        while True:
            if self.at("["):
                self.fail(tok, "arrays are outside the subset")
            if qual == "uniform":
                self.declare(tok, ty, True, f"u_{tok[1]}")
                self.uniforms[tok[1]] = ty
            elif qual in ("in", "varying"):
                if ty != "vec2":
                    self.fail(tok, f"in {ty} {tok[1]}: only an in vec2 (the uv) is fed")
                self.declare(tok, ty, True, "_uv")
            elif qual == "out":
                if ty != "vec4":
                    self.fail(tok, f"out {ty} {tok[1]}: only an out vec4 is drawn")
                self.outvar = tok[1]
            else:
                self.want("=")
                e = self.expr()
                if e.t != ty:
                    self.fail(tok, f"{tok[1]} is a {ty}, but this is a {e.t}")
                self.code.append(f"{self.declare(tok, ty, True, f'g_{tok[1]}_{self.n + 1}')} = {e.c}")
            if not self.eat(","):
                break
            tok = self.name()
        self.want(";")

    def function(self, rt, tok):
        name, params, outp = tok[1], [], None
        self.want("(")
        if self.at("void") and self.peek(1)[1] == ")":
            self.take()
        while not self.eat(")"):
            quals = []
            while self.peek()[1] in ("in", "out", "inout", "const"):
                quals.append(self.take()[1])
            ty, ptok = self.type(), self.name()
            if self.at("["):
                self.fail(ptok, "arrays are outside the subset")
            if "out" in quals or "inout" in quals:
                if name != "mainImage" or params or ty != "vec4":
                    self.fail(ptok, "out parameters are outside the subset (but mainImage's)")
                outp = ptok
            params.append((ptok, ty))
            if not self.at(")"):
                self.want(",")
        if self.at(";"):
            self.fail(tok, f"a prototype is outside the subset: define {name}() before its first use")
        sig = tuple(ty for _, ty in params)
        entry = (name == "main" and not sig) or (name == "mainImage" and sig == ("vec4", "vec2") and outp)
        if name in ("main", "mainImage") and (not entry or rt != "void"):
            self.fail(tok, f"{name}() must be void main() or void mainImage(out vec4, in vec2)")
        overloads = self.funcs.setdefault(name, [])
        if any(o[0] == sig for o in overloads):
            self.fail(tok, f"{name}({', '.join(sig)}) is already defined")
        py = f"f_{name}_{len(overloads)}"
        self.scopes.append({})
        if entry:
            self.scopes[-1][outp[1] if outp else self.outvar or "gl_FragColor"] = ("o_", "vec4", False)
        args = [self.declare(p, ty, False, f"a_{p[1]}") for p, ty in params if p is not outp]
        self.out, self.fn = [f"def {py}({', '.join(args)}):"], (name, rt, entry)
        self.emit(1, "o_ = (0.0, 0.0, 0.0, 0.0)" if entry else f"_tick({tok[2]})")  # calls count, as loops do
        self.block(1)
        if entry:
            self.emit(1, "return o_")
        elif rt != "void":
            self.emit(1, "raise _Undef()")  # GLSL leaves falling off the end undefined
        self.scopes.pop()
        overloads.append((sig, rt, py))  # after the body: a call to itself finds nothing, as GLSL has no recursion
        self.code += self.out

    # statements
    def block(self, ind):
        self.want("{")
        self.scopes.append({})
        n = len(self.out)
        while not self.eat("}"):
            if self.peek()[0] == "end":
                self.fail(self.peek(), "a { is never closed")
            self.stmt(ind)
        if len(self.out) == n:
            self.emit(ind, "pass")
        self.scopes.pop()

    def sub(self, ind):
        n = len(self.out)
        self.scopes.append({})
        self.stmt(ind)
        self.scopes.pop()
        if len(self.out) == n:
            self.emit(ind, "pass")

    def cond(self):
        self.want("(")
        e = self.expr()
        if e.t != "bool":
            self.fail(self.peek(), f"a condition must be a bool, not a {e.t}")
        self.want(")")
        return e.c

    def stmt(self, ind):
        t = self.peek()
        w = t[1]
        if w == "{":
            return self.block(ind)
        if w in ("continue", "do", "switch", "struct", "case", "default"):
            self.fail(t, f"{w} is outside the subset")
        if w == ";":
            self.take()
        elif w == "if":
            self.take()
            self.emit(ind, f"if {self.cond()}:")
            self.sub(ind + 1)
            if self.eat("else"):
                self.emit(ind, "else:")
                self.sub(ind + 1)
        elif w == "while":
            self.take()
            self.emit(ind, f"while {self.cond()}:")
            self.loop(ind, t, [])
        elif w == "for":
            self.take()
            self.want("(")
            self.scopes.append({})
            if not self.eat(";"):
                self.decl(ind) if self.is_decl() else (self.simple(ind), self.want(";"))
            c = "True"
            if not self.at(";"):
                e = self.expr()
                if e.t != "bool":
                    self.fail(t, f"a condition must be a bool, not a {e.t}")
                c = e.c
            self.want(";")
            saved, self.out = self.out, []
            if not self.at(")"):
                self.simple(ind + 1)
            step, self.out = self.out, saved
            self.want(")")
            self.emit(ind, f"while {c}:")
            self.loop(ind, t, step)
            self.scopes.pop()
        elif w in ("break", "discard"):
            self.take()
            if w == "break" and not self.loops:
                self.fail(t, "break outside a loop")
            self.emit(ind, "break" if w == "break" else "raise _Undef()")
            self.want(";")
        elif w == "return":
            self.take()
            name, rt, entry = self.fn
            if self.eat(";"):
                if rt != "void":
                    self.fail(t, f"{name}() must return a {rt}")
                return self.emit(ind, "return o_" if entry else "return")
            e = self.expr()
            if e.t != rt:
                self.fail(t, f"this returns a {e.t}, but {name}() returns {rt}")
            self.emit(ind, f"return {e.c}")
            self.want(";")
        elif self.is_decl():
            self.decl(ind)
        else:
            self.simple(ind)
            self.want(";")

    def loop(self, ind, tok, step):
        self.emit(ind + 1, f"_tick({tok[2]})")
        self.loops += 1
        self.sub(ind + 1)
        self.loops -= 1
        self.out += step

    def is_decl(self):
        t, nxt = self.peek(), self.peek(1)
        if t[1] == "const" or t[1] in PRECISION:
            return True
        if t[0] == "id" and nxt[0] == "id" and t[1] not in TYPES:
            self.fail(t, f"{t[1]} is outside the subset")
        return t[1] in TYPES and nxt[0] == "id"

    def decl(self, ind):
        const = self.eat("const")
        ty = self.type()
        while True:
            tok = self.name()
            if self.at("["):
                self.fail(tok, "arrays are outside the subset")
            code = zero(ty)
            if self.eat("="):
                e = self.expr()
                if e.t != ty:
                    self.fail(tok, f"{tok[1]} is a {ty}, but this is a {e.t}")
                code = e.c
            elif const:
                self.fail(tok, f"const {tok[1]} needs a value")
            self.emit(ind, f"{self.declare(tok, ty, const)} = {code}")
            if not self.eat(","):
                break
        self.want(";")

    def simple(self, ind):
        t = self.peek()
        if t[1] in ("++", "--"):
            self.take()
            return self.assign(ind, self.postfix(), t[1][0] + "=", None, t)
        lhs = self.expr()
        t = self.peek()
        if t[1] in ASSIGN:
            self.take()
            return self.assign(ind, lhs, t[1], self.expr(), t)
        if t[1] in ("++", "--"):
            self.take()
            return self.assign(ind, lhs, t[1][0] + "=", None, t)
        self.emit(ind, lhs.c)

    def assign(self, ind, lhs, op, rhs, tok):
        if lhs.lv is None:
            self.fail(tok, f"the left of {op} can't be assigned")
        kind, py, name, ro, idx = lhs.lv
        if ro:
            self.fail(tok, f"{name} is read-only")
        if rhs is None:  # ++ and --
            base = TYPES[lhs.t][0]
            rhs = E(lit(1.0 if base == "float" else 1), base, 1)
        if op != "=":
            rhs = self.binop(op[:-1], lhs, rhs, tok)
        if rhs.t != lhs.t:
            self.fail(tok, f"{name} is a {lhs.t}, but this is a {rhs.t}")
        val = rhs.c if kind == "v" else f"_set({py}, {idx!r}, {rhs.c if len(idx) > 1 else f'({rhs.c},)'})"
        self.emit(ind, f"{py} = {val}")

    # expressions
    def expr(self):
        c = self.binary(1)
        if not self.at("?"):
            return c
        t = self.take()
        a = self.expr()
        self.want(":")
        b = self.expr()
        if c.t != "bool" or a.t != b.t:
            self.fail(t, f"{c.t} ? {a.t} : {b.t} doesn't type-check")
        return E(f"({a.c} if {c.c} else {b.c})", a.t)

    def binary(self, lvl):
        left = self.unary()
        while True:
            t = self.peek()
            p = PREC.get(t[1]) if t[0] == "op" else None
            if p is None or p < lvl:
                return left
            self.take()
            left = self.binop(t[1], left, self.binary(p + 1), t)

    def binop(self, op, a, b, tok):
        ta, tb = a.t, b.t
        (ba, na), (bb, nb) = TYPES[ta], TYPES[tb]
        ka, kb = shape(ta), shape(tb)

        def bad():
            self.fail(tok, f"{ta} {op} {tb} doesn't type-check")
        if op in ("&&", "||", "^^"):
            if ta != "bool" or tb != "bool":
                bad()
            return E(f"({a.c} {dict(zip(('&&', '||', '^^'), ('and', 'or', '!=')))[op]} {b.c})", "bool")
        if op in ("==", "!="):
            return E(f"({a.c} {op} {b.c})", "bool") if ta == tb else bad()
        if op in ("<", ">", "<=", ">="):
            return E(f"({a.c} {op} {b.c})", "bool") if ta == tb and ta in ("float", "int", "uint") else bad()
        shift = op in ("<<", ">>")
        if {"bool", "void"} & {ba, bb} or (ba != bb and not shift) or (ba == "float" and op in "%&|^<<>>"):
            bad()
        if shift and (bb == "float" or kb == "v" and nb != na or ka == "s" and kb != "s"):
            bad()
        f = f"_o_{ba}_{OPN[op]}"
        if op == "*" and "m" in (ka, kb) and "s" not in (ka, kb):
            n = round(math.sqrt(na if ka == "m" else nb))
            if ka == kb == "m" and ta == tb:
                return E(f"_mm({n}, {a.c}, {b.c})", ta)
            if ka == "m" and kb == "v" and nb == n:
                return E(f"_mv({n}, {a.c}, {b.c})", tb)
            if ka == "v" and kb == "m" and na == n:
                return E(f"_vm({n}, {a.c}, {b.c})", ta)
            bad()
        if ta == tb or shift and kb == "s" and ka == "s":
            if ka != "s":
                return E(f"tuple(map({f}, {a.c}, {b.c}))", ta)
            return E(f"({a.c} {op} {b.c})" if ba == "float" else f"{f}({a.c}, {b.c})", ta)
        if ka != "s" and kb == "s":
            return E(f"_vs({f}, {a.c}, {b.c})", ta)
        if ka == "s" and kb != "s" and not shift:
            return E(f"_sv({f}, {a.c}, {b.c})", tb)
        if shift and ka == kb == "v":
            return E(f"tuple(map({f}, {a.c}, {b.c}))", ta)
        bad()

    def unary(self):
        t = self.peek()
        if t[1] in ("++", "--"):
            self.fail(t, f"{t[1]} inside an expression is outside the subset")
        if t[1] not in ("-", "+", "!", "~") or t[0] != "op":
            return self.postfix()
        self.take()
        e = self.unary()
        base, k = TYPES[e.t][0], shape(e.t)
        if t[1] == "+" and base != "bool":
            return e
        if t[1] == "!" and e.t == "bool":
            return E(f"(not {e.c})", "bool")
        if t[1] == "-" and base != "bool":
            if e.k is not None:
                v = -e.k if base == "float" else _wi(-e.k) if base == "int" else -e.k & M
                return E(lit(v), e.t, v)
            if k != "s":
                return E(f"tuple(map(_o_{base}_sub, {zero(e.t)}, {e.c}))" if base != "float" else f"_neg({e.c})",
                         e.t)
            return E(f"(-{e.c})" if base == "float" else f"_o_{base}_sub(0, {e.c})", e.t)
        if t[1] == "~" and base in ("int", "uint") and k == "s":
            return E(f"(~{e.c})" if base == "int" else f"(~{e.c} & {M})", e.t)
        self.fail(t, f"{t[1]}{e.t} doesn't type-check")

    def postfix(self):
        e = self.primary()
        while True:
            t = self.peek()
            if t[1] == "[":
                self.fail(t, "indexing is outside the subset: use a swizzle")
            if t[1] != ".":
                return e
            self.take()
            e = self.swizzle(e, self.name())

    def swizzle(self, e, f):
        base, n = TYPES[e.t]
        idx = next((tuple(s.index(ch) for ch in f[1]) for s in ("xyzw", "rgba", "stpq")
                    if all(ch in s for ch in f[1])), None)
        if shape(e.t) != "v" or idx is None or max(idx) >= n or len(idx) > 4:
            self.fail(f, f"{e.t} has no .{f[1]}")
        lv = e.lv and e.lv[0] == "v" and len(set(idx)) == len(idx) and ("s",) + e.lv[1:4] + (idx,)
        code = f"{e.c}[{idx[0]}]" if len(idx) == 1 else f"_sw({e.c}, {idx!r})"
        return E(code, vtype(base, len(idx)), None, lv or None)

    def primary(self):
        t = self.take()
        if t[0] == "num":
            return self.number(t)
        if t[1] == "(":
            e = self.expr()
            self.want(")")
            return e
        if t[0] != "id":
            self.fail(t, f"expected a value, found {t[1]!r}")
        if t[1] in ("true", "false"):
            return E(t[1].title(), "bool", t[1] == "true")
        if self.at("("):
            return self.call(t)
        for scope in reversed(self.scopes):
            if t[1] in scope:
                py, ty, ro = scope[t[1]]
                return E(py, ty, None, ("v", py, t[1], ro, None))
        if t[1] in SHADERTOY:
            self.scopes[0][t[1]] = (f"u_{t[1]}", SHADERTOY[t[1]], True)
            self.uniforms[t[1]] = SHADERTOY[t[1]]
            self.i -= 1
            return self.primary()
        self.fail(t, f"{t[1]} is not declared")

    def number(self, t):
        s = t[1]
        hexa = s[:2] in ("0x", "0X")
        if not hexa and ("." in s or "e" in s.lower()):
            v = float(s.rstrip("fF"))
            if not math.isfinite(v):
                self.fail(t, f"{s} is not a finite number")
            return E(lit(v), "float", v)
        d = s.rstrip("uU")
        try:
            v = int(d, 16 if hexa else 8 if len(d) > 1 and d[0] == "0" else 10)
        except ValueError:
            self.fail(t, f"{s} is not a number")
        if v > M:
            self.fail(t, f"{s} doesn't fit in 32 bits")
        ty = "uint" if s[-1] in "uU" else "int"
        v = v if ty == "uint" else _wi(v)
        return E(lit(v), ty, v)

    def call(self, t):
        name, args = t[1], []
        self.want("(")
        while not self.eat(")"):
            args.append(self.expr())
            if not self.at(")"):
                self.want(",")
        ts = [a.t for a in args]
        if name in TYPES and name != "void":
            return self.construct(name, args, t)
        if name in self.funcs:
            for sig, rt, py in self.funcs[name]:
                if list(sig) == ts:
                    return E(f"{py}({', '.join(a.c for a in args)})", rt)
            self.fail(t, f"no {name}({', '.join(ts)}) is declared")
        if name in BUILT:
            return self.builtin(name, args, t)
        self.fail(t, f"{name}() is {'outside the subset' if name in NOT_HERE else 'not declared'}")

    def convert(self, a, base):
        src = TYPES[a.t][0]
        if src == base:
            return a.c
        if a.k is not None:
            return lit(RUNTIME[f"_to_{base}"](a.k))
        return f"_to_{base}({a.c})" if shape(a.t) == "s" else f"tuple(map(_to_{base}, {a.c}))"

    def construct(self, ty, args, t):
        base, n = TYPES[ty]
        sizes = [TYPES[a.t][1] for a in args]
        if not args or any(a.t.startswith("mat") or a.t == "void" for a in args):
            self.fail(t, f"{ty}({', '.join(a.t for a in args)}) is outside the subset")
        if n == 1:
            if len(args) != 1:
                self.fail(t, f"{ty}() takes one value")
            a = args[0]
            c = a if shape(a.t) == "s" else E(f"{a.c}[0]", TYPES[a.t][0])
            return E(self.convert(c, base), ty, None if c.k is None else RUNTIME[f"_to_{base}"](c.k))
        if len(args) == 1 and sizes[0] == 1:
            c = self.convert(args[0], base)
            return E(f"_diag({round(math.sqrt(n))}, {c})" if ty.startswith("mat") else f"(({c}),) * {n}", ty)
        total = sum(sizes)
        if total < n or total - sizes[-1] >= n:
            self.fail(t, f"{ty}() takes {n} components, not {total}")
        if total == n:
            parts = [self.convert(a, base) if s == 1 else
                     f"*{a.c}" if TYPES[a.t][0] == base else f"*tuple(map(_to_{base}, {a.c}))"
                     for a, s in zip(args, sizes)]
            return E(f"({', '.join(parts)},)", ty)
        return E(f"_mk({n}, _to_{base}, {', '.join(a.c for a in args)})", ty)

    def builtin(self, name, args, t):
        ts = [a.t for a in args]
        bases, pats, res = BUILT[name]
        for p in pats.split():
            if len(p) != len(args):
                continue
            T = ts[p.index("T")]
            base = TYPES[T][0]
            s = base
            if shape(T) == "m" or base[0] not in bases or not all(ts[i] == (T if c == "T" else s)
                                                                  for i, c in enumerate(p)):
                continue
            if name == "cross" and T != "vec3":
                continue
            out = T if res == "T" else s
            cs = [a.c for a in args]
            vec = shape(T) == "v"
            if name in ("dFdx", "dFdy", "fwidth"):
                self.sites.append(self.toks[self.i - 1][2])
                return E(f"_d({('dFdx', 'dFdy', 'fwidth').index(name)}, {len(self.sites) - 1}, {cs[0]})", out)
            special = {"length": ("_hypot(*{0})", "abs({0})"), "distance": ("_dist({0}, {1})", "abs({0} - {1})"),
                       "dot": ("_dot({0}, {1})", "({0} * {1})"), "normalize": ("_norm({0})", "_b_sign({0})"),
                       "cross": ("_cross({0}, {1})", ""), "reflect": ("_reflect({0}, {1})", "_reflect({0}, {1})")}
            if name in special:
                return E(special[name][0 if vec else 1].format(*cs), out)
            fn = "atan2" if name == "atan" and len(args) == 2 else name
            if not vec:
                return E(INLINE[fn].format(*cs) if fn in INLINE else f"_b_{fn}({', '.join(cs)})", out)
            if len(args) == 1:
                return E(f"tuple(map(_b_{fn}, {cs[0]}))", out)
            return E(f"_L(_b_{fn}, {', '.join(cs)})", out)
        self.fail(t, f"no {name}({', '.join(ts)}) is built in")


def _uniforms(declared, sets, w, h, time):
    """u_NAME: value for each uniform, and the names that took a preview default."""
    values, defaulted, ramp = {}, [], 0
    for name, vals in sets.items():
        if name not in declared:
            raise ShadeError(f"{name} is not a uniform here (declared: {', '.join(declared) or 'none'})")
        n = TYPES[declared[name]][1]
        if len(vals) != n:
            raise ShadeError(f"{name} is a {declared[name]}: {n} number{'s' * (n > 1)}, not {len(vals)}")
    for name, ty in declared.items():
        base, n = TYPES[ty]
        conv = RUNTIME[f"_to_{base}"]
        if name in sets:
            v = tuple(map(conv, sets[name]))
        elif name in ("uRes", "uResolution", "iResolution") and base == "float" and n in (2, 3):
            v = (float(w), float(h), 1.0)[:n]
        elif name in ("uTime", "iTime") and ty == "float":
            v = (float(time),)
        elif name in ("iFrame", "iMouse"):
            v = (int(time * 60),) if name == "iFrame" else (0.0,) * 4
        else:
            defaulted.append(name)
            if name in PREVIEW and ty == "float":
                v = (PREVIEW[name],)
            elif ty in ("vec3", "vec4"):
                v, ramp = RAMP[ramp % 4] + (1.0,) * (n - 3), ramp + 1
            elif ty == "vec2":
                v = (0.5, 0.5)
            elif ty.startswith("mat"):
                v = RUNTIME["_diag"](round(math.sqrt(n)), 1.0)
            else:
                v = (conv(1),) * n
        values[f"u_{name}"] = v[0] if n == 1 else tuple(v)
    return values, defaulted


def _byte(c):
    return 0 if not c > 0 else 255 if c >= 1 else int(c * 255 + 0.5)  # NaN is black, inf white


def render(src, w, h, sets=None, time=0.0, first_line=1):
    """(rgb bytes, rows top-down; notes) for the shader at w x h. notes: defaulted uniforms, undefined pixels."""
    try:
        return _render(src, w, h, sets, time, first_line)
    except (SyntaxError, RecursionError, MemoryError) as e:  # Python's own limits on nesting
        raise ShadeError(f"the shader is too deep for this interpreter ({type(e).__name__})") from e
    except ArithmeticError as e:  # a const that divides by zero, a --set value an int can't hold
        raise ShadeError(f"the shader can't run: {type(e).__name__}: {e}") from e


def _render(src, w, h, sets, time, first_line):
    comp = _Compiler(src, first_line)
    code, entry = comp.run()
    values, defaulted = _uniforms(comp.uniforms, sets or {}, w, h, time)
    ns = dict(RUNTIME, **values)
    budget, seen, calls, vals, gx, gy, drawing = [0, 0], {}, {}, {}, 0, 0, True

    def _tick(line):
        budget[0] += 1
        budget[1] += 1
        if budget[0] > LIMIT:
            raise ShadeError(f"line {line}: past {LIMIT} loop turns and calls in one pixel")
        if budget[1] > TOTAL:
            raise ShadeError(f"line {line}: the render ran past {TOTAL} steps: try a smaller --size")

    def _d(kind, site, v):  # a GPU differences the 2x2 quad: the first pass records, the second differences
        n = calls.get(site, 0)
        if len(vals) >= DERIVS:
            raise ShadeError(f"line {comp.sites[site]}: more than {DERIVS} derivatives in one pixel")
        calls[site], vals[(site, n)] = n + 1, v
        out = []
        for axis, size, here in ((0, w, gx), (1, h, gy)):
            a = here - (here & 1)
            a, b = (a, a + 1) if a + 1 < size else (here - 1, here)
            p0, p1 = ((a, gy), (b, gy)) if axis == 0 else ((gx, a), (gx, b))
            v0, v1 = seen.get(p0, {}).get((site, n)), seen.get(p1, {}).get((site, n))
            if not drawing or a < 0 or v0 is None or v1 is None:
                out.append(tuple([0.0] * len(v)) if type(v) is tuple else 0.0)
            else:
                out.append(tuple(map(operator.sub, v1, v0)) if type(v) is tuple else v1 - v0)
        if kind < 2:
            return out[kind]
        if type(v) is tuple:
            return tuple([abs(x) + abs(y) for x, y in zip(*out)])
        return abs(out[0]) + abs(out[1])
    ns.update(_tick=_tick, _d=_d, _fc=None, _uv=None)
    exec(compile(code, "<shader>", "exec"), ns)
    fn, rgb, undefined = ns[entry], bytearray(), 0
    toy = entry.startswith("f_mainImage")

    def pixel(x, y, draw):
        nonlocal gx, gy, drawing, calls, vals
        gx, gy, drawing, calls, vals = x, y, draw, {}, {}
        fc = (x + 0.5, y + 0.5)
        ns["_fc"], ns["_uv"] = fc + (0.5, 1.0), (fc[0] / w, fc[1] / h)
        budget[0] = 0
        try:
            return fn(fc) if toy else fn()
        except ShadeError:
            raise
        except (ZeroDivisionError, ValueError, OverflowError, _Undef):
            return None
        finally:
            if not draw:
                seen[(x, y)] = vals

    # ponytail: a derivative of a value that itself took a derivative reads first-pass zeros: one level deep.
    kept = set()  # rows recorded for derivatives: only the quads around the row being drawn
    for y in range(h - 1, -1, -1):
        if comp.sites:
            a = y - (y & 1)
            for r in ((a, a + 1) if a + 1 < h else (y - 1, y)):
                if r >= 0 and r not in kept:
                    kept.add(r)
                    for x in range(w):
                        pixel(x, r, False)
            for r in [r for r in kept if r > y + 1]:
                kept.discard(r)
                for x in range(w):
                    del seen[(x, r)]
        for x in range(w):
            col = pixel(x, y, True)
            if col is None:
                undefined += 1
                rgb += b"\0\0\0"
            else:
                rgb += bytes(_byte(c) for c in col[:3])
    return bytes(rgb), {"defaulted": defaulted, "undefined": undefined}


def source(path):
    """(GLSL, its first line's number in the file): a card's first fragment block, or a whole .frag file."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not path.endswith(".md"):
        return text, 1
    from fmscene import GLSL
    for m in GLSL.finditer(text):
        if "gl_Position" not in m.group(1):
            return m.group(1), text.count("\n", 0, m.start(1)) + 1
    raise ShadeError(f"{path}: no fragment shader (a glsl block without gl_Position)")
