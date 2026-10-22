import { useReducedMotion } from "framer-motion";

export function Card({ up }) {
  const still = useReducedMotion();
  return <div style={{ transition: still ? "none" : "transform .2s ease", transform: up ? "translateY(-2px)" : "none" }} />;
}
