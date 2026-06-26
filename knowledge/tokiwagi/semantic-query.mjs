#!/usr/bin/env node
/**
 * Semantic Memory Query — tokiwagi knowledge graph
 * Usage:
 *   node semantic-query.mjs "<keyword>"
 *   node semantic-query.mjs "<keyword>" --layer "API Routes"
 *   node semantic-query.mjs "<keyword>" --tag "auth"
 *   node semantic-query.mjs --layer "API Routes" --limit 20
 *   node semantic-query.mjs --imports "src/services/gmo.service.ts"
 *   node semantic-query.mjs --dependents "src/libs/middleware/checkAuth.ts"
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const GRAPH_PATH = path.join(__dirname, 'knowledge-graph.json');

const args = process.argv.slice(2);
function getArg(flag) { const i = args.indexOf(flag); return i !== -1 ? args[i+1] : undefined; }
const flagValues = new Set(['--layer','--tag','--imports','--dependents','--limit'].map(f => getArg(f)).filter(Boolean));
const keyword = args.find(a => !a.startsWith('--') && !flagValues.has(a));
const layerFilter = getArg('--layer');
const tagFilter = getArg('--tag');
const importsOf = getArg('--imports');
const dependentsOf = getArg('--dependents');
const limit = parseInt(getArg('--limit')) || 15;
const json = args.includes('--json');

const graph = JSON.parse(fs.readFileSync(GRAPH_PATH, 'utf8'));
const fileLevelTypes = new Set(['file','config','document','service','pipeline','table','schema','resource','endpoint']);
const nodeMap = {};
graph.nodes.forEach(n => nodeMap[n.id] = n);

// Build path → node map
const pathMap = {};
graph.nodes.forEach(n => { if (n.filePath) pathMap[n.filePath] = n; });

// Build layer → nodeIds map
const layerNodes = {};
graph.layers.forEach(l => { layerNodes[l.name] = new Set(l.nodeIds); });

// --imports: what does this file import?
if (importsOf) {
  const node = pathMap[importsOf];
  if (!node) { console.log('File not found:', importsOf); process.exit(1); }
  const imports = graph.edges
    .filter(e => e.source === node.id && e.type === 'imports')
    .map(e => nodeMap[e.target]?.filePath).filter(Boolean);
  output({ query: `imports of ${importsOf}`, results: imports.map(p => ({ path: p, summary: pathMap[p]?.summary || '' })) });
  process.exit(0);
}

// --dependents: who imports this file?
if (dependentsOf) {
  const node = pathMap[dependentsOf];
  if (!node) { console.log('File not found:', dependentsOf); process.exit(1); }
  const dependents = graph.edges
    .filter(e => e.target === node.id && e.type === 'imports')
    .map(e => nodeMap[e.source]?.filePath).filter(Boolean);
  output({ query: `dependents of ${dependentsOf}`, results: dependents.map(p => ({ path: p, summary: pathMap[p]?.summary || '' })) });
  process.exit(0);
}

// Keyword + filter search
const kw = keyword?.toLowerCase() || '';
const fileNodes = graph.nodes.filter(n => fileLevelTypes.has(n.type));

let candidates = fileNodes;

// Apply layer filter
if (layerFilter) {
  const matchedLayer = graph.layers.find(l => l.name.toLowerCase().includes(layerFilter.toLowerCase()));
  if (matchedLayer) {
    const ids = new Set(matchedLayer.nodeIds);
    candidates = candidates.filter(n => ids.has(n.id));
  }
}

// Apply tag filter
if (tagFilter) {
  candidates = candidates.filter(n => (n.tags||[]).some(t => t.toLowerCase().includes(tagFilter.toLowerCase())));
}

// Score by keyword
function score(node) {
  if (!kw) return 1;
  let s = 0;
  const fp = (node.filePath||'').toLowerCase();
  const sum = (node.summary||'').toLowerCase();
  const tags = (node.tags||[]).join(' ').toLowerCase();
  if (fp.includes(kw)) s += 3;
  if (path.basename(fp).includes(kw)) s += 2;
  if (sum.includes(kw)) s += 2;
  if (tags.includes(kw)) s += 1;
  return s;
}

const results = candidates
  .map(n => ({ node: n, score: score(n) }))
  .filter(r => !kw || r.score > 0)
  .sort((a, b) => b.score - a.score)
  .slice(0, limit)
  .map(r => ({
    path: r.node.filePath,
    type: r.node.type,
    summary: r.node.summary,
    tags: r.node.tags,
    complexity: r.node.complexity,
    score: r.score
  }));

output({
  query: [keyword, layerFilter && `layer:${layerFilter}`, tagFilter && `tag:${tagFilter}`].filter(Boolean).join(' '),
  totalCandidates: candidates.length,
  returned: results.length,
  results
});

function output(data) {
  if (json) {
    console.log(JSON.stringify(data, null, 2));
    return;
  }
  console.log(`\n🔍 Query: "${data.query}" — ${data.returned ?? data.results.length} results\n`);
  data.results.forEach((r, i) => {
    console.log(`${i+1}. ${r.path}`);
    if (r.summary) console.log(`   ${r.summary}`);
    if (r.tags?.length) console.log(`   tags: ${r.tags.join(', ')}`);
    if (r.complexity) console.log(`   complexity: ${r.complexity}`);
    console.log();
  });
}
