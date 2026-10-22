function mulberry32(seed) {
  return () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function Stars({ n, seed = 7 }) {
  const rand = mulberry32(seed);
  return Array.from({ length: n }, (_, i) => <i key={i} style={{ left: `${rand() * 100}%` }} />);
}
