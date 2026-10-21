const chokidar = require("${TREE:-.}/node_modules/chokidar");
const w = chokidar.watch(process.argv[2], { ignoreInitial: true });
w.on("ready", () => console.log("ready"));
setInterval(() => {}, 1000);
