module.exports = (sequelize, DataTypes) => {
    const Product = sequelize.define("Product", {
      GTIN: {
        type: DataTypes.STRING
      },
      // id: {
      //   type: DataTypes.INTEGER
      // },
      ProductFrName: {
        type: DataTypes.STRING
      },
      irc: {
        type: DataTypes.STRING
      },
      ProducerCompanyCode: {
        type: DataTypes.INTEGER
      },
    });
  
    return Product;
  };