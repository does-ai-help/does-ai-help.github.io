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
    for(const route of ['', 'bibliography.html','cite.html','releases.html']){
      await page.goto(origin+prefix+route);
      assert.equal(await page.locator('.draft-notice').isVisible(),true);
      assert.equal(await page.locator('meta[name="robots"]').getAttribute('content'),'noindex,follow');
      assert.equal(await page.locator('.wordmark').getAttribute('href'),prefix);
      assert.equal(await page.locator('a[href*="index.html"]').count(),0);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`${route} overflows at ${width}`);
      await page.screenshot({path:path.join(output,`${route.replace('.html','')||'article'}-${width}.png`)});
    }
  }
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
  await page.goto(origin+prefix+'cite.html');
  assert.ok((await page.locator('.citation-example').innerText()).includes('2026.11.0-preview.1'));
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
  fs.writeFileSync(path.join(output,'report.json'),JSON.stringify({result:'passed',records:records.length,viewports:[1440,768,390],checks:['draft labels','navigation','no horizontal overflow','filters','existing-source DOI','downloads','October return link','no page errors']},null,2)+'\n');
  console.log('November preview browser checks passed; screenshots in build/november-qa.');
} finally {
  if(browser) await browser.close();
  await new Promise(resolve=>server.close(resolve));
}
