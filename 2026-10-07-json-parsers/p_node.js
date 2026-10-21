const fs = require("fs");
const d = JSON.parse(fs.readFileSync("data.json", "utf8"));
let t = 0; for (const r of d) t += r.amount;
console.log(t.toFixed(2));
