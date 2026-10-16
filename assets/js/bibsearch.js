document.addEventListener("DOMContentLoaded", function () {
  var input = document.getElementById("bibsearch");
  var list = document.getElementById("publication-list");
  var status = document.getElementById("bibsearch-status");
  if (!input || !list || !status) return;

  var entries = Array.from(list.querySelectorAll("ol.bibliography > li"));
  var searchText = entries.map(function (entry) {
    var year = entry.parentElement.previousElementSibling;
    return (entry.textContent + " " + (year ? year.textContent : "")).toLocaleLowerCase();
  });
  function filter() {
    var terms = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    var visible = 0;
    entries.forEach(function (entry, index) {
      entry.hidden = !terms.every(function (term) { return searchText[index].includes(term); });
      if (!entry.hidden) visible++;
    });
    list.querySelectorAll("ol.bibliography").forEach(function (group) {
      var empty = !Array.from(group.children).some(function (entry) { return !entry.hidden; });
      group.hidden = empty;
      var heading = group.previousElementSibling;
      if (heading && /^H[1-6]$/.test(heading.tagName)) heading.hidden = empty;
    });
    status.textContent = status.dataset.countTemplate.replace('%visible%', visible).replace('%total%', entries.length);
  }
  input.hidden = false;
  input.addEventListener("input", filter);
  filter();
});
