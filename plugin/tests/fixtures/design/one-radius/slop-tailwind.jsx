export function Panel() {
  return (
    <div className="rounded-lg p-4"> {/* expect */}
      <button className="rounded-lg px-3">Go</button>
      <input className="rounded-lg" />
      <img className="rounded-full" src="a.png" alt="" />
      <section className="rounded-lg">
        <span className="rounded-lg">new</span>
      </section>
    </div>
  );
}
