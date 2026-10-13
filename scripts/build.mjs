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
const humanAffiliation = meta.authors.find(author=>author.name==='Witold Bołt').institution;
const downloadStems={...JSON.parse(read('data/download-names.json')),[`does-ai-help-${meta.release}.pdf`]:'does-ai-help'};
const downloadNames=Object.fromEntries(Object.entries(downloadStems).map(([name,stem])=>[name,`${stem}-${meta.version}${name.slice(name.indexOf('.'))}`]));
const filteredCslName=`${downloadStems['bibliography.csl.json']}-filtered-${meta.version}.csl.json`;
const publicDownloads = html=>html.replace(/href="downloads\/([^"#]+)(#[^"]*)?"/g,(match,name,fragment='')=>downloadNames[name]?`href="downloads/${downloadNames[name]}${fragment}"`:match);
const downloadHref = href=>{
  if(!href.startsWith('downloads/')) return href;
  const url=new URL(href,'https://downloads.invalid/');
  const name=url.pathname.slice('/downloads/'.length);
  return downloadNames[name]?`downloads/${downloadNames[name]}${url.search}${url.hash}`:href;
};
const releaseLabel=meta.release_label;
const cutoffLabel=new Intl.DateTimeFormat('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(meta.cutoff+'T00:00:00Z'));
const pdfName=`does-ai-help-${meta.release}.pdf`;
const zipName=meta.archive_name || `release-${meta.release}.zip`;
const sources = JSON.parse(read('data/sources.json'));
const citationNotes = JSON.parse(read('data/citation-notes.json'));
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
const authorLabel = (r, compact=true) => {
  if(compact && r.author_display) return r.author_display;
  const names = r.authors.length ? r.authors : r.editors || [];
  return names.length ? (compact && names.length>5?names.slice(0,3):names).map(a=>a.includes(', ')?a.split(', ').reverse().join(' '):a).join('; ') + (compact && names.length>5?'; et al.':'') + (!r.authors.length && r.editors?.length?' (editors)':'') : 'Author not established';
};
const authorSentence = r=>{const label=authorLabel(r);return label.endsWith('.')?label:label+'.';};
const references = `<ol class="reference-list">${citations.map(id => { const r=byId.get(id); return `<li id="ref-${id}"><a class="reference-title" href="${esc(r.url)}">${esc(r.title)}</a><p>${esc(authorSentence(r))} ${r.year || 'n.d.'}. ${esc(r.publication_status.replaceAll('-',' '))}.</p>${citationNotes[id]?`<p>${esc(citationNotes[id])}</p>`:''}<p class="ref-scope"><a href="bibliography.html#${id}">Evidence record and reading scope</a></p></li>`; }).join('')}</ol>`;
const verified = sources.filter(r=>r.verified);
const core = sources.filter(r=>r.editorial_priority==='core');
const star = meta.github_url ? `<a class="github-star" href="${esc(meta.github_url)}" target="_blank" rel="noopener" data-repository="${esc(new URL(meta.github_url).pathname.slice(1))}" aria-label="Star Does AI Help? on GitHub" title="View the repository and give it a star on GitHub"><span aria-hidden="true">☆</span> Star <span class="github-star-count" hidden></span></a>` : '';
const githubLink = meta.github_url ? `<a class="github-repository" href="${esc(meta.github_url)}" target="_blank" rel="noopener" title="Browse the source, suggest changes, or fork the repository"><span class="github-icon" aria-hidden="true"></span>Fork me on GitHub</a>` : '';
const nav = `<a class="wordmark" href="/">${esc(meta.title)}</a><nav aria-label="Main navigation"><a href="/">Review</a><a href="bibliography.html">Evidence map</a><a href="releases.html">Releases</a><a href="downloads/${pdfName}" class="pdf-link">Download PDF <span aria-hidden="true">↗</span></a></nav>`;
const head = (title, description) => `<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(title)}</title><meta name="description" content="${esc(description)}"><link rel="stylesheet" href="assets/style.css"><link rel="icon" href="favicon.ico" sizes="16x16 32x32"><link rel="icon" type="image/png" href="assets/favicon-32.png" sizes="32x32"><link rel="icon" type="image/svg+xml" href="favicon.svg" sizes="any"><link rel="apple-touch-icon" href="apple-touch-icon.png" sizes="180x180"><meta name="theme-color" content="#166f59"><meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(description)}">${meta.canonical_url?`<link rel="canonical" href="${esc(meta.canonical_url)}">`:''}`;
const footer = `<footer><span>GPT 6.1 · Witold Bołt</span><span>${esc(releaseLabel)} · CC BY 4.0</span><a href="cite.html">Cite this release</a><a href="releases.html">Methods &amp; maintenance</a></footer>`;
const contributionLinks = meta.github_url
  ? `<a href="${esc(meta.github_url)}/issues/new/choose">Suggest evidence or a correction</a> · <a href="${esc(meta.github_url)}/pulls">Pull requests</a>`
  : '<a href="downloads/CONTRIBUTING.md">Contribution guide</a> · Public repository address pending';
const downloads = `<div class="downloads" id="downloads"><a href="downloads/${pdfName}">Article PDF</a><a href="downloads/bibliography.csl.json" download>CSL-JSON</a><a href="downloads/bibliography.bib" download>BibTeX</a><a href="downloads/bibliography.ris" download>RIS</a><a href="downloads/sources.csv" download>CSV</a><a href="downloads/sources.json" download>Evidence JSON</a><a href="downloads/${zipName}" download>Release ZIP</a></div>`;
const counts = `<div class="release-counts"><span><strong>${verified.length}</strong> checked reference identities</span><span><strong>${core.length}</strong> annotated sources</span><span><strong>${citations.length}</strong> cited in the article</span></div>`;
const page = (title, body, scripts='') => {
  const longPage=Boolean(scripts);
  const pageFooter=longPage?footer.replace('</footer>','<a class="back-to-top-link" href="#page-top">Back to top</a></footer>'):footer;
  const topControl=longPage?'<a class="back-to-top" href="#page-top" aria-label="Back to top" title="Back to top" hidden><span aria-hidden="true">↑</span></a><script src="assets/back-to-top.js" defer></script>':'';
  return `<!doctype html><html lang="en"><head>${head(title,meta.subtitle)}</head><body><a href="#main" class="skip-link">Skip to content</a><header id="page-top" tabindex="-1">${nav.replace('</nav>',githubLink+star+'</nav>')}</header>${body}${pageFooter}${scripts}${topControl}<script src="assets/github-star.js" defer></script></body></html>`;
};
const citationTitle=`${meta.title} ${meta.subtitle}`;
const citationYear=meta.release_date.slice(0,4);
const citationKey=`does-ai-help-${meta.version}`;
const citationNames=meta.authors.map(a=>a.name);
const citationNote=`Living critical narrative review and evidence map; ${releaseLabel} release; version ${meta.version}; lead AI author and human co-author; not peer reviewed.`;
const citationText=`${citationNames.join(' & ')} (${citationYear}). ${citationTitle} (Version ${meta.version}). ${meta.canonical_url}`;
const citationBib=`@misc{${citationKey},\n  author = {${citationNames.map(name=>name==='GPT 6.1'?'{GPT 6.1}':name).join(' and ')}},\n  title = {{${citationTitle}}},\n  year = {${citationYear}},\n  month = {${meta.release_date.slice(5,7)}},\n  version = {${meta.version}},\n  url = {${meta.canonical_url}},\n  note = {${citationNote}}\n}\n`;
const citationCsl={id:citationKey,type:'report',title:citationTitle,author:meta.authors.map(a=>a.name==='Witold Bołt'?{given:'Witold',family:'Bołt'}:{literal:a.name}),issued:{'date-parts':[meta.release_date.split('-').map(Number)]},version:meta.version,URL:meta.canonical_url,note:citationNote};
const citationRis=`TY  - RPRT\n${citationNames.map(name=>`AU  - ${name==='Witold Bołt'?'Bołt, Witold':name}`).join('\n')}\nTI  - ${citationTitle}\nPY  - ${citationYear}\nDA  - ${meta.release_date.replaceAll('-','/')}\nUR  - ${meta.canonical_url}\nN1  - ${citationNote}\nER  - \n`;
write('site/downloads/does-ai-help-citation.bib',citationBib);
write('site/downloads/does-ai-help-citation.csl.json',JSON.stringify([citationCsl],null,2)+'\n');
write('site/downloads/does-ai-help-citation.ris',citationRis);
write('site/cite.html',page('Cite this release | Does AI Help?',`<main id="main" class="release-page citation-page"><p class="eyebrow">${esc(releaseLabel)} · Version ${esc(meta.version)}</p><h1>Cite this release</h1><section><h2>Full reference</h2><p class="citation-example">${esc(citationText)}</p><p><strong>In-text citation:</strong> (${esc(citationNames.join(' & '))}, ${citationYear}).</p><p><strong>Release date:</strong> ${esc(cutoffLabel)}. <strong>Evidence cutoff:</strong> ${esc(cutoffLabel)}.</p><p>${esc(citationNote)}</p>${meta.github_url?`<p><a href="${esc(meta.github_url)}/releases/tag/v${esc(meta.version)}">Permanent versioned release</a></p>`:''}</section><section><h2>BibTeX</h2><pre><code>${esc(citationBib)}</code></pre><a href="downloads/does-ai-help-citation.bib" download>Download BibTeX</a></section><section><h2>Citation formats</h2><div class="downloads"><a href="downloads/does-ai-help-citation.ris" download>RIS</a><a href="downloads/does-ai-help-citation.csl.json" download>CSL-JSON</a><a href="downloads/CITATION.cff" download>Citation File Format</a></div></section><p>Article text and original annotations are licensed under CC BY 4.0. Source publications retain their own rights.</p></main>`));
write('site/index.html', page(meta.title+' | October 2026', `<main id="main"><section class="article-heading"><p class="eyebrow">Living critical review · October 2026 release</p><h1>${esc(meta.title)}</h1><p class="subtitle">${esc(meta.subtitle)}</p><p class="byline"><strong>GPT 6.1</strong>, lead AI author &nbsp;·&nbsp; <strong>Witold Bołt</strong>, co-author</p><p class="release-detail">Evidence cutoff: 13 October 2026 · Version ${esc(meta.version)} · Not peer reviewed</p>${downloads}${counts}</section><div class="reading-layout"><aside class="contents"><p>Contents</p><nav aria-label="Article contents">${headings.map(t=>`<a href="#${slug(t.text)}">${esc(t.text)}</a>`).join('')}<a href="#selected-references">Selected references</a></nav></aside><article class="manuscript">${articleHtml}${references}</article></div></main>`, '<script src="assets/article.js" defer></script>'));
const option = (value,label=value)=>`<option value="${esc(value)}">${esc(label.replaceAll('-',' '))}</option>`;
const topicOptions = [...new Set(sources.flatMap(r=>r.topics))].sort();
const methodOptions = [...new Set(sources.map(r=>r.method))].sort();
const yearOptions = [...new Set(sources.map(r=>r.year).filter(Boolean))].sort((a,b)=>b-a);
const recordHtml = r=>`<article class="source-row" id="${r.id}" data-id="${r.id}"><div class="source-meta"><span>${r.year||'n.d.'}</span><span class="status ${r.verification.level==='content-checked'?'checked':''}">${esc(r.verification.level.replaceAll('-',' '))}</span></div><div class="source-body"><h2><a href="${esc(r.url)}">${esc(r.title)}</a></h2><p class="source-author">${esc(authorLabel(r))}</p><p>${esc(r.summary)}</p><p class="source-tags">${esc(r.topics.join(' · '))} &nbsp; / &nbsp; ${esc(r.method.replaceAll('-',' '))}</p><details><summary>Evidence &amp; limitations</summary><p><strong>Publication status:</strong> ${esc(r.publication_status.replaceAll('-',' '))}</p><p><strong>Limitations:</strong> ${esc(r.limitations)}</p><p><strong>Verification:</strong> ${esc(r.verification.basis||'Access or identification incomplete.')} Checked ${esc(r.verification.checked_on||'not established')}.</p>${r.version_note?`<p><strong>Version:</strong> ${esc(r.version_note)}</p>`:''}${r.doi?`<p><strong>DOI:</strong> <a href="https://doi.org/${esc(r.doi)}">${esc(r.doi)}</a></p>`:''}<p><strong>Stable ID:</strong> <code>${r.id}</code></p><button type="button" class="copy-citation" data-id="${r.id}">Copy citation</button></details></div></article>`;
write('site/bibliography.html', page('Evidence map | Does AI Help?', `<main id="main" class="bibliography"><div class="page-intro"><p class="eyebrow">October 2026 · Reference database</p><h1>Evidence map</h1><p class="subtitle">${verified.length} checked identities, ${core.length} annotated sources, and ${sources.length-verified.length} candidates awaiting verification.</p><p class="evidence-note">Content checks record the inspected scope. Identity checks establish a citation, not its findings. Candidates are excluded from citation-manager exports.</p>${downloads}</div><form class="filters" id="filters" role="search"><label class="search-label">Search references<input id="search" type="search" placeholder="Title, author, topic, or finding" autocomplete="off"></label><label>Topic<select id="topic"><option value="">All topics</option>${topicOptions.map(t=>option(t)).join('')}</select></label><label>Method<select id="method"><option value="">All methods</option>${methodOptions.map(t=>option(t)).join('')}</select></label><label>Year<select id="year"><option value="">All years</option>${yearOptions.map(t=>option(t,String(t))).join('')}</select></label><label>Verification<select id="verification"><option value="verified">Checked identities</option><option value="content-checked">Content checked</option><option value="identity-checked">Identity only</option><option value="candidate">Candidates</option><option value="all">All records</option></select></label><label>Sort<select id="sort"><option value="newest">Newest first</option><option value="title">Title A-Z</option></select></label><button type="reset">Reset filters</button></form><div class="results-bar"><p id="result-count" aria-live="polite">${sources.length} records. Filters require JavaScript.</p><button id="export-filtered" type="button">Export results · CSL-JSON</button><a href="downloads/sources.jsonl" download>JSON Lines</a></div><p id="copy-status" class="copy-status" aria-live="polite"></p><section id="source-list" aria-label="Reference results">${sources.map(recordHtml).join('')}</section><p id="empty-state" hidden>No references match these filters.</p><noscript><p>All records are available above and in the downloadable database. Search and filter controls require JavaScript.</p></noscript></main>`, '<script src="assets/bibliography.js" defer></script>'));
write('site/releases.html', page('Releases and methods | Does AI Help?', `<main id="main" class="release-page"><p class="eyebrow">Versioned publication</p><h1>Releases &amp; methods</h1><section><h2>October 2026</h2><p>Version ${esc(meta.version)}. Evidence cutoff: 13 October 2026.</p>${counts}${downloads}<p>Initial English synthesis and searchable evidence map. Corrections include updated authorship and sample scope for Writing Code vs. Shipping Code, the current title of the retail field-experiment paper, and removal of an unrelated inherited catalog link.</p><p><a href="downloads/CHANGELOG.md">Release changelog</a> · <a href="downloads/methodology.md">Methodology</a> · <a href="downloads/exclusions.json">Exclusions</a> · <a href="downloads/checksums.sha256">Checksums</a></p></section><section><h2>Verification levels</h2><dl><dt>Content checked</dt><dd>Inspected source scope is recorded, ranging from an abstract to a full technical report. This is appraisal, not independent replication.</dd><dt>Identity checked</dt><dd>Primary metadata establishes the bibliographic identity. Result-level appraisal remains pending.</dd><dt>Candidate</dt><dd>Retained for follow-up after incomplete access or identification. Excluded from checked-citation exports.</dd></dl></section><section><h2>Monthly update policy</h2><p>Each release preserves its manuscript, database, PDF, exports, cutoff, changelog, and checksums. Link monitoring is automated; substantive inclusion and conclusions require editorial review. New versions will be added to this release history.</p><p><a href="downloads/MAINTENANCE.md">Maintenance procedure</a> · <a href="downloads/source-schema.json">Database schema</a></p></section><section><h2>Contributions</h2>${meta.authors.map(a=>`<p><strong>${esc(a.name)} · ${esc(a.role)}</strong><br>${esc(a.contribution)}</p>`).join('')}<p>AI-authored initial release; not a peer-reviewed publication. Source publications retain their rights. Article text and original annotations are licensed under CC BY 4.0.</p></section></main>`));

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
    if(t.type==='link') { const target=downloadHref(t.href); const href=target.startsWith('downloads/') && meta.canonical_url ? new URL(target,meta.canonical_url).href : target.replace(/^downloads\//,''); return t.text===t.href && /^https?:\/\//.test(href) ? `\\url{${texEscape(href)}}` : `\\href{${texEscape(href)}}{${inline(t.tokens)}}`; }
    if(t.type==='codespan') return `\\texttt{${texEscape(t.text)}}`;
    if(t.type==='br') return '\\newline ';
    if(t.type==='image') return `\n\\begin{figure}[htbp]\\centering\\includegraphics[width=\\textwidth]{../site/${texEscape(t.href)}}\\end{figure}\n`;
    if(t.tokens) return inline(t.tokens);
    return (t.text||'').split(/\b([a-f0-9]{40}|[a-f0-9]{64})\b/g).map((part,index)=>index%2?`\\nolinkurl{${part}}`:texText(part)).join('');
  }).join('');
}
function blocks(tokens) {
  return tokens.map(t=>{
    if(t.type==='space') return '\n';
    if(t.type==='heading') { const text=texEscape(t.text); const cmd=t.depth<=2?'section':'subsection'; return `\n\\${cmd}*{${text}}\\phantomsection\\addcontentsline{toc}{${cmd}}{${text}}\n`; }
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
write('latex/release.tex', [['ReviewTitle',meta.title],['ReviewRelease',releaseLabel],['ReviewCutoff',cutoffLabel],['ReviewVersion',meta.version],['ReviewHumanAffiliation',humanAffiliation]].map(([name,value])=>`\\newcommand{\\${name}}{${texEscape(value)}}`).join('\n')+'\n');
const texRefs = citations.map(id=>{const r=byId.get(id); return `\\item[${numbers.get(id)}.] \\hypertarget{ref-${id}}{} ${texEscape(authorSentence(r))} ${r.year||'n.d.'}. \\textit{${texEscape(r.title)}}. ${texEscape(r.publication_status.replaceAll('-',' '))}. ${citationNotes[id]?texEscape(citationNotes[id])+' ':''}\\url{${texEscape(r.url)}}.`;}).join('\n\n');
write('latex/body.tex', blocks(bodyTokens)+'\n{\\small\\setlength{\\parskip}{0pt}\\begin{description}[leftmargin=2em,labelwidth=1.5em,itemsep=1pt,parsep=0pt]\n'+texRefs+'\n\\end{description}}\n');
write('site/downloads/article.md', manuscript);
write('site/downloads/release.json', JSON.stringify({...meta,counts:{total:sources.length,verified:verified.length,core:core.length,cited:citations.length}},null,2)+'\n');
for(const [source, dest] of [['data/source-schema.json','source-schema.json'],['data/exclusions.json','exclusions.json'],['manuscript/methodology.md','methodology.md'],['CHANGELOG.md','CHANGELOG.md'],['MAINTENANCE.md','MAINTENANCE.md'],['CITATION.cff','CITATION.cff']]) fs.copyFileSync(path.join(root,source),path.join(root,'site/downloads',dest));
for (const filename of ['CONTRIBUTING.md', 'LICENSE-CONTENT.md', 'HOSTING.md']) fs.copyFileSync(path.join(root, filename), path.join(root,'site/downloads',filename));
fs.copyFileSync(path.join(root,'manuscript/metadata-review.md'),path.join(root,'site/downloads/metadata-review.md'));
fs.copyFileSync(path.join(root,'manuscript/document-followup.md'),path.join(root,'site/downloads/document-followup.md'));
fs.copyFileSync(path.join(root,'data/swebench-recommended.bib'),path.join(root,'site/downloads/swebench-recommended.bib'));
fs.copyFileSync(path.join(root,'manuscript/related-reviews.md'),path.join(root,'site/downloads/related-reviews.md'));
fs.copyFileSync(path.join(root,'manuscript/balance-review.md'),path.join(root,'site/downloads/balance-review.md'));
fs.copyFileSync(path.join(root,'manuscript/october-final-review.md'),path.join(root,'site/downloads/october-final-review.md'));
fs.copyFileSync(path.join(root,'manuscript/kpmg-q3-2026.md'),path.join(root,'site/downloads/kpmg-q3-2026.md'));
for(const [from,to] of [['data/browser-verification.json','browser-verification.json'],['data/browser-review-policy.json','browser-review-policy.json'],['BROWSER-VERIFICATION.md','BROWSER-VERIFICATION.md']]) fs.copyFileSync(path.join(root,from),path.join(root,'site/downloads',to));
const externalLinks=new Set();
const documentPaths=['README.md','HOSTING.md','CONTRIBUTING.md','MAINTENANCE.md','LICENSE-CONTENT.md','manuscript/article.md','manuscript/methodology.md','manuscript/metadata-review.md','manuscript/document-followup.md','manuscript/related-reviews.md','manuscript/balance-review.md'];
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
write('site/assets/data.js','window.REVIEW_DATA='+JSON.stringify({sources,citations:JSON.parse(read('site/downloads/bibliography.csl.json')),releaseVersion:meta.version,filteredCslName})+';\n');
write('site/bibliography.html',read('site/bibliography.html').replace('<script src="assets/bibliography.js" defer></script>',`<script src="assets/data.js?v=${esc(meta.version)}" defer></script><script src="assets/bibliography.js?v=${esc(meta.version)}" defer></script>`));
for(const filename of ['index.html','bibliography.html','releases.html','cite.html']) {
  let source=read('site/'+filename);
  if(filename==='bibliography.html') for(const r of sources) {
    const stable=`<p><strong>Stable ID:</strong> <code>${r.id}</code></p>`;
    const dateLabel=r.date_kind==='git-file-revision'?'Document revision date':'Publication date';
    const dating=`<p><strong>${dateLabel}:</strong> ${esc(r.date || r.year || 'Not established')}.</p><p><strong>Date basis:</strong> ${esc(r.date_basis || 'Not established')}.</p>`;
    const publisher=r.publisher?`<p><strong>Publisher:</strong> ${esc(r.publisher)}.</p>`:'';
    source=source.replace(stable,stable+dating+publisher);
    if(r.id==='kpmgpulseq32026') source=source.replace(stable,stable+'<p><a href="downloads/kpmg-q3-2026.md">Detailed KPMG Q3 appraisal and reported figures</a></p>');
    if(r.authorship_basis) source=source.replace(stable,stable+`<p><strong>Authorship basis:</strong> ${esc(r.authorship_basis)}</p>${r.author_note?`<p><strong>Attribution note:</strong> ${esc(r.author_note)}</p>`:''}`);
    if(r.author_display) source=source.replace(stable,stable+`<p><strong>Registered creators:</strong> ${esc(authorLabel(r,false))}.</p>`);
    if(r.source_revision) {
      const revision=r.source_revision;
      source=source.replace(stable,stable+`<p><strong>Repository provenance:</strong> <a href="${esc(revision.file_url)}">Pinned source revision</a> · <a href="${esc(revision.history_url)}">File history metadata</a>.</p><p><strong>Date type:</strong> ${esc(r.date_kind.replaceAll('-',' '))}. Authored: ${esc(revision.authored_at)}. Committed: ${esc(revision.committed_at)}.</p>`);
    }
    if(['ref-8ecd8d70a1','ref-3e4a5dea3a'].includes(r.id)) source=source.replace(stable,stable+'<p><a href="downloads/swebench-recommended.bib" download>Download authors\' recommended SWE-bench citations</a>. Conference citations are separate from repository and preprint dates.</p>');
    if(r.document_verification) {
      const d=r.document_verification;
      source=source.replace(stable,stable+`<p><strong>Document inspection:</strong> ${esc(d.method.replaceAll('-',' '))}, ${esc(d.checked_on)}; ${esc(d.pages)} pages. Artifact: ${esc(d.filename)}.</p><p><strong>Reading scope:</strong> ${esc(d.scope)}. Third-party PDF not redistributed. <a href="downloads/document-followup.md">Document follow-up and provenance</a>.</p>`);
    }
  }
  if(filename==='bibliography.html') for(const r of sources.filter(r=>r.browser_verification)) {
    const b=r.browser_verification;
    const stable=`<p><strong>Stable ID:</strong> <code>${r.id}</code></p>`;
    source=source.replace(stable,stable+`<p><strong>Alternative verification:</strong> Local Chrome, ${esc(b.checked_at.slice(0,10))}; ${esc(b.outcome.replaceAll('-',' '))}. Reviewer: ${esc(b.reviewer)}.</p><p><strong>Browser reading scope:</strong> ${esc(b.scope)}</p><p>${esc(b.notes)} <a href="downloads/browser-verification.json">Browser verification ledger</a></p>`);
  }
  const canonical=meta.canonical_url?new URL(filename==='index.html'?'':filename,meta.canonical_url).href:'';
  const updated=source
    .replace('Initial English synthesis and searchable evidence map. Corrections include updated authorship and sample scope for Writing Code vs. Shipping Code, the current title of the retail field-experiment paper, and removal of an unrelated inherited catalog link.','Initial October 2026 publication: a critical synthesis and searchable evidence map covering productivity, learning, engineering, scientific discovery and community perspectives. Technical version history is preserved in the release changelog; monthly literature updates begin with the next release.')
    .replace(`<link rel="canonical" href="${esc(meta.canonical_url)}">`,canonical?`<link rel="canonical" href="${esc(canonical)}"><meta property="og:url" content="${esc(canonical)}">`:'')
    .replace('<strong>Witold Bołt</strong>, co-author',`<strong>Witold Bołt, PhD</strong>, co-author <span class="author-affiliation">· ${esc(humanAffiliation)}</span>`)
    .replace('</main>', '<section class="community-note" aria-label="Contribute and reuse"><h2>Contribute evidence</h2><p>'+contributionLinks+'. Suggestions are assessed for monthly releases; corrections are welcome.</p><p>Free reuse with attribution under <a href="https://creativecommons.org/licenses/by/4.0/" rel="license">CC BY 4.0</a>. <a href="downloads/LICENSE-CONTENT.md">Reuse and attribution</a> · <a href="downloads/reference-verification.md">Latest identity audit</a> · <a href="downloads/metadata-review.md">Editorial metadata notes</a></p></section></main>')
    .replace('Living critical review · October 2026 release',`Living critical review · ${meta.release_status==='final'?'Final ':''}${esc(releaseLabel)} release`)
    .replaceAll('Evidence cutoff: 13 October 2026',`Evidence cutoff: ${esc(cutoffLabel)}`)
    .replace('October 2026 · Reference database',`${esc(releaseLabel)} · Reference database`)
    .replace('<h2>October 2026</h2>',`<h2>${esc(releaseLabel)}</h2>`)
    .replace(' | October 2026</title>',` | ${esc(releaseLabel)}</title>`);
  write('site/'+filename,publicDownloads(updated));
}
write('site/downloads/download-files.json',JSON.stringify({version:meta.version,files:downloadNames,filtered_csl:filteredCslName},null,2)+'\n');
for(const [original,versioned] of Object.entries(downloadNames)) {
  const file=path.join(root,'site/downloads',original);
  if(fs.existsSync(file)) fs.copyFileSync(file,path.join(root,'site/downloads',versioned));
}
write('build/cited-ids.json',JSON.stringify(citations,null,2));
console.log(`Built article and evidence map: ${verified.length} checked identities, ${core.length} core annotations, ${citations.length} cited sources.`);
