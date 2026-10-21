const http = require("http");
http.get(process.argv[2], (res) => { res.on("data", () => {}); res.on("end", () => console.log("done")); })
    .on("error", (e) => { console.log("error " + e.message); process.exit(1); });
