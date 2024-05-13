module.exports = (sequelize, DataTypes) => {
    const User = sequelize.define("WhUser", {
      id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
      },
      first_name: {
        type: DataTypes.STRING
      },
      last_name: {
        type: DataTypes.STRING
      },
      username: {
        type: DataTypes.STRING
      },  
      password: {
        type: DataTypes.STRING
      }, 
      phone: {
        type: DataTypes.STRING
      },
      is_active: {
        type: DataTypes.BOOLEAN,
        defaultValue: true
      },  
      date_joined: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW,
        allowNull: false
      },        
    });
  
    return User;
  };