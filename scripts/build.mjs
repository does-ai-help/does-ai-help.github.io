import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';

const require = createRequire(import.meta.url);
const { marked } = await import(pathToFileURL(require.resolve('marked')).href);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
const write = (p, text) => { fs.mkdirSync(path.dirname(path.join(root, p)), {recursive:true}); fs.writeFileSync(path.join(root, p), text); };
const meta = JSON.parse(read('data/release.json'));
const releaseLabel=meta.release_label;
const cutoffLabel=new Intl.DateTimeFormat('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(meta.cutoff+'T00:00:00Z'));
const pdfName=`ai-intellectual-work-${meta.release}.pdf`;
const zipName=`release-${meta.release}.zip`;
const sources = JSON.parse(read('data/sources.json'));
const byId = new Map(sources.map(r => [r.id, r]));
const manuscript = read('manuscript/article.md');
const citations = [...new Set([...manuscript.matchAll(/\[@([^\]]+)\]/g)].flatMap(m => m[1].split(';').map(k => k.trim().replace(/^@/, ''))))];
for (const id of citations) {
  if (!byId.has(id) || byId.get(id).verification.level !== 'content-checked') throw new Error(`Unappraised citation: ${id}`);
}
const numbers = new Map(citations.map((id, i) => [id, i+1]));
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const slug = text => text.toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu, '').replace(/\s+/g, '-');
const citedHtml = text => text.replace(/\[@([^\]]+)\]/g, (_, group) => '<span class="citations">[' + group.split(';').map(k => k.trim().replace(/^@/,'')).map(id => `<a href="#ref-${id}" aria-label="Reference ${numbers.get(id)}" title="${esc(byId.get(id).title)}">${numbers.get(id)}</a>`).join(', ') + ']</span>');
const headingRenderer = {
  heading({tokens, depth, text}) { return `<h${depth} id="${slug(text)}">${this.parser.parseInline(tokens)}</h${depth}>\n`; },
  image({href,text}) { return `<a class="diagram-link" href="${esc(href)}" target="_blank" rel="noopener" title="View full-resolution figure"><img src="${esc(href)}" alt="${esc(text)}"></a>`; }
};
marked.use({renderer: headingRenderer});
const articleHtml = marked.parse(citedHtml(manuscript));
const tokens = marked.lexer(manuscript);
const headings = tokens.filter(t => t.type === 'heading' && t.depth===2 && !['Abstract','Selected references'].includes(t.text));
const authorLabel = (r, compact=true) => r.authors.length ? (compact && r.authors.length>5?r.authors.slice(0,3):r.authors).map(a=>a.includes(', ')?a.split(', ').reverse().join(' '):a).join('; ') + (compact && r.authors.length>5?'; et al.':'') : 'Author not established';
const references = `<ol class="reference-list">${citations.map(id => { const r=byId.get(id); return `<li id="ref-${id}"><a class="reference-title" href="${esc(r.url)}">${esc(r.title)}</a><p>${esc(authorLabel(r))}. ${r.year || 'n.d.'}. ${esc(r.publication_status.replaceAll('-',' '))}.</p>${r.version_note?`<p>${esc(r.version_note)}</p>`:''}<p class="ref-scope">Checked: ${esc(r.verification.basis)}. <a href="bibliography.html#${id}">Evidence record</a></p></li>`; }).join('')}</ol>`;
const verified = sources.filter(r=>r.verified);
const core = sources.filter(r=>r.editorial_priority==='core');
const nav = `<a class="wordmark" href="index.html">AI &amp; Intellectual Work</a><nav aria-label="Main navigation"><a href="index.html">Review</a><a href="bibliography.html">Evidence map</a><a href="releases.html">Releases</a><a href="downloads/${pdfName}" class="pdf-link">Download PDF <span aria-hidden="true">↗</span></a></nav>`;
const head = (title, description) => `<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(title)}</title><meta name="description" content="${esc(description)}"><link rel="stylesheet" href="assets/style.css"><meta name="theme-color" content="#166f59"><meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(description)}">${meta.canonical_url?`<link rel="canonical" href="${esc(meta.canonical_url)}">`:''}`;
const footer = `<footer><span>GPT 6.1 · Witold Bołt</span><span>${esc(releaseLabel)} · CC BY 4.0</span><a href="downloads/CITATION.cff">Cite this release</a><a href="releases.html">Methods &amp; maintenance</a></footer>`;
const contributionLinks = meta.github_url
  ? `<a href="${esc(meta.github_url)}/issues/new/choose">Suggest evidence or a correction</a> · <a href="${esc(meta.github_url)}/pulls">Pull requests</a>`
  : '<a href="downloads/CONTRIBUTING.md">Contribution guide</a> · Public repository address pending';
const downloads = `<div class="downloads" id="downloads"><a href="downloads/${pdfName}">Article PDF</a><a href="downloads/bibliography.csl.json" download>CSL-JSON</a><a href="downloads/bibliography.bib" download>BibTeX</a><a href="downloads/bibliography.ris" download>RIS</a><a href="downloads/sources.csv" download>CSV</a><a href="downloads/sources.json" download>Evidence JSON</a><a href="downloads/${zipName}" download>Release ZIP</a></div>`;
const counts = `<div class="release-counts"><span><strong>${verified.length}</strong> checked reference identities</span><span><strong>${core.length}</strong> annotated sources</span><span><strong>${citations.length}</strong> cited in the article</span></div>`;
const page = (title, body, scripts='') => `<!doctype html><html lang="en"><head>${head(title,meta.subtitle)}</head><body><a href="#main" class="skip-link">Skip to content</a><header>${nav}</header>${body}${footer}${scripts}</body></html>`;
write('site/index.html', page(meta.title+' | October 2026', `<main id="main"><section class="article-heading"><p class="eyebrow">Living critical review · October 2026 release</p><h1>${esc(meta.title)}</h1><p class="subtitle">${esc(meta.subtitle)}</p><p class="byline"><strong>GPT 6.1</strong>, lead AI author &nbsp;·&nbsp; <strong>Witold Bołt</strong>, co-author</p><p class="release-detail">Evidence cutoff: 12 October 2026 · Version ${esc(meta.version)} · Not peer reviewed</p>${downloads}${counts}</section><div class="reading-layout"><aside class="contents"><p>Contents</p><nav aria-label="Article contents">${headings.map(t=>`<a href="#${slug(t.text)}">${esc(t.text)}</a>`).join('')}<a href="#selected-references">Selected references</a></nav></aside><article class="manuscript">${articleHtml}${references}</article></div></main>`, '<script src="assets/article.js" defer></script>'));
const option = (value,label=value)=>`<option value="${esc(value)}">${esc(label.replaceAll('-',' '))}</option>`;
const topicOptions = [...new Set(sources.flatMap(r=>r.topics))].sort();
const methodOptions = [...new Set(sources.map(r=>r.method))].sort();
const yearOptions = [...new Set(sources.map(r=>r.year).filter(Boolean))].sort((a,b)=>b-a);
const recordHtml = r=>`<article class="source-row" id="${r.id}" data-id="${r.id}"><div class="source-meta"><span>${r.year||'n.d.'}</span><span class="status ${r.verification.level==='content-checked'?'checked':''}">${esc(r.verification.level.replaceAll('-',' '))}</span></div><div class="source-body"><h2><a href="${esc(r.url)}">${esc(r.title)}</a></h2><p class="source-author">${esc(authorLabel(r))}</p><p>${esc(r.summary)}</p><p class="source-tags">${esc(r.topics.join(' · '))} &nbsp; / &nbsp; ${esc(r.method.replaceAll('-',' '))}</p><details><summary>Evidence &amp; limitations</summary><p><strong>Publication status:</strong> ${esc(r.publication_status.replaceAll('-',' '))}</p><p><strong>Limitations:</strong> ${esc(r.limitations)}</p><p><strong>Verification:</strong> ${esc(r.verification.basis||'Access or identification incomplete.')} Checked ${esc(r.verification.checked_on||'not established')}.</p>${r.version_note?`<p><strong>Version:</strong> ${esc(r.version_note)}</p>`:''}${r.doi?`<p><strong>DOI:</strong> <a href="https://doi.org/${esc(r.doi)}">${esc(r.doi)}</a></p>`:''}<p><strong>Stable ID:</strong> <code>${r.id}</code></p><button type="button" class="copy-citation" data-id="${r.id}">Copy citation</button></details></div></article>`;
write('site/bibliography.html', page('Evidence map | AI & Intellectual Work', `<main id="main" class="bibliography"><div class="page-intro"><p class="eyebrow">October 2026 · Reference database</p><h1>Evidence map</h1><p class="subtitle">${verified.length} checked identities, ${core.length} annotated sources, and ${sources.length-verified.length} candidates awaiting verification.</p><p class="evidence-note">Content checks record the inspected scope. Identity checks establish a citation, not its findings. Candidates are excluded from citation-manager exports.</p>${downloads}</div><form class="filters" id="filters" role="search"><label class="search-label">Search references<input id="search" type="search" placeholder="Title, author, topic, or finding" autocomplete="off"></label><label>Topic<select id="topic"><option value="">All topics</option>${topicOptions.map(t=>option(t)).join('')}</select></label><label>Method<select id="method"><option value="">All methods</option>${methodOptions.map(t=>option(t)).join('')}</select></label><label>Year<select id="year"><option value="">All years</option>${yearOptions.map(t=>option(t,String(t))).join('')}</select></label><label>Verification<select id="verification"><option value="verified">Checked identities</option><option value="content-checked">Content checked</option><option value="identity-checked">Identity only</option><option value="candidate">Candidates</option><option value="all">All records</option></select></label><label>Sort<select id="sort"><option value="newest">Newest first</option><option value="title">Title A-Z</option></select></label><button type="reset">Reset filters</button></form><div class="results-bar"><p id="result-count" aria-live="polite">${sources.length} records. Filters require JavaScript.</p><button id="export-filtered" type="button">Export results · CSL-JSON</button><a href="downloads/sources.jsonl" download>JSON Lines</a></div><p id="copy-status" class="copy-status" aria-live="polite"></p><section id="source-list" aria-label="Reference results">${sources.map(recordHtml).join('')}</section><p id="empty-state" hidden>No references match these filters.</p><noscript><p>All records are available above and in the downloadable database. Search and filter controls require JavaScript.</p></noscript></main>`, '<script src="assets/bibliography.js" defer></script>'));
write('site/releases.html', page('Releases and methods | AI & Intellectual Work', `<main id="main" class="release-page"><p class="eyebrow">Versioned publication</p><h1>Releases &amp; methods</h1><section><h2>October 2026</h2><p>Version ${esc(meta.version)}. Evidence cutoff: 12 October 2026.</p>${counts}${downloads}<p>Initial English synthesis and searchable evidence map. Corrections include updated authorship and sample scope for Writing Code vs. Shipping Code, the current title of the retail field-experiment paper, and removal of an unrelated inherited catalog link.</p><p><a href="downloads/CHANGELOG.md">Release changelog</a> · <a href="downloads/methodology.md">Methodology</a> · <a href="downloads/exclusions.json">Exclusions</a> · <a href="downloads/checksums.sha256">Checksums</a></p></section><section><h2>Verification levels</h2><dl><dt>Content checked</dt><dd>Inspected source scope is recorded, ranging from an abstract to a full technical report. This is appraisal, not independent replication.</dd><dt>Identity checked</dt><dd>Primary metadata establishes the bibliographic identity. Result-level appraisal remains pending.</dd><dt>Candidate</dt><dd>Retained for follow-up after incomplete access or identification. Excluded from checked-citation exports.</dd></dl></section><section><h2>Monthly update policy</h2><p>Each release preserves its manuscript, database, PDF, exports, cutoff, changelog, and checksums. Link monitoring is automated; substantive inclusion and conclusions require editorial review. New versions will be added to this release history.</p><p><a href="downloads/MAINTENANCE.md">Maintenance procedure</a> · <a href="downloads/source-schema.json">Database schema</a></p></section><section><h2>Contributions</h2>${meta.authors.map(a=>`<p><strong>${esc(a.name)} · ${esc(a.role)}</strong><br>${esc(a.contribution)}</p>`).join('')}<p>AI-authored initial release; not a peer-reviewed publication. Source publications retain their rights. Article text and original annotations are licensed under CC BY 4.0.</p></section></main>`));

const texEscape = text => String(text).replace(/[\\{}%&#_$^~]/g,c=>({'\\':'\\textbackslash{}','{':'\\{','}':'\\}','%':'\\%','&':'\\&','#':'\\#','_':'\\_','$':'\\$','^':'\\textasciicircum{}','~':'\\textasciitilde{}'}[c]));
function texText(text) {
  return text.split(/(\[@[^\]]+\])/g).map(part=>{
    const match = part.match(/^\[@([^\]]+)\]$/);
    if (!match) return texEscape(part);
    return '['+match[1].split(';').map(k=>k.trim().replace(/^@/,'')).map(id=>`\\hyperlink{ref-${id}}{${numbers.get(id)}}`).join(', ')+']';
  }).join('');
}
function inline(tokens) {
  return (tokens||[]).map(t=>{
    if(t.type==='strong') return `\\textbf{${inline(t.tokens)}}`;
    if(t.type==='em') return `\\emph{${inline(t.tokens)}}`;
    if(t.type==='link') { const href=t.href.startsWith('downloads/') && meta.canonical_url ? new URL(t.href,meta.canonical_url).href : t.href.replace(/^downloads\//,''); return `\\href{${texEscape(href)}}{${inline(t.tokens)}}`; }
    if(t.type==='codespan') return `\\texttt{${texEscape(t.text)}}`;
    if(t.type==='br') return '\\newline ';
    if(t.type==='image') return `\n\\begin{figure}[htbp]\\centering\\includegraphics[width=\\textwidth]{../site/${texEscape(t.href)}}\\end{figure}\n`;
    if(t.tokens) return inline(t.tokens);
    return texText(t.text||'');
  }).join('');
}
function blocks(tokens) {
  return tokens.map(t=>{
    if(t.type==='space') return '\n';
    if(t.type==='heading') { const text=texEscape(t.text); const cmd=t.depth<=2?'section':'subsection'; const pageBreak=t.text==='Selected references'?'\\clearpage\n':''; return `${pageBreak}\n\\${cmd}*{${text}}\\phantomsection\\addcontentsline{toc}{${cmd}}{${text}}\n`; }
    if(t.type==='paragraph') return inline(t.tokens)+'\n\n';
    if(t.type==='list') return `\\begin{${t.ordered?'enumerate':'itemize'}}\n`+t.items.map(i=>'\\item '+blocks(i.tokens)).join('\n')+`\\end{${t.ordered?'enumerate':'itemize'}}\n`;
    if(t.type==='text') return (t.tokens?inline(t.tokens):texText(t.text))+'\n';
    if(t.type==='blockquote') return '\\begin{quote}'+blocks(t.tokens)+'\\end{quote}\n';
    if(t.type==='table') {
      const n=t.header.length;
      const cols=Array(n).fill(`>{\\raggedright\\arraybackslash}p{${(0.92/n).toFixed(3)}\\textwidth}`).join('');
      const row = cells=>cells.map(c=>inline(c.tokens)).join(' & ')+' \\\\';
      return `\n{\\footnotesize\\setlength{\\tabcolsep}{3pt}\\renewcommand{\\arraystretch}{1.25}\n\\begin{longtable}{${cols}}\\toprule\n${row(t.header)}\\midrule\\endhead\n${t.rows.map(row).join('\n')}\n\\bottomrule\\end{longtable}}\n`;
    }
    throw new Error(`Unsupported Markdown block: ${t.type}`);
  }).join('');
}
const abstractTokens = tokens.slice(1, tokens.findIndex(t=>t.type==='heading' && t.text.startsWith('1.')));
write('latex/abstract.tex', '\\section*{Abstract}\n'+blocks(abstractTokens));
const bodyTokens = tokens.slice(tokens.findIndex(t=>t.type==='heading' && t.text.startsWith('1.')));
write('latex/release.tex', [['ReviewTitle',meta.title],['ReviewRelease',releaseLabel],['ReviewCutoff',cutoffLabel],['ReviewVersion',meta.version]].map(([name,value])=>`\\newcommand{\\${name}}{${texEscape(value)}}`).join('\n')+'\n');
const texRefs = citations.map(id=>{const r=byId.get(id); return `\\item[${numbers.get(id)}.] \\hypertarget{ref-${id}}{} ${texEscape(authorLabel(r))}. ${r.year||'n.d.'}. \\textit{${texEscape(r.title)}}. ${texEscape(r.publication_status.replaceAll('-',' '))}. ${r.version_note?texEscape(r.version_note)+' ':''}\\url{${texEscape(r.url)}}.`;}).join('\n\n');
write('latex/body.tex', blocks(bodyTokens)+'\n{\\small\\begin{description}[leftmargin=2em,labelwidth=1.5em]\n'+texRefs+'\n\\end{description}}\n');
write('site/downloads/article.md', manuscript);
write('site/downloads/release.json', JSON.stringify({...meta,counts:{total:sources.length,verified:verified.length,core:core.length,cited:citations.length}},null,2)+'\n');
for(const [source, dest] of [['data/source-schema.json','source-schema.json'],['data/exclusions.json','exclusions.json'],['manuscript/methodology.md','methodology.md'],['CHANGELOG.md','CHANGELOG.md'],['MAINTENANCE.md','MAINTENANCE.md'],['CITATION.cff','CITATION.cff']]) fs.copyFileSync(path.join(root,source),path.join(root,'site/downloads',dest));
for (const filename of ['CONTRIBUTING.md', 'LICENSE-CONTENT.md', 'HOSTING.md']) fs.copyFileSync(path.join(root, filename), path.join(root,'site/downloads',filename));
fs.copyFileSync(path.join(root,'manuscript/metadata-review.md'),path.join(root,'site/downloads/metadata-review.md'));
fs.copyFileSync(path.join(root,'manuscript/related-reviews.md'),path.join(root,'site/downloads/related-reviews.md'));
const externalLinks=new Set();
const documentPaths=['README.md','HOSTING.md','CONTRIBUTING.md','MAINTENANCE.md','LICENSE-CONTENT.md','manuscript/article.md','manuscript/methodology.md','manuscript/metadata-review.md','manuscript/related-reviews.md'];
for(const file of documentPaths) marked.walkTokens(marked.lexer(read(file)), token=>{
  if(['link','image'].includes(token.type) && /^https?:\/\//.test(token.href)) externalLinks.add(token.href.split('#')[0]);
});
write('site/downloads/external-links.json',JSON.stringify([...externalLinks].sort(),null,2)+'\n');
if(fs.existsSync(path.join(root,'build/access-report.json'))) fs.copyFileSync(path.join(root,'build/access-report.json'),path.join(root,'site/downloads/access-report.json'));
for (const extension of ['json','csv','md']) {
  const file=path.join(root,`build/reference-verification.${extension}`);
  if(fs.existsSync(file)) fs.copyFileSync(file,path.join(root,`site/downloads/reference-verification.${extension}`));
}
write('site/.nojekyll','');
write('site/assets/data.js','window.REVIEW_DATA='+JSON.stringify({sources,citations:JSON.parse(read('site/downloads/bibliography.csl.json'))})+';\n');
write('site/bibliography.html',read('site/bibliography.html').replace('<script src="assets/bibliography.js" defer></script>','<script src="assets/data.js" defer></script><script src="assets/bibliography.js" defer></script>'));
for(const filename of ['index.html','bibliography.html','releases.html']) {
  const source=read('site/'+filename);
  const canonical=meta.canonical_url?new URL(filename==='index.html'?'':filename,meta.canonical_url).href:'';
  const updated=source
    .replace(`<link rel="canonical" href="${esc(meta.canonical_url)}">`,canonical?`<link rel="canonical" href="${esc(canonical)}"><meta property="og:url" content="${esc(canonical)}">`:'')
    .replace('<strong>Witold Bołt</strong>, co-author','<strong>Witold Bołt, PhD</strong>, co-author')
    .replace('</main>', '<section class="community-note" aria-label="Contribute and reuse"><h2>Contribute evidence</h2><p>'+contributionLinks+'. Suggestions are assessed for monthly releases; corrections are welcome.</p><p>Free reuse with attribution under <a href="https://creativecommons.org/licenses/by/4.0/" rel="license">CC BY 4.0</a>. <a href="downloads/LICENSE-CONTENT.md">Reuse and attribution</a> · <a href="downloads/reference-verification.md">Latest identity audit</a> · <a href="downloads/metadata-review.md">Editorial metadata notes</a></p></section></main>')
    .replace('Living critical review · October 2026 release',`Living critical review · ${esc(releaseLabel)} release`)
    .replaceAll('Evidence cutoff: 12 October 2026',`Evidence cutoff: ${esc(cutoffLabel)}`)
    .replace('October 2026 · Reference database',`${esc(releaseLabel)} · Reference database`)
    .replace('<h2>October 2026</h2>',`<h2>${esc(releaseLabel)}</h2>`)
    .replace(' | October 2026</title>',` | ${esc(releaseLabel)}</title>`);
  write('site/'+filename,updated);
}
write('build/cited-ids.json',JSON.stringify(citations,null,2));
console.log(`Built article and evidence map: ${verified.length} checked identities, ${core.length} core annotations, ${citations.length} cited sources.`);
