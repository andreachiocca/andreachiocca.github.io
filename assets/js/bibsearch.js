/* Phase 4. Progressive filtering of the existing Jekyll Scholar HTML. */
document.addEventListener("DOMContentLoaded", function () {
  var input = document.getElementById("bibsearch");
  var list = document.getElementById("publication-list");
  var status = document.getElementById("bibsearch-status");
  var filters = document.getElementById("publication-type-filters");
  var empty = document.getElementById("bibsearch-empty");
  var clear = document.getElementById("bibsearch-clear");
  if (!input || !list || !status || !filters || !empty || !clear) return;

  var buttons = Array.from(filters.querySelectorAll("button[data-publication-filter]"));
  var categories = Array.from(list.querySelectorAll("section[data-publication-category]"));
  var selected = "all";

  function fold(value) {
    return String(value || "").normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase();
  }

  var entries = Array.from(list.querySelectorAll("ol.bibliography > li")).map(function (element) {
    var section = element.closest("section[data-publication-category]");
    var group = element.closest("ol.bibliography");
    var heading = group ? group.previousElementSibling : null;
    return {
      element: element,
      category: section ? section.dataset.publicationCategory : "",
      search: fold(element.textContent + " " + (heading && /^H[1-6]$/.test(heading.tagName) ? heading.textContent : ""))
    };
  });

  function filterPublications() {
    var terms = fold(input.value).trim().split(/\s+/).filter(Boolean);
    var totals = { all: entries.length, article: 0, inproceedings: 0, phdthesis: 0 };
    var visible = 0;

    entries.forEach(function (entry) {
      if (Object.prototype.hasOwnProperty.call(totals, entry.category)) {
        totals[entry.category] += 1;
      }
      var categoryMatches = selected === "all" || entry.category === selected;
      var matches = categoryMatches && terms.every(function (term) {
        return entry.search.includes(term);
      });
      entry.element.hidden = !matches;
      if (matches) visible += 1;
    });

    categories.forEach(function (section) {
      Array.from(section.querySelectorAll("ol.bibliography")).forEach(function (group) {
        var hasResults = Array.from(group.children).some(function (item) {
          return item.tagName === "LI" && !item.hidden;
        });
        group.hidden = !hasResults;
        var heading = group.previousElementSibling;
        if (heading && /^H[1-6]$/.test(heading.tagName) && heading.classList.contains("bibliography")) {
          heading.hidden = !hasResults;
        }
      });
      var hasVisible = Array.from(section.querySelectorAll("ol.bibliography > li")).some(function (item) {
        return !item.hidden;
      });
      section.hidden = !hasVisible && (selected !== "all" || terms.length > 0);
    });

    buttons.forEach(function (button) {
      var name = button.dataset.publicationFilter;
      button.setAttribute("aria-pressed", String(name === selected));
      var count = button.querySelector(".publication-type-count");
      if (count) count.textContent = String(totals[name] || 0);
    });

    status.textContent = status.dataset.countTemplate
      .replace("%visible%", String(visible)).replace("%total%", String(entries.length));
    empty.hidden = visible !== 0;
    clear.hidden = selected === "all" && terms.length === 0;
  }

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      selected = button.dataset.publicationFilter;
      filterPublications();
    });
  });
  input.addEventListener("input", filterPublications);
  clear.addEventListener("click", function () {
    input.value = "";
    selected = "all";
    filterPublications();
    input.focus();
  });

  filterPublications();
  input.hidden = false;
  filters.hidden = false;
});
