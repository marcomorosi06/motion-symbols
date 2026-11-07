// Copyright 2026 Marco Morosi
// Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
//
// Development aid for verify_chrome.py: opens an HTML file in headless
// Chrome, seeks every <svg data-t="ms"> to its time and takes a screenshot.
// Needs puppeteer (M3A_PUPPETEER: module path) and a Chrome binary
// (M3A_CHROME: executable path).
// Usage: node shot.js PAGE.html OUT.png WIDTH HEIGHT
const puppeteer = require(process.env.M3A_PUPPETEER || 'puppeteer');
(async () => {
  const [html, out, w, h] = process.argv.slice(2);
  const browser = await puppeteer.launch({executablePath: process.env.M3A_CHROME || undefined, args: ['--no-sandbox']});
  const page = await browser.newPage();
  await page.setViewport({width: +w, height: +h, deviceScaleFactor: 1});
  await page.goto('file://' + html);
  await page.evaluate(() => {
    for (const s of document.querySelectorAll('svg[data-t]')) {
      s.pauseAnimations();
      s.setCurrentTime(parseFloat(s.dataset.t) / 1000);
    }
  });
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({path: out, fullPage: true});
  await browser.close();
})();
