---
name: unsafe-deserialization
title: Unsafe deserialization
area: security
tags: [security, deserialization, pickle, yaml, rce, serialization]
detect: [dep:pyyaml, dep:jsonpickle, dep:dill, dep:cloudpickle, dep:node-serialize, dep:serialize-javascript, dep:xstream]
related: [input-validation, command-injection, dependency-audit, semgrep]
---
Never deserialize untrusted bytes with a format that can build arbitrary objects; use data-only formats with a schema.

## Verify
- `semgrep scan --config p/security-audit --error`: no `pickle.loads`, `yaml.load`, `eval` or unsafe loaders on external data.
- `grep -rnE "pickle\.loads?|yaml\.load\(|marshal\.loads|jsonpickle\.decode|ObjectInputStream|unserialize\(|Marshal\.load|BinaryFormatter" src/`: every hit is a trusted-source use or removed.
- `bandit -r src -t B301,B302,B506`: pickle, marshal and unsafe-YAML findings are clear.

## Test first
Show that a crafted payload does not execute and is rejected.
```python
import pickle, os, pytest
class Evil:
    def __reduce__(self):
        return (os.system, ("touch /tmp/pwned",))

def test_import_endpoint_rejects_pickle(client):
    r = client.post("/import", data=pickle.dumps(Evil()))
    assert r.status_code in (400, 415)
    assert not os.path.exists("/tmp/pwned")

def test_yaml_tag_does_not_construct_objects(load_config):
    with pytest.raises(Exception):
        load_config("!!python/object/apply:os.system ['id']")
```

## Do
- Use JSON (or MessagePack, Protobuf) and validate it with a schema into typed models.
- Parse YAML with `yaml.safe_load` (PyYAML) or `YAML.safe_load` (Ruby Psych), and Jackson with default typing off.
- If pickle is unavoidable between your own trusted processes, sign the bytes with HMAC and verify before loading.
- Java: set an `ObjectInputFilter` allowlist, or avoid native serialization. Configure XStream's security allowlist.
- .NET: avoid `BinaryFormatter` (removed from supported use), and use `System.Text.Json`.
- PHP: use `json_decode` rather than `unserialize`, or pass `allowed_classes => false`.
- Treat cache, queue and session stores as untrusted if other writers can reach them.

## Avoid
- `pickle.load` on files, cache entries, ML model uploads or network input: it runs code. Use safetensors or a data format, or sign and verify.
- `yaml.load(data)` without `Loader=SafeLoader`: `!!python/object` constructs arbitrary objects. Use `safe_load`.
- `eval`, `exec`, `new Function` and `vm.runInNewContext` to parse data: use `JSON.parse` or `ast.literal_eval` for literals.
- Jackson `enableDefaultTyping` or `@JsonTypeInfo(use = Id.CLASS)` on external data: gadget chains. Use a typed allowlist.
- Trusting a signature check that happens after deserialization: verify first.
- node-serialize `unserialize` on cookies: immediately executable. Use signed JSON.

## Review
- [ ] No object-capable deserializer reads external data.
- [ ] YAML uses the safe loader.
- [ ] Structured input is validated against a schema after parsing.
- [ ] Any retained binary format is HMAC-verified first.
- [ ] A malicious-payload test exists for each import path.
