const dbConfig = require("../config/db.config.js");

const Sequelize = require("sequelize");
const sequelize = new Sequelize(dbConfig.DB, dbConfig.USER, dbConfig.PASSWORD, {
  host: dbConfig.HOST,
  port: dbConfig.PORT,
  dialect: dbConfig.dialect,
  pool: {
    max: dbConfig.pool.max,
    min: dbConfig.pool.min,
    acquire: dbConfig.pool.acquire,
    idle: dbConfig.pool.idle,
  },
  logging: false
});

const db = {};

db.Sequelize = Sequelize;
db.sequelize = sequelize;

db.tutorials = require("./tutorial.model.js")(sequelize, Sequelize);
db.orders = require("./order.model.js")(sequelize,Sequelize);
db.companies = require("./company.model.js")(sequelize, Sequelize);
db.products = require("./product.model.js")(sequelize, Sequelize);
db.users = require("./user.model.js")(sequelize,Sequelize);
// db.ongoingbarcodes = require("./ongoingbarcode.model.js")(sequelize,Sequelize);
db.order_product = require("./order_product.model")(sequelize,Sequelize);
db.settings = require("./setting.model.js")(sequelize,Sequelize);
db.scanlog = require("./scanlog.model.js")(sequelize,Sequelize);
db.user_tokens = require("./user_token.model.js")(sequelize,Sequelize);
db.order_product_levels = require("./order_product_levels.model.js")(sequelize, Sequelize);
db.levels = require("./levels.model.js")(sequelize, Sequelize);
db.barcode = require("./barcode.model.js")(sequelize, Sequelize);

module.exports = db;