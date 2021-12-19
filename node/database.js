const express = require("express");
const data = require("../vaccineData.json");
const app = express();
const port = process.env.PORT || 5000;

app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.get("/data", (req, res) => {
    if (!data || data.length === 0) throw new Error("Sorry! no data found");
    res.json(data);
});

app.listen(port, () => console.log(`App listening on port ${port}!`))