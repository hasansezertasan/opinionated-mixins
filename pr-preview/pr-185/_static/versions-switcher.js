(() => {
  const choices = document.querySelector(".nav-versions-choices ul");
  if (!choices) return;

  const scriptUrl = document.currentScript.src;
  const siteRoot = new URL("../../", scriptUrl);
  const manifestUrl = new URL("../../latest/_static/versions.json", scriptUrl);
  fetch(manifestUrl, { cache: "no-store" })
    .then((response) => (response.ok ? response.json() : null))
    .then((manifest) => {
      if (!manifest || !Array.isArray(manifest.versions)) return;

      const items = [
        ["latest", new URL("latest/", siteRoot).href],
        ...manifest.versions.map((slug) => [slug, new URL(`${slug}/`, siteRoot).href]),
      ];
      choices.replaceChildren(
        ...items.map(([label, href]) => {
          const item = document.createElement("li");
          const link = document.createElement("a");
          link.href = href;
          link.textContent = label;
          item.append(link);
          return item;
        }),
      );
    })
    .catch(() => {});
})();
