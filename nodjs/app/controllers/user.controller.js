const db = require("../models");
const User = db.users;
const bcrypt = require('bcryptjs');
const Op = db.Sequelize.Op;
const config = require("../config/db.config");
const { QueryTypes } = require('sequelize');
const { InsertOrUpdateUserToken } = require("./functions.controller");

// Create and Save a new User
exports.create = async (req, res) => {
  // Validate request
  if (!req.body.username) {
    res.status(400).send({
      message: "UserName cannot be empty!"
    });
    return;
  }

  // Create a User
  const user = {
    fname: req.body.fname,
    lname: req.body.lname,
    phone: req.body.phone,
    username: req.body.username,
    password: req.body.password,
  };

  try {
    const data = await User.create(user);
    res.send(data);
  } catch (err) {
    res.status(500).send({
      message: err.message || "Some error occurred while creating the User."
    });
  }
};

exports.insert = async (req, res) => {
  // Create a User with hashed password
  const user = {
    fname: req.body.fname,
    lname: req.body.lname,
    phone: req.body.phone,
    username: req.body.username,
    password: bcrypt.hashSync(req.body.password, 8), // Hashing the password
  };

  const sql = `INSERT INTO "WhUsers" ("fname", "lname", "username", "password", "phone", "createdAt", "updatedAt")
               VALUES (:fname, :lname, :username, :password, :phone, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
               RETURNING id;`;

  try {
    const result = await db.sequelize.query(sql, {
      replacements: user,
      type: db.Sequelize.QueryTypes.INSERT
    });
    res.send(result[0]);
  } catch (err) {
    console.error(err);
    res.status(500).send({ message: "Error inserting new user" });
  }
};

exports.inquiry = async (req, res, sequelize) => {
  const user = {
    username: req.body.username,
    password: req.body.password,  // این باید هش شود در صورتی که هش شده ذخیره می‌شود
  };

  const sql = `SELECT * FROM "WhUsers" WHERE "username" = :username AND "password" = :password LIMIT 1;`;

  try {
    const result = await sequelize.query(sql, {
      replacements: user,
      type: QueryTypes.SELECT
    });
    if (result.length > 0) {
      const userid = result[0].id;
      const userToken = await InsertOrUpdateUserToken(userid);  // تابع را بررسی کنید
      res.send({ ...result[0], token: userToken });
    } else {
      res.status(404).send({ message: "User not found" });
    }
  } catch (err) {
    console.error(err);
    res.status(500).send({ message: "Error during user inquiry" });
  }
};

exports.findAll = (req, res) => {
  const userid = req.query.id;
  var condition = userid ? { userid: { [Op.like]: `%${userid}%` } } : null;

  User.findAll({ where: condition })
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({
        message: err.message || "Some error occurred while retrieving users."
      });
    });
};

exports.findOne = (req, res) => {
  const id = req.params.id;

  User.findByPk(id)
    .then(data => {
      if (data) {
        res.send(data);
      } else {
        res.status(404).send({
          message: `User not found with id=${id}`
        });
      }
    })
    .catch(err => {
      res.status(500).send({
        message: `Error retrieving User with id=${id}`
      });
    });
};

exports.update = async (req, res) => {
  const id = req.params.id;

  try {
    const [updated] = await User.update(req.body, { where: { id: id } });
    if (updated) {
      res.send({ message: "User was updated successfully." });
    } else {
      res.status(404).send({ message: `Cannot update User with id=${id}. Maybe User was not found or req.body is empty!` });
    }
  } catch (err) {
    res.status(500).send({ message: "Error updating User with id=" + id });
  }
};

exports.delete = async (req, res) => {
  const id = req.params.id;

  try {
    const deleted = await User.destroy({ where: { id: id } });
    if (deleted) {
      res.send({ message: "User was deleted successfully!" });
    } else {
      res.status(404).send({ message: `Cannot delete User with id=${id}. Maybe User was not found!` });
    }
  } catch (err) {
    res.status(500).send({ message: "Could not delete User with id=" + id });
  }
};

exports.deleteAll = async (req, res) => {
  try {
    const nums = await User.destroy({ where: {}, truncate: false });
    res.send({ message: `${nums} Users were deleted successfully!` });
  } catch (err) {
    res.status(500).send({ message: err.message || "Some error occurred while removing all users." });
  }
};

exports.findAllPublished = async (req, res) => {
  try {
    const data = await User.findAll({ where: { published: true } });
    res.send(data);
  } catch (err) {
    res.status(500).send({ message: err.message || "Some error occurred while retrieving users." });
  }
};
