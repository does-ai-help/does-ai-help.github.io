async function start() {
  const records=window.REVIEW_DATA.sources;
  const csl=window.REVIEW_DATA.citations;
  const form = document.getElementById('filters');
  const list = document.getElementById('source-list');
  const rows = new Map([...list.children].map(row=>[row.dataset.id,row]));
  const field = id => document.getElementById(id).value;
  let shown = [];
  function render() {
    const query=field('search').trim().toLowerCase(), topic=field('topic'), method=field('method'), year=field('year'), verification=field('verification');
    shown = records.filter(r=>{
      const text=[r.title,r.authors.join(' '),r.summary,r.limitations,r.topics.join(' '),r.id].join(' ').toLowerCase();
      const matchesVerification=verification==='all'||(verification==='verified'?r.verified:r.verification.level===verification);
      return (!query||text.includes(query))&&(!topic||r.topics.includes(topic))&&(!method||r.method===method)&&(!year||String(r.year)===year)&&matchesVerification;
    }).sort((a,b)=>field('sort')==='title'?a.title.localeCompare(b.title):(b.year||0)-(a.year||0)||a.title.localeCompare(b.title));
    rows.forEach(row=>row.hidden=true);
    shown.forEach(r=>{const row=rows.get(r.id);row.hidden=false;list.append(row);});
    document.getElementById('result-count').textContent=`${shown.length} matching references · ${shown.filter(r=>r.editorial_priority==='core').length} annotated`;
    document.getElementById('empty-state').hidden=shown.length>0;
  }
  form.addEventListener('input',render);
  form.addEventListener('change',render);
  form.addEventListener('submit',e=>e.preventDefault());
  form.addEventListener('reset',()=>requestAnimationFrame(render));
  document.getElementById('export-filtered').addEventListener('click',()=>{
    const ids=new Set(shown.filter(r=>r.verified).map(r=>r.id));
    const data=csl.filter(r=>ids.has(r.id));
    const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    const href=URL.createObjectURL(blob);const a=document.createElement('a');a.href=href;a.download='bibliography-filtered.csl.json';a.click();setTimeout(()=>URL.revokeObjectURL(href),1000);
    document.getElementById('copy-status').textContent=`Exported ${data.length} checked citations. Candidate records are excluded.`;
  });
  list.addEventListener('click',async e=>{
    const button=e.target.closest('.copy-citation');if(!button)return;
    const r=records.find(r=>r.id===button.dataset.id);
    const citation=`${r.authors.join('; ')||'Author not established'}. ${r.year||'n.d.'}. ${r.title}. ${r.url}`;
    try{await navigator.clipboard.writeText(citation);document.getElementById('copy-status').textContent='Citation copied.';}
    catch{document.getElementById('copy-status').textContent=citation;}
  });
  if(location.hash){const id=decodeURIComponent(location.hash.slice(1));const r=records.find(r=>r.id===id);if(r){document.getElementById('verification').value='all';document.getElementById('search').value=id;}}
  render();
}
start().catch(error=>{document.getElementById('result-count').textContent=error.message+' Downloadable data remain available.';});
