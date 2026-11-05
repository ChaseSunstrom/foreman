/* The live page's look, set before the first paint. The server writes its default (the sampo
   setting live_theme) on <html data-theme>; a viewer's own choice, kept in localStorage, wins. */
(function () {
  var root = document.documentElement, pick = root.getAttribute("data-theme");
  try { var mine = localStorage.getItem("sampo-live-theme"); if (mine === "modern" || mine === "forge") pick = mine; } catch (e) {}
  if (pick !== "forge") pick = "modern";
  root.setAttribute("data-theme", pick);
  var meta = document.querySelector('meta[name="color-scheme"]');
  if (meta) meta.setAttribute("content", pick === "forge" ? "dark" : "dark light");
  document.title = pick === "forge" ? "Sampo · the live forge" : "Sampo · live";
})();
