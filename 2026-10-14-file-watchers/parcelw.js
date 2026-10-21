const w = require("${TREE:-.}/node_modules/@parcel/watcher");
w.subscribe(process.argv[2], () => {}).then(() => console.log("ready"));
setInterval(() => {}, 1000);
