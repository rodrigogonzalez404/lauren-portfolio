// Renders the CSS laptop (same as the viewer) onto the shared cream: hero.jpg (16:9) and card.jpg (4:3) for big-pink and marketplace.
const {chromium}=require('/workspace/shot-tools/node_modules/playwright-core');
const B='http://localhost:8765/lauren-portfolio/';   // serve /tmp/srv (lauren-portfolio -> repo); then convert PNG -> JPG into /workspace/bigpink/rendered/
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1600,height:1200},deviceScaleFactor:2});
const jobs=[['big-pink','../../assets/img/big-pink/scr/s01.jpg'],['marketplace','../../assets/img/marketplace/scr/s01.jpg']];
for(const [slug,src] of jobs){
 for(const [name,w,h,lw] of [['hero.jpg',1440,810,1000],['card.jpg',1200,900,1000]]){
  await p.goto(`${B}_src/bigpink/laptop-render.html?w=${w}&h=${h}&lw=${lw}&src=${encodeURIComponent(src)}`,{waitUntil:'networkidle'});await p.waitForTimeout(400);
  await (await p.$('#st')).screenshot({path:`/workspace/bigpink/rendered/${slug}-${name.replace('.jpg','.png')}`});
 }}
await b.close()})();
