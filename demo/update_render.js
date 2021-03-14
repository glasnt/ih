// npm -i puppeteer
// takes a screenshot in headless chrome

const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({width: 1330,height: 800});
  await page.goto('file:///Users/glasnt/git/glasnt/ih/demo/demo_image.html');
  await page.screenshot({ path: 'demo/demo_render.png' });

  await browser.close();
})();
