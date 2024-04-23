module.exports = (sequelize, Sequelize) => {
    const Company = sequelize.define("Company", {
      nationalid: {
        type: Sequelize.STRING
      },
      companyfaname: {
        type: Sequelize.STRING
      },
      prefix: {
        type: Sequelize.STRING
      },
      defaultDc: {
        type: Sequelize.BOOLEAN
      },
      defaultOc: {
        type: Sequelize.BOOLEAN
      },
    });
  
    return Company;
  };