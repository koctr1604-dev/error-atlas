// Optional: requires Playwright + Chromium. The core project has no npm dependency.
const {chromium} = require('playwright');
const {pathToFileURL} = require('node:url');
const path = require('node:path');
const assert = require('node:assert/strict');
const fs = require('node:fs');
(async()=>{
  const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
  try {
    const page=await browser.newPage({viewport:{width:1440,height:1050}});
    const errors=[];const network=[];
    page.on('pageerror',e=>errors.push(String(e)));
    page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url());});
    const url=pathToFileURL(path.resolve(__dirname,'../docs/index.html')).href;
    await page.goto(url);
    const total=Number(await page.locator('#total-count').textContent());
    assert(total>0);assert.equal(await page.locator('.card').count(),total);
    await page.locator('#query').fill('eresolve');
    assert(await page.locator('.card').count()>0);
    await page.locator('.open-entry').first().click();
    assert(await page.locator('#detail').evaluate(e=>e.open));
    assert((await page.locator('#detail-content').textContent()).includes('官方依据'));
    const hash=await page.evaluate(()=>location.hash);
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#detail').evaluate(e=>e.open),false);
    await page.locator('#query').fill('unmatched-phrase-7f8629');
    assert(await page.locator('.empty').isVisible());
    await page.locator('#clear').click();
    await page.locator('[data-category=tls]').click();
    assert(await page.locator('.card').count()>0);
    assert.equal(await page.locator('[data-category=tls]').getAttribute('aria-pressed'),'true');
    await page.locator('[data-category=all]').click();
    await page.screenshot({path:path.resolve(__dirname,'../docs/preview.png'),fullPage:false});
    await page.setViewportSize({width:390,height:844});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await page.locator('#query').fill('certificate');
    await page.locator('.open-entry').first().click();
    assert(await page.evaluate(()=>document.querySelector('dialog').getBoundingClientRect().width<=innerWidth));
    await page.locator('#close').click();
    await page.goto(url+hash);
    assert(await page.locator('#detail').evaluate(e=>e.open));
    assert.equal(network.length,0,'offline viewer should make no automatic network requests');
    assert.deepEqual(errors,[]);
    console.log(JSON.stringify({entries:total,desktop:true,mobile:true,search:true,filters:true,details:true,deepLink:true,networkRequests:network.length,consoleErrors:errors.length}));
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
