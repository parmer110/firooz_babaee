module.exports = (sequelize, Sequelize) => {
    const Company = sequelize.define("Company", {
      NationalId: {
        type: Sequelize.STRING
      },
      CompanyFaName: {
        type: Sequelize.STRING
      },
      Prefix: {
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