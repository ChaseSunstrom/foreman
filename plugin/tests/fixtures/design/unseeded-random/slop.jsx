export function Stars({ n }) {
  return Array.from({ length: n }, (_, i) => (
    <i key={i} style={{ left: `${Math.random() * 100}%` }} /> // expect
  ));
}
