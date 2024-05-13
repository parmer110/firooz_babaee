module.exports = (sequelize, DataTypes) => {
    const Order_Product = sequelize.define("WarehouseOrderProduct", {
      orderid: {
        type: DataTypes.INTEGER
      },
      gtin: {
        type: DataTypes.STRING
      },
                
    });
    return Order_Product;
  };