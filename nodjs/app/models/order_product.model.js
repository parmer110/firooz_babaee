module.exports = (sequelize, Sequelize) => {
  const OrderProduct = sequelize.define("WarehouseOrderProduct", {
    orderid: {
      type: Sequelize.INTEGER,
      allowNull: false // Assuming orderid should not be null
    },
    gtin: {
      type: Sequelize.STRING,
      allowNull: false // Assuming gtin should not be null
    },
  });

  return OrderProduct;
};
