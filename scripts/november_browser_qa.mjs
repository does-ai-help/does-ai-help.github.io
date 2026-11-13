import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=path.join(root,'build/november-qa');
fs.mkdirSync(output,{recursive:true});
const prefix='/preview/november/';
const records=JSON.parse(fs.readFileSync(path.join(root,'preview/november/downloads/sources.json')));
const release=JSON.parse(fs.readFileSync(path.join(root,'preview/november/downloads/release.json')));
const server=http.createServer((req,res)=>{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  const base=pathname.startsWith(prefix)?path.join(root,'preview/november'):path.join(root,'site');
  const relative=pathname.startsWith(prefix)?pathname.slice(prefix.length):pathname.slice(1);
  const file=path.resolve(base,relative.endsWith('/')||!relative?relative+'index.html':relative);
  if(!file.startsWith(base+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){
    res.writeHead(404);res.end();return;
  }
  const mime={'.html':'text/html','.css':'text/css','.js':'text/javascript','.pdf':'application/pdf','.png':'image/png','.svg':'image/svg+xml','.ico':'image/x-icon','.json':'application/json'}[path.extname(file)]||'application/octet-stream';
  res.setHeader('Content-Type',mime);res.end(fs.readFileSync(file));
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const origin=`http://127.0.0.1:${server.address().port}`;
let browser;
try {
  const chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  browser=await chromium.launch({headless:true,...(fs.existsSync(chrome)?{executablePath:chrome}:{})});
  const page=await browser.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('https://api.github.com/repos/does-ai-help/does-ai-help.github.io',route=>route.fulfill({json:{stargazers_count:42}}));
  for(const width of [1440,768,390]){
    await page.setViewportSize({width,height:1000});
    for(const route of ['', 'bibliography.html','cite.html','releases.html','updates.html','release-notes.html']){
      await page.goto(origin+prefix+route);
      assert.equal(await page.locator('.draft-notice').isVisible(),true);
      assert.equal(await page.locator('meta[name="robots"]').getAttribute('content'),'noindex,follow');
      assert.equal(await page.locator('.wordmark').getAttribute('href'),prefix);
      assert.equal(await page.locator('a[href*="index.html"]').count(),0);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`${route} overflows at ${width}`);
      await page.screenshot({path:path.join(output,`${route.replace('.html','')||'article'}-${width}.png`)});
    }
  }
  await page.setViewportSize({width:1440,height:1000});
  await page.goto(origin+prefix);
  const citation=page.locator('.citations a').first();
  const referenceId=await citation.getAttribute('data-reference-id');
  const source=records.find(record=>record.id===referenceId);
  await citation.hover();
  const tooltip=page.getByRole('tooltip');
  await tooltip.waitFor({state:'visible'});
  assert.equal(await tooltip.locator('h2').innerText(),source.title);
  assert.equal(await tooltip.locator('.reference-preview-summary').innerText(),source.summary);
  assert.ok((await tooltip.innerText()).includes(source.limitations));
  assert.ok((await tooltip.locator('.reference-preview-meta').innerText()).includes(String(source.year)));
  assert.equal(await citation.getAttribute('title'),null);
  assert.equal(await citation.getAttribute('aria-describedby'),'reference-preview');
  const tipBox=await tooltip.boundingBox();
  assert.ok(tipBox.x>=0 && tipBox.y>=0 && tipBox.x+tipBox.width<=1440 && tipBox.y+tipBox.height<=1000);
  await tooltip.hover();
  assert.equal(await tooltip.isVisible(),true);
  await page.screenshot({path:path.join(output,'reference-preview-desktop.png')});
  await page.keyboard.press('Escape');
  assert.equal(await tooltip.isVisible(),false);
  assert.equal(await citation.getAttribute('aria-describedby'),null);
  await citation.focus();
  await tooltip.waitFor({state:'visible'});
  await page.keyboard.press('Escape');
  assert.equal(await tooltip.isVisible(),false);
  const touchContext=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  const touchPage=await touchContext.newPage();
  await touchPage.goto(origin+prefix);
  const touchCitation=touchPage.locator('.citations a').first();
  const hash=await touchCitation.getAttribute('href');
  assert.ok(await touchCitation.getAttribute('title'));
  await touchCitation.tap();
  assert.equal(new URL(touchPage.url()).hash,hash);
  assert.equal(await touchPage.locator('#reference-preview').isVisible(),false);
  await touchContext.close();
  await page.goto(origin+prefix);
  await page.getByRole('link',{name:'November release notes',exact:true}).click();
  assert.equal(page.url(),origin+prefix+'release-notes.html');
  assert.equal(await page.locator('h1').innerText(),'November 2026 Release Notes');
  assert.equal(await page.getByRole('navigation',{name:'Release notes contents'}).getByRole('link').count(),13);
  await page.getByRole('navigation',{name:'Release notes contents'}).getByRole('link',{name:'2. Security Discovery Becomes an Operational Question',exact:true}).click();
  assert.equal(new URL(page.url()).hash,'#2-security-discovery-becomes-an-operational-question');
  assert.equal(await page.getByRole('link',{name:'Download release notes as Markdown'}).getAttribute('href'),`downloads/does-ai-help-release-notes-${release.version}.md`);
  assert.equal(await page.locator('.back-to-top-link').count(),1);
  await page.goto(origin+prefix+'updates.html');
  assert.equal(await page.getByRole('link',{name:'November release notes',exact:true}).getAttribute('href'),'release-notes.html');
  await page.goto(origin+prefix);
  await page.getByRole('link',{name:'November update summary',exact:true}).click();
  assert.equal(page.url(),origin+prefix+'updates.html');
  assert.equal(await page.locator('h1').innerText(),'November 2026 Preview: Evidence Update');
  assert.equal(await page.locator('main table thead th').count(),3);
  assert.equal(await page.locator('main table tbody tr').count(),6);
  assert.equal(await page.getByRole('link',{name:'Download Markdown source'}).getAttribute('href'),'downloads/november-update-summary.md');
  assert.equal(await page.getByRole('link',{name:"What's new",exact:true}).getAttribute('href'),'updates.html');
  assert.equal(await page.locator('.back-to-top-link').count(),1);
  await page.goto(origin+prefix+'bibliography.html');
  await page.waitForFunction(()=>Boolean(window.REVIEW_DATA));
  assert.equal(await page.locator('.source-row').count(),records.length);
  await page.locator('#search').fill('roylecisco2026');
  assert.equal(await page.locator('.source-row:visible').count(),1);
  await page.locator('#search').fill('');
  await page.locator('#topic').selectOption('mathematics');
  assert.ok(await page.locator('.source-row:visible').count()>2);
  await page.locator('button[type="reset"]').click();
  await page.locator('#search').fill('ref-712e3405f2');
  const row=page.locator('#ref-712e3405f2');
  await row.locator('summary').click();
  assert.equal(await row.locator('a[href="https://doi.org/10.1145/3706598.3713778"]').count(),1);
  const accessPolicy=JSON.parse(fs.readFileSync(path.join(root,'november/access-deferrals.json')));
  for(const decision of accessPolicy.records){
    await page.locator('#search').fill(decision.id);
    const deferredRow=page.locator('#'+decision.id);
    assert.equal(await deferredRow.isVisible(),true);
    assert.equal(await deferredRow.locator('.status').innerText(),'Currently unverified');
    assert.ok((await deferredRow.locator('.access-deferral').innerText()).includes('Currently unverified for November'));
  }
  const policyResponse=await page.request.get(origin+prefix+`downloads/does-ai-help-access-deferrals-${release.version}.json`);
  assert.equal(policyResponse.ok(),true);
  assert.equal((await policyResponse.json()).records.length,4);
  await page.screenshot({path:path.join(output,'access-deferral-desktop.png')});
  await page.goto(origin+prefix+'cite.html');
  assert.ok((await page.locator('.citation-example').innerText()).includes(release.version));
  assert.equal(await page.getByRole('link',{name:'Permanent versioned release'}).count(),0);
  const downloads=JSON.parse(fs.readFileSync(path.join(root,'preview/november/downloads/download-files.json'))).files;
  for(const name of ['bibliography.bib','bibliography.ris','bibliography.csl.json','sources.csv','sources.json','does-ai-help-2026-11.pdf']){
    const response=await page.request.get(origin+prefix+'downloads/'+downloads[name]);
    assert.equal(response.ok(),true,name);
    assert.ok((await response.body()).length>0,name);
  }
  await page.goto(origin+prefix);
  await page.locator('.draft-notice a').click();
  assert.equal(page.url(),origin+'/');
  assert.ok((await page.locator('.release-detail').innerText()).includes('2026.10.15'));
  assert.deepEqual(errors,[]);
  fs.writeFileSync(path.join(output,'report.json'),JSON.stringify({result:'passed',records:records.length,viewports:[1440,768,390],checks:['draft labels','navigation','rendered update summary','detailed release notes and contents links','desktop citation context','hover persistence','keyboard focus and Escape','tooltip screen bounds','unchanged touch reference navigation','no horizontal overflow','filters','existing-source DOI','downloads','October return link','no page errors']},null,2)+'\n');
  console.log('November preview browser checks passed; screenshots in build/november-qa.');
} catch (error) {
  const page=browser?.contexts()[0]?.pages()[0];
  if(page) {
    await page.screenshot({path:path.join(output,'failure.png')});
    console.error(await page.evaluate(()=>({desktop:matchMedia('(hover: hover) and (pointer: fine) and (min-width: 721px)').matches,tooltip:document.getElementById('reference-preview')?.outerHTML,active:document.activeElement?.outerHTML})));
  }
  throw error;
} finally {
  if(browser) await browser.close();
  await new Promise(resolve=>server.close(resolve));
}
