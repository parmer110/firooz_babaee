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

// Ensure all models are initialized consistently
db.tutorials = require("./tutorial.model.js")(sequelize, Sequelize.DataTypes, Sequelize);
const orderModels = require("./order.model.js")(sequelize, Sequelize.DataTypes, Sequelize);
db.WarehouseOrder = orderModels.WarehouseOrder;
db.Order = orderModels.Order;
db.companies = require("./company.model.js")(sequelize, Sequelize.DataTypes, Sequelize);
db.products = require("./product.model.js")(sequelize, Sequelize.DataTypes, Sequelize);
db.users = require("./user.model.js")(sequelize, Sequelize.DataTypes, Sequelize);
db.ongoingbarcodes = require("./ongoingbarcode.model.js")(sequelize, Sequelize.DataTypes, Sequelize);
db.order_product = require("./order_product.model")(sequelize, Sequelize.DataTypes, Sequelize);
db.settings = require("./setting.model.js")(sequelize, Sequelize.DataTypes, Sequelize);
db.scanlog = require("./scanlog.model.js")(sequelize, Sequelize.DataTypes, Sequelize);
db.user_tokens = require("./user_token.model.js")(sequelize, Sequelize.DataTypes, Sequelize);
db.order_product_levels = require("./order_product_levels.model.js")(sequelize, Sequelize.DataTypes, Sequelize);
db.levels = require("./levels.model.js")(sequelize, Sequelize.DataTypes, Sequelize);
db.barcode = require("./barcode.model.js")(sequelize, Sequelize.DataTypes, Sequelize);

// Define relationships
db.WarehouseOrder.hasMany(db.barcode, { foreignKey: 'whOrderId', sourceKey: 'OrderId' });
db.barcode.belongsTo(db.WarehouseOrder, { foreignKey: 'whOrderId', targetKey: 'OrderId' });

db.Order.hasMany(db.barcode, { foreignKey: 'orderId', sourceKey: 'OrderCode' });
db.barcode.belongsTo(db.Order, { foreignKey: 'orderId', targetKey: 'OrderCode' });

module.exports = db;
