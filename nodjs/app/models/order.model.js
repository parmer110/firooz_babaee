module.exports = (sequelize, DataTypes) => {
  const WarehouseOrder = sequelize.define("WarehouseOrder", {
      id: {
          type: DataTypes.INTEGER,
          allowNull: false
      },
      OrderId: {
          type: DataTypes.INTEGER,
          primaryKey: true,
          allowNull: false
      },
      DistributerCompanyNid: {
          type: DataTypes.STRING,
          allowNull: true
      },
      ordertype: {
          type: DataTypes.STRING,
          allowNull: false,
          field: 'ordertype',
          defaultValue: 'outgoing',
          validate: {
              isIn: [['incoming', 'outgoing', 'returning']]
          }
      },
      no: {
          type: DataTypes.STRING,
          defaultValue: ""
      },
      gtin: {
          type: DataTypes.STRING,
          allowNull: true
      },
      batchnumber: {
          type: DataTypes.STRING,
          allowNull: true
      },
      expdate: {
          type: DataTypes.STRING,
          allowNull: true
      },
      userId: {
          type: DataTypes.INTEGER,
          allowNull: true
      },
      insertdate: {
          type: DataTypes.STRING,
          allowNull: true
      },
      lastxmldate: {
          type: DataTypes.STRING,
          allowNull: true
      },
      ordercompanynid: {
          type: DataTypes.INTEGER,
          allowNull: true
      },
      DeviceId: {
          type: DataTypes.STRING,
          allowNull: true
      },
      productionorderid: {
          type: DataTypes.STRING,
          allowNull: true
      },
      details: {
          type: DataTypes.STRING,
          allowNull: true
      },
      lc: {
          type: DataTypes.STRING,
          allowNull: true
      },
      px: {
          type: DataTypes.STRING,
          defaultValue: ""
      },
      wo: {
          type: DataTypes.STRING,
          allowNull: true
      },
      createdAt: {
          type: DataTypes.DATE,
          defaultValue: DataTypes.NOW
      },
      updatedAt: {
          type: DataTypes.DATE,
          defaultValue: DataTypes.NOW
      }
  }, {
      tableName: 'WarehouseOrders'
  });

  return WarehouseOrder;
};
