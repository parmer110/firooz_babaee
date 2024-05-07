const db = require("../models");
const User = db.users;
const bcrypt = require('bcryptjs');
// const bcrypt = require('bcrypt');
const Op = db.Sequelize.Op;
const config = require("../config/db.config");
const sequelize = db.sequelize;
const { QueryTypes } = require('sequelize');
const Sequelize = require('sequelize');
const { InsertOrUpdateUserToken } = require("./functions.controller");
const jwt = require('jsonwebtoken');
const fs = require('fs');
const privateKey = fs.readFileSync('./privateKey.pem', 'utf8');
const publicKey = fs.readFileSync('./publicKey.pem', 'utf8');
require('dotenv').config({ path: `${process.cwd()}/../../.env` });
// const authHelper = require('../../helpers/authHelper');

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

// Create a User with hashed password
exports.insert = async (req, res) => {
  try {

    const { fname: first_name, lname: last_name, phone, username, password } = req.body;

    const existingUser = await User.findOne({ where: { username } });
    if (existingUser) {
      return res.status(409).send({ message: "Username already exists" });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const newUser = await User.create({
      first_name,
      last_name,
      username,
      password: hashedPassword,
      phone,
      createdAt: new Date(),
      updatedAt: new Date()
    });

    res.send([[{ ServerUserId: newUser.id.toString() }]]);
  } catch (error) {
    console.error(error);
    res.status(500).send({ message: "Error creating new user" });
  }
};

exports.inquiry = async (req, res) => {
  console.log("↓↓↓↓↓↓↓↓↓↓");
  const jwtPrivateKey = privateKey
  const { username, password } = req.body;

  try {
    // Find the user in the database
    const user = await db.users.findOne({ where: { username } });
    if (!user) {
      return res.send([{ result: 'notfound' }]);
    }

    // Compare hashed password with the provided password
    const test = await bcrypt.compare(password, user.password);
    console.log(test);
    const isPasswordMatch = await bcrypt.compare(password, user.password);
    console.log(isPasswordMatch);
    if (isPasswordMatch) {
      // Remove all existing tokens for the user
      await db.user_tokens.destroy({
        where: { whUserId: user.id }
      });

      // Generate token using private key
      const userToken = jwt.sign({ userId: user.id }, jwtPrivateKey, { algorithm: 'RS256' });

      // Save the new token to the database
      await db.user_tokens.create({
        key: userToken,
        whUserId: user.id,
      });

      // Prepare user response, excluding sensitive information
      const userResponse = user.toJSON();
      userResponse.password = "";
      userResponse.result = 'ok';

      // Save the token to the database
      await db.user_tokens.create({
        key: userToken,
        whUserId: user.id,
      });

      res.send([userResponse, { token: userToken }]);
    } else {
      res.send([{ result: 'Incorrect password' }]);
    }
  } catch (err) {
    console.error(err);
    res.status(500).send([{ message: "Error during user inquiry" }]);
  }
};

exports.logout = async (req, res) => {
  try {
    // Assuming the token is sent as 'Bearer {token}'
    const authHeader = req.headers.authorization;
    if (!authHeader) {
      return res.status(401).send({ message: 'No token provided' });
    }

    const token = authHeader.split(' ')[1]; // Split 'Bearer' from the token
    await db.user_tokens.destroy({
      where: { key: token }
    });
    res.send({ message: 'Logged out successfully' });
  } catch (error) {
    console.error('Logout Error:', error);
    res.status(500).send({ message: 'Error during logout' });
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
