module.exports = (sequelize, DataTypes) => {
  const ScanLog = sequelize.define('ScanLog', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    whOrderId: {
      type: DataTypes.INTEGER,
      references: {
        model: 'WarehouseOrder',
        key: 'OrderId'
      },
      onUpdate: 'CASCADE',
      onDelete: 'CASCADE'
    },
    whUserId: {
      type: DataTypes.INTEGER,
      references: {
        model: 'WhUsers',
        key: 'id'
      },
      onUpdate: 'CASCADE',
      onDelete: 'SET NULL'
    },
    uuid: {
      type: DataTypes.STRING(20)
    },
    createdAt: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW
    },
    updatedAt: {
      type: DataTypes.DATE
    }
  }, {
    tableName: 'ScanLogs',
    timestamps: true
  });

  return ScanLog;
};
