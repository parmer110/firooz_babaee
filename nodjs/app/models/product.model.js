module.exports = (sequelize, Sequelize) => {
    const Product = sequelize.define("Product", {
      GTIN: {
        type: Sequelize.STRING
      },
      // id: {
      //   type: Sequelize.INTEGER
      // },
      ProductFrName: {
        type: Sequelize.STRING
      },
      irc: {
        type: Sequelize.STRING
      },
      ProducerCompanyCode: {
        type: Sequelize.INTEGER
      },
    });
  
    return Product;
  };