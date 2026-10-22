// const still = useReducedMotion(); (left for later)
export function Card({ up }) {
  return <div style={{ transition: "transform .2s ease", transform: up ? "translateY(-2px)" : "none" }} />; // expect
}
