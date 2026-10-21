import fetch from "${TREE:-.}/node_modules/node-fetch/src/index.js";
const r = await fetch(process.argv[2]); console.log((await r.text()).slice(0,10));
