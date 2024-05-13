module.exports = (sequelize, DataTypes) => {
    const Company = sequelize.define("Company", {
      NationalId: {
        type: DataTypes.STRING
      },
      CompanyFaName: {
        type: DataTypes.STRING
      },
      Prefix: {
        type: DataTypes.STRING
      },
      defaultDc: {
        type: DataTypes.BOOLEAN
      },
      defaultOc: {
        type: DataTypes.BOOLEAN
      },
    });
  
    return Company;
  };