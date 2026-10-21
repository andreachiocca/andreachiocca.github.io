document.addEventListener("DOMContentLoaded", function () {
  const controls = document.querySelector(".publication-controls");
  const list = document.getElementById("publication-list");
  if (!controls || !list) return;

  const input = controls.querySelector("#bibsearch");
  const clear = controls.querySelector("#bibsearch-clear");
  const status = controls.querySelector("#bibsearch-status");
  const empty = controls.querySelector("#bibsearch-empty");
  const buttons = [...controls.querySelectorAll("[data-publication-type]")];
  const sections = [...list.querySelectorAll(".publication-section")];
  const groups = [...list.querySelectorAll("ol.bibliography")];
  const entries = [...list.querySelectorAll("ol.bibliography > li")];
  const searchable = entries.map(function (entry) {
    const year = entry.parentElement.previousElementSibling;
    const keywords = entry.querySelector("[data-publication-keywords]");
    return [entry.textContent, year?.textContent, keywords?.dataset.publicationKeywords]
      .join(" ").toLocaleLowerCase();
  });
  let selectedType = "all";

  function filter() {
    const terms = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    entries.forEach(function (entry, index) {
      const type = entry.closest(".publication-section").dataset.publicationType;
      entry.hidden = (selectedType !== "all" && type !== selectedType) ||
        !terms.every(term => searchable[index].includes(term));
      if (!entry.hidden) visible++;
    });
    groups.forEach(function (group) {
      group.hidden = ![...group.children].some(entry => !entry.hidden);
      const year = group.previousElementSibling;
      if (year?.matches("h2.bibliography")) year.hidden = group.hidden;
    });
    sections.forEach(function (section) {
      section.hidden = ![...section.querySelectorAll("ol.bibliography > li")]
        .some(entry => !entry.hidden);
    });
    buttons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.publicationType === selectedType)));
    clear.hidden = !input.value;
    empty.hidden = visible !== 0;
    status.textContent = status.dataset.countTemplate.replace("%visible%", visible).replace("%total%", entries.length);
  }

  function resetFilters() {
    selectedType = "all";
    input.value = "";
    filter();
  }

  buttons.forEach(button => button.addEventListener("click", function () {
    selectedType = button.dataset.publicationType;
    filter();
  }));
  input.addEventListener("input", filter);
  clear.addEventListener("click", function () { input.value = ""; filter(); input.focus(); });
  document.querySelectorAll('.publication-index a[href^="#"]').forEach(link => link.addEventListener("click", resetFilters));
  function revealLinkedPublication() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (target?.closest("li")?.hidden || target?.closest(".publication-section")?.hidden) {
      resetFilters();
      target.scrollIntoView();
    }
  }
  window.addEventListener("hashchange", revealLinkedPublication);
  controls.hidden = false;
  filter();
  revealLinkedPublication();
});
