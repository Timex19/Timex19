// Local visual verification using the workspace's existing development tools.
const fs = require('node:fs');
const path = require('node:path');
const { createRequire } = require('node:module');
const { pathToFileURL } = require('node:url');
const projectRequire = createRequire(path.resolve(__dirname, '../..', 'client/package.json'));
const markdown = projectRequire('markdown-it')({ html: true });
const { chromium } = projectRequire('playwright');
const output = path.join(__dirname, 'preview.html');
const body = markdown.render(fs.readFileSync(path.join(__dirname, 'README.md'), 'utf8'));
fs.writeFileSync(output, `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Joseph — profile design preview</title><style>
*{box-sizing:border-box}body{margin:0;background:#0d1117;color:#e6edf3;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}main{max-width:1012px;margin:32px auto;padding:32px;border:1px solid #30363d;border-radius:12px}h1,h2,h3{line-height:1.3}h1{font-size:28px}h2{font-size:24px;padding-bottom:8px;border-bottom:1px solid #30363d;margin-top:32px}h3{font-size:20px;margin-top:24px}p{margin:16px 0}img{max-width:100%;vertical-align:middle}p img[src*="shields.io"]{margin:3px 1px}a{color:#58a6ff;text-decoration:none}a:hover{text-decoration:underline}table{border-collapse:collapse;width:100%;margin:16px 0}td,th{border:1px solid #30363d;padding:14px;overflow-wrap:anywhere}td h3{margin-top:4px}td p{margin:8px 0}th{text-align:left;background:#161b22}tr:nth-child(2n){background:#161b22}details{padding:14px 16px;border:1px solid #30363d;border-radius:8px;margin:20px 0}summary{cursor:pointer}li{margin:8px 0}ul{padding-left:24px}@media(max-width:600px){main{margin:0;padding:16px;border:0;border-radius:0}td,th{padding:8px}td h3{font-size:17px}h1{font-size:23px}}@media(prefers-color-scheme:light){body{background:#fff;color:#1f2328}main,h2,td,th,details{border-color:#d1d9e0}th,tr:nth-child(2n){background:#f6f8fa}a{color:#0969da}}
</style></head><body><main>${body}</main></body></html>`);
(async () => {
  const browser = await chromium.launch({headless:true,channel:'msedge'});
  const page = await browser.newPage({viewport:{width:1120,height:900},colorScheme:'dark'});
  // Keep the preview reproducible when badge services cannot be reached.
  await page.route('https://img.shields.io/**', async route => {
    const pathname = new URL(route.request().url()).pathname;
    const payload = decodeURIComponent(pathname.slice('/badge/'.length));
    const colorAt = payload.lastIndexOf('-');
    const color = payload.slice(colorAt+1);
    const label = payload.slice(0,colorAt).replace(/--/g,'\u0000').replace(/-/g,' · ').replace(/_/g,' ').replace(/\u0000/g,'-');
    const safeLabel = label.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    const width = Math.max(58, label.length * 7 + 24);
    await route.fulfill({contentType:'image/svg+xml',body:`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="28"><rect width="100%" height="100%" rx="3" fill="#${color}"/><text x="50%" y="18" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="700" fill="white">${safeLabel}</text></svg>`});
  });
  await page.route('https://github-readme-stats.vercel.app/**', route => route.abort());
  await page.goto(pathToFileURL(output).href,{waitUntil:'networkidle'});
  const broken = await page.locator('img[src^="./assets/"]').evaluateAll(images=>images.filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src));
  if(broken.length) throw new Error(`Broken local images: ${broken.join(', ')}`);
  await page.screenshot({path:path.join(__dirname,'preview-desktop.png'),fullPage:true});
  await page.screenshot({path:path.join(__dirname,'preview-hero.png'),fullPage:false});
  await page.setViewportSize({width:390,height:844});
  for (const scheme of ['dark','light']) {
    await page.emulateMedia({colorScheme:scheme});
    const overflow = await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
    if(overflow) throw new Error(`Horizontal overflow at 390px in ${scheme} mode`);
    await page.screenshot({path:path.join(__dirname,`preview-mobile-${scheme}.png`),fullPage:true});
  }
  await browser.close();
  console.log('Local assets loaded. Desktop and mobile previews generated; no mobile horizontal overflow in dark or light mode. Badge graphics are local approximations; actual GitHub rendering was not tested.');
})().catch(err=>{console.error(err);process.exitCode=1;});
