module.exports = (sequelize, DataTypes) => {
    const User = sequelize.define("WhUserToken", {
      id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
      },
      key: {
        type: DataTypes.STRING
      },
      whUserId: {
        type: DataTypes.INTEGER,
        references: {
          model: 'WhUsers',
          key: 'Id'
        },
        onUpdate: 'CASCADE',
        onDelete: 'SET NULL'
      },
    });
  
    return User;
  };