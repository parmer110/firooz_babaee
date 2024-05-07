const express = require("express");
// const bodyParser = require("body-parser"); /* deprecated */
const cors = require("cors");

const jwt = require('jsonwebtoken'); 

const dotenv = require('dotenv'); 

const app = express();

dotenv.config(); 

var corsOptions = {
  origin: "http://localhost:8080"
};

app.use(cors(corsOptions));

// parse requests of content-type - application/json
app.use(express.json());  /* bodyParser.json() is deprecated */

// parse requests of content-type - application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));   /* bodyParser.urlencoded() is deprecated */

const db = require("./app/models");

db.sequelize.sync();
// // drop the table if it already exists
// db.sequelize.sync({ force: true }).then(() => {
//   console.log("Drop and re-sync db.");
// });
const AppVersion='14020306';
// simple route
app.get("/", (req, res) => {
  res.json({ message: `Welcome to handheld application.\n Version:${AppVersion}` });
});

// Development environment log
app.use((req, res, next) => {
  console.log(`→→→→→→→ ${req.method}, ${req.protocol}://${req.get('host')}${req.originalUrl}`);
  console.log('Headers:', req.headers);
  console.log('Body:', req.body);
  next();
});

require("./app/routes/order.routes")(app);
require("./app/routes/company.routes")(app);
require("./app/routes/product.routes")(app);
require("./app/routes/user.routes")(app);
require("./app/routes/ongoingbarcode.routes")(app);
require("./app/routes/order_product.routes")(app);
require("./app/routes/setting.routes")(app);
require("./app/routes/scanlog.routes")(app);
require("./app/routes/user_token.routes")(app);



// set port, listen for requests
const PORT = process.env.PORT || 8082;
const HOST = process.env.HOST || 'localhost';
app.listen(PORT, () => {
  console.log(`Server is running on url http://${HOST}:${PORT}`);
});