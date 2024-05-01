module.exports = (sequelize, DataTypes) => {
    const Level = sequelize.define("Level", {
      levelId: {
        type: DataTypes.INTEGER,
        unique: true,
        allowNull: false,
        field: 'levelId',
        validate: {
          notEmpty: true
        }
      },
      level_name: {
        type: DataTypes.STRING(128),
        allowNull: true,
        field: 'level_name',
        validate: {
          len: [0, 128]
        }
      },
      insert_date: {
        type: DataTypes.DATEONLY,
        allowNull: false,
        defaultValue: DataTypes.NOW,
        field: 'insert_date'
      }
    }, {
      tableName: 'levels',
      timestamps: true,
      underscored: true
    });
  
    Level.associate = function(models) {
        Level.belongsTo(models.WhUser, {
          foreignKey: 'user',
          as: 'user',
          allowNull: true,
          onDelete: 'SET NULL'
        });
      };
        
    return Level;
  };
  