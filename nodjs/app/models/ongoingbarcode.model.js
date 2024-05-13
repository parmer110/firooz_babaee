module.exports = (sequelize, DataTypes) => {
  const Ongoingbarcode = sequelize.define("Ongoingbarcode", {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
    },
    orderid: {
      type: DataTypes.STRING,
    },
    levelid: {
      type: DataTypes.INTEGER,
    },
    parent: {
      type: DataTypes.STRING,
    },
    uuid: { type: DataTypes.STRING },
    rndesalat: { type: DataTypes.STRING },
    orderserial: { type: DataTypes.INTEGER },
    favoritecode: { type: DataTypes.INTEGER },
    whorderid: { type: DataTypes.INTEGER},
  });

  return Ongoingbarcode;
};
