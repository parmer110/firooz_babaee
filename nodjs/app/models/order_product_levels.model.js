module.exports = (sequelize, DataTypes) => {
  const WareHouseOrderLevels = sequelize.define("WareHouseOrderLevels", {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
      allowNull: false
    },
    OrderId: {
      type: DataTypes.INTEGER,
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
      allowNull: true,
      references: {
        model: 'Levels',
        key: 'levelId'
      },
      onUpdate: 'CASCADE'
    },
    NumberOfOrder: {
      type: DataTypes.INTEGER,
      allowNull: true
    }
  }, {
    tableName: 'WareHouseOrderLevels',
    timestamps: false
  });

  return WareHouseOrderLevels;
};
