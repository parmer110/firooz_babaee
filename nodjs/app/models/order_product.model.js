module.exports = (sequelize, DataTypes) => {
  const WarehouseOrderProducts = sequelize.define("WarehouseOrderProducts", {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
      allowNull: false
    },
    orderId: {
      type: DataTypes.INTEGER,
      field: 'orderid',
      allowNull: true,
      references: {
        model: 'WarehouseOrder',
        key: 'OrderId'
      },
      onUpdate: 'CASCADE',
      onDelete: 'CASCADE'
    },
    Gtin: {
      type: DataTypes.CHAR(14),
      field: 'gtin',
      allowNull: true,
      references: {
        model: 'Product',
        key: 'GTIN'
      },
      onUpdate: 'CASCADE'
    },
    createdAt: {
      type: DataTypes.DATE,
      allowNull: true,
      defaultValue: DataTypes.NOW
    },
    updatedAt: {
      type: DataTypes.DATE,
      allowNull: true,
      defaultValue: DataTypes.NOW
    }
  }, {
    tableName: 'WarehouseOrderProducts',
    timestamps: true
  });

  return WarehouseOrderProducts;
};
