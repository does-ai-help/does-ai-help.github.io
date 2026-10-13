import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';
import http from 'node:http';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const site=path.join(root,'site');
const records=JSON.parse(fs.readFileSync(path.join(root,'data/sources.json'),'utf8'));
const release=JSON.parse(fs.readFileSync(path.join(site,'downloads/release.json'),'utf8'));
const verifiedCount=records.filter(r=>r.verified).length;
const candidateCount=records.filter(r=>r.verification.level==='candidate').length;
const coreCount=records.filter(r=>r.verification.level==='content-checked').length;
const citedCount=release.counts.cited;
const output=path.join(root,'build/qa');fs.mkdirSync(output,{recursive:true});
const server=http.createServer((req,res)=>{
  const requested=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  const file=path.resolve(site,'.'+(requested==='/'?'/index.html':requested));
  if(!file.startsWith(site+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end();return;}
  const mime={'.html':'text/html','.css':'text/css','.js':'text/javascript','.json':'application/json','.png':'image/png','.pdf':'application/pdf','.zip':'application/zip'}[path.extname(file)]||'application/octet-stream';
  res.setHeader('Content-Type',mime);res.end(fs.readFileSync(file));
});
await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
const url=`http://127.0.0.1:${server.address().port}`;
let browser;
try {
  const chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  browser=await chromium.launch({headless:true,...(fs.existsSync(chrome)?{executablePath:chrome}:{})});
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(url+'/');
  assert.equal(await page.locator('h1').innerText(),'Does AI Help?');
  assert.equal(await page.locator('.wordmark').innerText(),release.title);
  for(const route of ['/','/bibliography.html','/releases.html']) {
    await page.goto(url+route);
    assert.equal(await page.locator('a[href*="index.html"]').count(),0);
    assert.equal(await page.locator('.wordmark').getAttribute('href'),'/');
    await page.locator('header nav a').filter({hasText:'Review'}).click();
    assert.equal(page.url(),url+'/');
  }
  const cutoffLabel=new Intl.DateTimeFormat('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(release.cutoff+'T00:00:00Z'));
  assert.equal(await page.locator('.release-detail').innerText().then(t=>t.includes(cutoffLabel)),true);
  assert.equal(await page.locator('.pdf-link').getAttribute('href'),`downloads/does-ai-help-${release.release}.pdf`);
  assert.equal(await page.locator('.byline').innerText().then(t=>t.includes('Witold Bołt, PhD')),true);
  assert.equal(await page.locator('a[href="mailto:Witold.Bolt@jit.team"]').count(),1);
  assert.equal(await page.locator('a[href="https://jit.team"]').count(),1);
  assert.equal(await page.locator('a[href="https://www.linkedin.com/in/witoldbolt/"]').count(),1);
  assert.equal(await page.locator('.community-note').count(),1);
  assert.equal(await page.locator('.reference-list > li').count(),citedCount);
  assert.equal(await page.locator('a[href^="#ref-"]').count()>=citedCount,true);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  await page.screenshot({path:path.join(output,'article-desktop.png')});
  await page.locator('[id="11-an-integrated-assessment-where-the-benefit-survives"]').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'article-figure-desktop.png')});
  await page.goto(url+'/bibliography.html');
  const swe=page.locator('#ref-10b59b402b');
  assert.equal(await swe.locator('.source-meta span').first().innerText(),'2024');
  await swe.locator('details').evaluate(el=>el.open=true);
  assert.match(await swe.innerText(),/2024-08-13/);
  assert.match(await swe.innerText(),/Publisher: OpenAI/);
  assert.match(await swe.innerText(),/Neil Chowdhury/);
  await swe.locator('details').evaluate(el=>el.open=false);
  assert.equal(await page.locator('#ref-3d0ab8c8d6 .source-meta span').first().innerText(),'2025');
  assert.equal(await page.locator('#ref-8ecd8d70a1 a[href="downloads/swebench-recommended.bib"]').count(),1);
  assert.equal(await page.locator('#ref-3e4a5dea3a a[href="downloads/swebench-recommended.bib"]').count(),1);
  const correctedAuthors=JSON.parse(fs.readFileSync(path.join(root,'data/bibliographic-corrections.json'),'utf8'));
  for(const [id,correction] of Object.entries(correctedAuthors).filter(([,c])=>c.authorship_basis)) {
    const row=page.locator('#'+id);
    assert.equal((await row.locator('.source-author').innerText()).includes('Author not established'),false,id);
    await row.locator('details').evaluate(el=>el.open=true);
    assert.equal((await row.innerText()).includes('Authorship basis:'),true,id);
    await row.locator('details').evaluate(el=>el.open=false);
  }
  assert.equal(await page.locator('#mathmisalignment2026 .source-author').innerText(),'Terence Tao et al.');
  for(const [id,year,date] of [['gravityabout2026','2026','2026-09-12'],['gravitypolicy2026','2026','2026-09-15'],['asahipolicy2026','2026','2026-09-08'],['zigpolicy2026','2025','2025-11-22']]) {
    const row=page.locator('#'+id);
    assert.equal(await row.locator('.source-meta span').first().innerText(),year);
    await row.locator('details').evaluate(el=>el.open=true);
    assert.equal((await row.innerText()).includes(date),true);
    assert.equal(await row.locator('a').filter({hasText:'Pinned source revision'}).count(),1);
    await row.locator('details').evaluate(el=>el.open=false);
  }
  assert.match(await page.locator('#ref-a97b44c4bb .source-author').innerText(),/editors/);
  const supplied=page.locator('#ref-47ac0a3015');
  await supplied.locator('details').evaluate(el=>el.open=true);
  assert.match(await supplied.innerText(),/Document inspection: user supplied pdf plus local chrome/);
  assert.match(await supplied.innerText(),/Third-party PDF not redistributed/);
  assert.match(await supplied.innerText(),/2025-03-15/);
  await supplied.locator('details').evaluate(el=>el.open=false);
  await page.locator('#candidate-sciencedirect-2026 details').evaluate(el=>el.open=true);
  assert.equal(await page.locator('#candidate-sciencedirect-2026').innerText().then(t=>t.includes('Alternative verification: Local Chrome')),true);
  await page.locator('#candidate-sciencedirect-2026 details').evaluate(el=>el.open=false);
  await page.waitForFunction(()=>document.querySelector('#result-count').textContent.includes('matching'));
  const initial=await page.locator('.source-row:visible').count();assert.equal(initial,verifiedCount);
  await page.locator('#search').fill('InnovationEval');assert.equal(await page.locator('.source-row:visible').count(),1);
  await page.locator('#search').fill('unlikely-search-no-results');assert.equal(await page.locator('.source-row:visible').count(),0);assert.equal(await page.locator('#empty-state').isVisible(),true);
  await page.locator('button[type=reset]').click();await page.waitForFunction(n=>document.querySelector('#result-count').textContent.startsWith(n+' matching'),verifiedCount);assert.equal(await page.locator('.source-row:visible').count(),verifiedCount);
  await page.locator('#verification').selectOption('candidate');assert.equal(await page.locator('.source-row:visible').count(),candidateCount);
  await page.locator('#verification').selectOption('content-checked');assert.equal(await page.locator('.source-row:visible').count(),coreCount);
  await page.locator('#topic').selectOption('learning');assert.equal(await page.locator('.source-row:visible').count()>0,true);
  const downloadEvent=page.waitForEvent('download');await page.locator('#export-filtered').click();const download=await downloadEvent;assert.equal(download.suggestedFilename(),'bibliography-filtered.csl.json');
  await page.locator('button[type=reset]').click();await page.waitForFunction(n=>document.querySelector('#result-count').textContent.startsWith(n+' matching'),verifiedCount);await page.locator('.source-row:visible').first().locator('summary').click();
  await page.screenshot({path:path.join(output,'bibliography-desktop.png')});
  for(const width of [390,768]) {
    await page.setViewportSize({width,height:844});
    await page.goto(url+'/');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
    await page.screenshot({path:path.join(output,`article-${width}.png`)});
    await page.goto(url+'/bibliography.html');await page.waitForFunction(()=>document.querySelector('#result-count').textContent.includes('matching'));
    const overflow=await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(el=>{const r=el.getBoundingClientRect();return r.width && r.right>innerWidth+1;}).slice(0,8).map(el=>({tag:el.tagName,class:el.className,text:el.textContent.slice(0,100),right:el.getBoundingClientRect().right})));
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,JSON.stringify({width,overflow}));
    await page.screenshot({path:path.join(output,`bibliography-${width}.png`)});
    await page.locator('#search').fill('ref-47ac0a3015');
    await page.locator('#ref-47ac0a3015 details').evaluate(el=>el.open=true);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
    await page.locator('#ref-47ac0a3015').scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(output,`document-record-${width}.png`)});
  }
  for(const name of [`does-ai-help-${release.release}.pdf`,'bibliography.csl.json','bibliography.bib','bibliography.ris','sources.csv','sources.json',release.archive_name || `release-${release.release}.zip`,'related-reviews.md','balance-review.md','document-followup.md','BROWSER-VERIFICATION.md','browser-verification.json','reference-verification.json']) {
    const response=await page.request.get(url+'/downloads/'+name);assert.equal(response.ok(),true,`Download missing: ${name}`);assert.equal((await response.body()).length>0,true);
  }
  await page.goto(url+'/releases.html');assert.equal(await page.locator('h1').innerText(),'Releases & methods');
  await page.goto(pathToFileURL(path.join(site,'bibliography.html')).href);
  await page.waitForFunction(n=>document.querySelector('#result-count').textContent.startsWith(n+' matching'),verifiedCount);
  await page.locator('#search').fill('InnovationEval');assert.equal(await page.locator('.source-row:visible').count(),1);
  assert.deepEqual(errors,[]);
  fs.writeFileSync(path.join(output,'browser-report.json'),JSON.stringify({result:'passed',viewports:[1440,768,390],checks:['article rendering','source filters and reset','empty state','candidate/core counts','filtered CSL download','responsive overflow','all download endpoints','release page','no JavaScript errors']},null,2));
  console.log('Browser checks passed at 1440, 768 and 390 pixels. Screenshots in build/qa.');
} finally {
  if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));
}
