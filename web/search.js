(function (root) {
  'use strict';
  function normalize(value) {
    return String(value).toLowerCase().replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, ' ').trim();
  }
  function score(entry, query) {
    const q = normalize(query);
    if (!q) return 1;
    const needles = [entry.error, ...entry.aliases].map(normalize);
    if (needles.some(n => q === n)) return 100;
    if (needles.some(n => n.length >= 8 && q.includes(n))) return 90;
    if (needles.some(n => n.includes(q))) return 80;
    const corpus = normalize(JSON.stringify(entry));
    if (corpus.includes(q)) return 50;
    return q.split(' ').every(w => corpus.includes(w)) ? 20 : 0;
  }
  function search(entries, query, category = 'all') {
    return entries.filter(e => category === 'all' || e.category === category)
      .map(entry => ({ entry, score: score(entry, query) })).filter(x => x.score > 0)
      .sort((a, b) => b.score - a.score || a.entry.id.localeCompare(b.entry.id)).map(x => x.entry);
  }
  const api = { normalize, score, search };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.ErrorAtlasSearch = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
