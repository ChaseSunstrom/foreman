(function () {
  var root = document.documentElement;
  try { var t = localStorage.getItem("fm-theme"); if (t) root.setAttribute("data-theme", t); } catch (e) {}
  var toggle = document.querySelector(".theme");
  if (toggle) toggle.addEventListener("click", function () {
    var dark = root.getAttribute("data-theme") === "dark" ||
      (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
    var next = dark ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("fm-theme", next); } catch (e) {}
  });

  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = document.getElementById(b.getAttribute("data-copy")).textContent;
      var done = function () { b.textContent = "Copied"; b.setAttribute("data-done", ""); setTimeout(function () { b.textContent = "Copy"; b.removeAttribute("data-done"); }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {}); else done();
    });
  });

  var still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var reel = document.getElementById("reel");
  var stations = document.querySelectorAll("#stations li");
  if (still || !("IntersectionObserver" in window)) {
    if (reel) reel.setAttribute("controls", "");
    stations.forEach(function (li) { li.classList.add("on"); });
    return;
  }
  // the one orchestrated moment: the stations tick through in order when the loop comes into view
  var ticked = false;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.target === reel) { e.isIntersecting ? reel.play().catch(function () { reel.setAttribute("controls", ""); }) : reel.pause(); }
      if (e.target.id === "stations" && e.isIntersecting && !ticked) {
        ticked = true;
        stations.forEach(function (li, i) { setTimeout(function () { li.classList.add("on"); }, 220 * i + 150); });
      }
    });
  }, { threshold: 0.35 });
  // T-1615: each chart draws itself once, the first time it comes into view (CSS does the motion; seen still, it's whole)
  var charts = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("drawn"); charts.unobserve(e.target); }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll(".viz.grow-x, .viz.grow-y, .viz.draw").forEach(function (v) {
    v.querySelectorAll(".m").forEach(function (m, i) { m.style.transitionDelay = Math.min(i, 24) * 40 + "ms"; });
    v.classList.add("armed");
    charts.observe(v);
  });
  if (reel) io.observe(reel);
  var st = document.getElementById("stations");
  if (st) io.observe(st);
})();
