module.exports = (sequelize, DataTypes) => {
  const Barcodes = sequelize.define("barcodes", {
      id: {
          type: DataTypes.BIGINT,
          primaryKey: true,
          autoIncrement: true,
          allowNull: false
      },
      OrderId: {
          type: DataTypes.STRING(20),
          allowNull: true
      },
      LevelId: {
          type: DataTypes.SMALLINT,
          allowNull: true
      },
      Parent: {
          type: DataTypes.STRING(20),
          allowNull: true
      },
      RndEsalat: {
          type: DataTypes.CHAR(11),
          allowNull: true
      },
      XmlStatus: {
          type: DataTypes.SMALLINT,
          defaultValue: 0
      },
      Printed: {
          type: DataTypes.SMALLINT,
          defaultValue: 0
      },
      PrintDate: {
          type: DataTypes.DATEONLY,
          allowNull: true
      },
      QC: {
          type: DataTypes.SMALLINT,
          defaultValue: 0
      },
      QcDate: {
          type: DataTypes.DATEONLY,
          allowNull: true
      },
      QcDeviceId: {
          type: DataTypes.STRING(10),
          allowNull: true
      },
      CV: {
          type: DataTypes.SMALLINT,
          defaultValue: 0
      },
      CvDeviceId: {
          type: DataTypes.STRING(10),
          allowNull: true
      },
      CvDate: {
          type: DataTypes.DATE,
          allowNull: true
      },
      UserId: {
          type: DataTypes.INTEGER,
          allowNull: true
      },
      OrderSerial: {
          type: DataTypes.INTEGER,
          allowNull: true
      },
      FavoriteCode: {
          type: DataTypes.STRING(80),
          allowNull: true
      },
      uuid: {
          type: DataTypes.CHAR(15),
          allowNull: true
      },
      WhOrderId: {
          type: DataTypes.INTEGER,
          allowNull: true
      },
      WhScanDateTime: {
          type: DataTypes.DATE,
          allowNull: true
      },
      WhUserId: {
          type: DataTypes.INTEGER,
          allowNull: true
      },
      WhScanDate: {
          type: DataTypes.DATE,
          allowNull: true
      },
      subBarches_id: {
          type: DataTypes.INTEGER,
          allowNull: true
      },
      subBatchId: {
          type: DataTypes.INTEGER,
          allowNull: true
      },
      prefix: {
          type: DataTypes.CHAR(5),
          allowNull: false,
          defaultValue: '0'
      },
      IsBlocked: {
          type: DataTypes.BOOLEAN,
          defaultValue: false
      }
  }, {
      tableName: 'Barcodes',
      timestamps: false // assuming no auto timestamp fields are wanted unless specified
  });

  return Barcodes;
};
