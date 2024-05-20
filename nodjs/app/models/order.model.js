module.exports = (sequelize, DataTypes, Sequelize) => {
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
    
    const Order = sequelize.define("Order", {
        Id: {
            type: DataTypes.BIGINT,
            allowNull: false,
            
        },
        OrderCode: {
            type: DataTypes.STRING(20),
            allowNull: false,
            unique: true,
            primaryKey: true
        },
        ProductCode: {
            type: DataTypes.CHAR(14),
            allowNull: true,
            references: {
                model: 'Products',
                key: 'GTIN'
            },
            onUpdate: 'CASCADE'
        },
        SupplierCode: DataTypes.CHAR(11),
        PublisherCode: DataTypes.CHAR(11),
        Numberinpack: {
            type: DataTypes.INTEGER,
            defaultValue: 0
        },
        NumberOfOrder: {
            type: DataTypes.INTEGER,
            defaultValue: 0
        },
        PakingLevel: {
            type: DataTypes.SMALLINT,
            defaultValue: 0
        },
        BatchNumber: DataTypes.STRING(80),
        ProduceDate: DataTypes.CHAR(10),
        ExpDate: DataTypes.CHAR(10),
        ReleaseNumber: DataTypes.STRING(64),
        ReleaseDate: DataTypes.STRING(10),
        OrderDate: DataTypes.STRING(10),
        NumberOfCoded: {
            type: DataTypes.INTEGER,
            defaultValue: 0
        },
        LastCodingDate: DataTypes.CHAR(20),
        Price: DataTypes.INTEGER,
        UserCode: DataTypes.STRING(50),
        InsertDate: {
            type: DataTypes.CHAR(10),
            defaultValue: Sequelize.literal('CURRENT_DATE')
        },
        Done: DataTypes.SMALLINT,
        FullPackcount: DataTypes.INTEGER,
        TotalCount: DataTypes.INTEGER,
        MiniOrigin: DataTypes.SMALLINT,
        invoiceNumber: DataTypes.STRING(100),
        TempIRC: DataTypes.STRING(50),
        Selected: DataTypes.BOOLEAN,
        Accepted: DataTypes.BOOLEAN,
        NumberOfPrinted: {
            type: DataTypes.INTEGER,
            defaultValue: 0
        },
        Userid: DataTypes.INTEGER,
        XmlStatus: {
            type: DataTypes.BOOLEAN,
            defaultValue: false
        },
        archiveprefix: DataTypes.CHAR(3),
        version: DataTypes.STRING(50),
        prefix: DataTypes.CHAR(5)
    }, {
        tableName: 'Orders',
        timestamps: true,
        updatedAt: 'updatedAt',
        createdAt: 'createdAt'
    });
    
    // Define relationships
    Order.associate = function(models) {
        Order.hasMany(models.Barcode, { foreignKey: 'orderId', sourceKey: 'OrderCode' });
      };
    
    return {
      WarehouseOrder,
      Order
    };
  };
  