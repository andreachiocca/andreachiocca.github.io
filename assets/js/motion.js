// Motion kit: reveal content blocks once as they enter the viewport.
// Progressive enhancement: without this script, or with reduced motion, nothing is hidden.
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;

  // Block-level units that read as one piece of content; nested matches are skipped.
  var selector = [
    '.home-page--editorial > section:not(.home-hero)',
    '.feature-card',
    '.research-area',
    '.research-output',
    '.output-atlas-feature',
    '.publications ol.bibliography > li',
    '.laboratory-equipment > *',
    '.thesis-topic',
    '.cv .card'
  ].join(',');
  var nodes = Array.prototype.filter.call(document.querySelectorAll(selector), function (node) {
    return !node.parentElement.closest(selector);
  });
  if (!nodes.length) return;

  var root = document.documentElement;
  var reveal = function (node) { node.classList.add('is-revealed'); };
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) { reveal(entry.target); observer.unobserve(entry.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

  nodes.forEach(function (node) {
    // Anything already on screen (or above it, e.g. after an anchor jump) is shown immediately.
    if (node.getBoundingClientRect().top < window.innerHeight) reveal(node);
    node.setAttribute('data-reveal', '');
    observer.observe(node);
  });
  root.classList.add('motion-ready');

  // Never leave content hidden for printing or for in-page search and anchors.
  var revealAll = function () { nodes.forEach(reveal); };
  window.addEventListener('beforeprint', revealAll);
  window.addEventListener('hashchange', revealAll);
})();
