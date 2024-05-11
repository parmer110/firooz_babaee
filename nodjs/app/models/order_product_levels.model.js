module.exports = (sequelize, DataTypes) => {
  const WareHouseOrderLevels = sequelize.define("WareHouseOrderLevels", {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
      allowNull: false
    },
    orderId: {
      type: DataTypes.INTEGER,
      field: 'order_id',
      allowNull: true,
      references: {
        model: 'WarehouseOrders',
        key: 'orderid'
      },
      onUpdate: 'CASCADE',
      onDelete: 'CASCADE'
    },
    LevelId: {
      type: DataTypes.INTEGER,
      field: 'level_id',
      allowNull: true,
      references: {
        model: 'Levels',
        key: 'levelId'
      },
      onUpdate: 'CASCADE'
    },
    NumberOfOrder: {
      type: DataTypes.INTEGER,
      field: 'number_of_order',
      allowNull: true
    }
  }, {
    tableName: 'warehouse_order_levels',
    timestamps: false
  });

  return WareHouseOrderLevels;
};
