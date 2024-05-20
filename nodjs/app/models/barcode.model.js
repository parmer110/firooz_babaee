module.exports = (sequelize, DataTypes) => {
  const Barcode = sequelize.define("Barcode", {
    id: {
      type: DataTypes.BIGINT,
      primaryKey: true,
      autoIncrement: true,
      allowNull: false
    },
    whOrderId: {
      type: DataTypes.INTEGER,
      allowNull: true,
      references: {
        model: 'WarehouseOrders',
        key: 'OrderId'
      },
      field: 'WhOrderId'
    },
    orderId: {
      type: DataTypes.INTEGER,
      allowNull: true,
      references: {
        model: 'Orders',
        key: 'OrderCode'
      },
      field: 'OrderId'
    },
    XmlStatus: {
      type: DataTypes.SMALLINT,
      defaultValue: 0,
      field: 'XmlStatus'
    },
    uuid: {
      type: DataTypes.CHAR(20),
      allowNull: false
    },
    UUIDCount: {
      type: DataTypes.INTEGER,
      defaultValue: 0,
      allowNull: true
    },
    RndEsalat: {
      type: DataTypes.STRING(140),
      allowNull: true,
      unique: true
    },
    RndEsalatCount: {
      type: DataTypes.INTEGER,
      defaultValue: 0
    },
    parent: {
      type: DataTypes.STRING(20),
      allowNull: true
    },
    datatime_created: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW
    },
    datatime_modified: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW
    },
    levelid: {
      type: DataTypes.SMALLINT,
      allowNull: true,
      field: "levelid"
    },
    favoriteCode: {
      type: DataTypes.STRING(80),
      allowNull: true
    },
  }, {
    tableName: 'Barcodes',
    timestamps: false
  });

  // Define relationships
  Barcode.associate = function(models) {
    Barcode.belongsTo(models.Order, { foreignKey: 'orderId', targetKey: 'OrderCode' });
  };

  return Barcode;
};
