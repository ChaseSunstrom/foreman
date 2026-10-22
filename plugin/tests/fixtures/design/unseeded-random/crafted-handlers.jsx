import { useEffect, useState } from "react";

const SESSION = Math.random().toString(36).slice(2);

export function Dice() {
  const [roll, setRoll] = useState(1);
  const reroll = () => setRoll(1 + Math.floor(Math.random() * 6));
  function handleKey() {
    setRoll(1 + Math.floor(Math.random() * 6));
  }
  useEffect(() => {
    const id = setInterval(() => setRoll(1 + Math.floor(Math.random() * 6)), 1000);
    return () => clearInterval(id);
  }, []);
  return (
    <button onClick={() => setRoll(1 + Math.floor(Math.random() * 6))} onKeyDown={handleKey} data-s={SESSION}>
      {roll} {reroll.name}
    </button>
  );
}
