const db = require("../models");
const User = db.users;
const Op = db.Sequelize.Op;
const config = require("../config/db.config");
const { QueryTypes } = require('sequelize');
const { InsertOrUpdateUserToken } = require("./functions.controller");

// Create and Save a new User
exports.create = (req, res) => {
  // Validate request
  if (!req.body.username) {
    res.status(400).send({
      message: "UserName can not be empty!"
    });
    return;
  }

  // Create a User
  const user = {
    // id: req.body.id,
    fname: req.body.fname,
    lname: req.body.lname,
    phone: req.body.phone,
    username: req.body.username,
    password: req.body.password,
  };

  // Save User in the database
  User.create(user)
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while creating the User."
      });
    });
};

exports.insert = async (req, res) => {
  const user = {
    fname: req.body.fname,
    lname: req.body.lname,
    phone: req.body.phone,
    username: req.body.username,
    password: req.body.password,
  };

  const sequelize = new Sequelize(config.DB, config.USER, config.PASSWORD, {
    host: config.HOST,
    dialect: 'postgres',
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  });

  const sql = `INSERT INTO "WhUsers" ("fname", "lname", "username", "password", "phone", "createdAt", "updatedAt")
               VALUES ($fname, $lname, $username, $password, $phone, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
               RETURNING id;`;

  try {
    const result = await sequelize.query(sql, {
      replacements: user,
      type: QueryTypes.INSERT
    });
    res.send(result[0]);
  } catch (err) {
    console.error(err);
    res.status(500).send({ message: "Error inserting new user" });
  }
};
exports.inquiry = async (req, res) => {
  const user = {
    username: req.body.username,
    password: req.body.password,
  };

  const sql = `SELECT * FROM "WhUsers" WHERE "username" = $username AND "password" = $password LIMIT 1;`;

  try {
    const result = await sequelize.query(sql, {
      replacements: { username: user.username, password: user.password },
      type: QueryTypes.SELECT
    });
    if (result.length > 0) {
      const userid = result[0].id;
      const userToken = await InsertOrUpdateUserToken(userid);  // اطمینان حاصل کنید که این تابع درست کار می‌کند
      res.send({ ...result[0], token: userToken });
    } else {
      res.status(404).send({ message: "User not found" });
    }
  } catch (err) {
    console.error(err);
    res.status(500).send({ message: "Error during user inquiry" });
  }
};

// Retrieve all Users from the database.
exports.findAll = (req, res) => {
  const userid = req.query.id;
  var condition = userid ? { userid: { [Op.like]: `%${userid}%` } } : null;

  User.findAll({ where: condition })
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving users."
      });
    });
};

// Find a single User with an id
exports.findOne = (req, res) => {
  const id = req.params.id;

  User.findByPk(id)
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({
        message: "Error retrieving User with id=" + id
      });
    });
};

// Update an existing User by the id in the request
exports.update = (req, res) => {
  const id = req.params.id;

  User.update(req.body, {
    where: { id: id }
  })
    .then(num => {
      if (num == 1) {
        res.send({
          message: "User was updated successfully."
        });
      } else {
        res.status(404).send({
          message: `Cannot update User with id=${id}. Maybe User was not found or req.body is empty!`
        });
      }
    })
    .catch(err => {
      res.status(500).send({
        message: "Error updating User with id=" + id
      });
    });
};

// Delete an User with the specified id in the request
exports.delete = (req, res) => {
  const id = req.params.id;

  User.destroy({
    where: { id: id }
  })
    .then(num => {
      if (num == 1) {
        res.send({
          message: "User was deleted successfully!"
        });
      } else {
        res.status(404).send({
          message: `Cannot delete User with id=${id}. Maybe User was not found!`
        });
      }
    })
    .catch(err => {
      res.status(500).send({
        message: "Could not delete User with id=" + id
      });
    });
};

// Delete all Users from the database.
exports.deleteAll = (req, res) => {
  User.destroy({
    where: {},
    truncate: false
  })
    .then(nums => {
      res.send({ message: `${nums} Users were deleted successfully!` });
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while removing all users."
      });
    });
};

// find all published User
exports.findAllPublished = (req, res) => {
  User.findAll({ where: { published: true } })
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving users."
      });
    });
};
