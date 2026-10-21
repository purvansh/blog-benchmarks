const fs = require("fs");
fs.watch(process.argv[2], { recursive: true }, () => {});
console.log("ready");
setInterval(() => {}, 1000);
