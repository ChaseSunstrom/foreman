export function Stars({ n }) {
  const tilt = Math.random() * 4; // expect
  return Array.from({ length: n }, (_, i) => (
    <i key={i} style={{ left: `${Math.random() * 100}%`, rotate: `${tilt}deg` }} /> // expect
  ));
}

export const Dot = () => <b style={{ top: Math.random() * 10 }} />; // expect
