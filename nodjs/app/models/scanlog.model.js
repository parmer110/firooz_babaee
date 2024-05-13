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
        model: 'WarehouseOrders',  // این باید نام جدول در دیتابیس باشد، نه نام مدل
        key: 'OrderId'
      },
      onUpdate: 'CASCADE',
      onDelete: 'CASCADE'
    },
    whUserId: {
      type: DataTypes.INTEGER,
      references: {
        model: 'WhUsers',  // اطمینان حاصل کنید که این هم نام دقیق جدول در دیتابیس است
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
    tableName: 'ScanLogs',  // اطمینان حاصل کنید که نام جدول مطابق با نام در پایگاه داده است
    timestamps: true
  });

  return ScanLog;
};
