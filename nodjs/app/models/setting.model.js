module.exports = (sequelize, DataTypes) => {
    const Setting = sequelize.define("tblSetting", {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true
        },
        subsystem: {
            type: DataTypes.STRING
        },
        attribute: {
            type: DataTypes.STRING
        },
        value: {
            type: DataTypes.STRING
        }
    });

    return Setting;
};