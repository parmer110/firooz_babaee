module.exports = (sequelize, DataTypes) => {
    const Barcodes = sequelize.define("barcodes", {
      id: {
        type: DataTypes.BIGINT,
        primaryKey: true,
        autoIncrement: true,
        allowNull: false
      },
      whOrderId: { // تغییر به camelCase
        type: DataTypes.INTEGER,
        allowNull: true,
        references: {
          model: 'WarehouseOrders', // اسم جدول کلید خارجی
          key: 'OrderId'
        },
        field: 'WhOrderId' // مطابقت با نام ستون در دیتابیس
      },
      orderId: { // تغییر به camelCase
        type: DataTypes.STRING(20),
        allowNull: true,
        references: {
          model: 'Orders', // اسم جدول کلید خارجی
          key: 'OrderCode'
        },
        field: 'orderid' // مطابقت با نام ستون در دیتابیس
      },
      xmlStatus: { // تغییر به camelCase
        type: DataTypes.SMALLINT,
        defaultValue: 0
      },
      uuid: {
        type: DataTypes.CHAR(20), // تغییر طول رشته به 20
        allowNull: false
      },
      uuidCount: { // اضافه شده برای هماهنگی با مدل جنگو
        type: DataTypes.INTEGER,
        defaultValue: 0,
        allowNull: true
      },
      rndEsalat: { // تغییر به camelCase و تغییر طول رشته
        type: DataTypes.STRING(140),
        allowNull: true,
        unique: true
      },
      rndEsalatCount: { // اضافه شده برای هماهنگی با مدل جنگو
        type: DataTypes.INTEGER,
        defaultValue: 0
      },
      parent: {
        type: DataTypes.STRING(20),
        allowNull: true
      },
      datatime_created: { // تغییر به camelCase و تنظیمات auto timestamp
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
      },
      datatime_modified: { // تغییر به camelCase و تنظیمات auto timestamp
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
      },
      levelId: { // تغییر به camelCase
        type: DataTypes.SMALLINT,
        allowNull: true
      },
      printed: { // مطابقت با مدل جنگو
        type: DataTypes.SMALLINT,
        defaultValue: 0
      },
      printDate: {
        type: DataTypes.DATEONLY,
        allowNull: true
      },
      qc: {
        type: DataTypes.SMALLINT,
        defaultValue: 0
      },
      qcDate: {
        type: DataTypes.DATEONLY,
        allowNull: true
      },
      qcDeviceId: {
        type: DataTypes.STRING(10),
        allowNull: true
      },
      cv: {
        type: DataTypes.SMALLINT,
        defaultValue: 0
      },
      cvDeviceId: {
        type: DataTypes.STRING(10),
        allowNull: true
      },
      cvDate: {
        type: DataTypes.DATE,
        allowNull: true
      },
      userId: {
        type: DataTypes.INTEGER,
        allowNull: true
      },
      orderSerial: {
        type: DataTypes.INTEGER,
        allowNull: true
      },
      favoriteCode: {
        type: DataTypes.STRING(80),
        allowNull: true
      },
      whScanDateTime: {
        type: DataTypes.DATE,
        allowNull: true
      },
      whUserId: {
        type: DataTypes.INTEGER,
        allowNull: true
      },
      whScanDate: {
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
      isBlocked: {
        type: DataTypes.BOOLEAN,
        defaultValue: false
      }
    }, {
      tableName: 'Barcodes',
      timestamps: false // assuming no auto timestamp fields are wanted unless specified
    });
  
    return Barcodes;
  };
  