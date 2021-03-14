// npm -i puppeteer
// takes a screenshot in headless chrome
// presumes ih has been run to produce the demo_image.html file

const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({width: 1330,height: 800});
  await page.goto('file://'+process.cwd()+'/demo/demo_image.html');
  await page.screenshot({ path: 'demo/demo_render.png' });

  await browser.close();
})();
