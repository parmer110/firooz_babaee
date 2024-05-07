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
    password: await bcrypt.hash(req.body.password, 10), // Hashing the password
  };

  const sql = `INSERT INTO "WhUsers" ("fname", "lname", "username", "password", "phone", "createdAt", "updatedAt")
               VALUES (:fname, :lname, :username, :password, :phone, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
               RETURNING id;`;

  try {
    const result = await db.sequelize.query(sql, {
      replacements: user,
      type: db.Sequelize.QueryTypes.INSERT
    });
    // Modify response to mimic the old structure
    const response = [[{ ServerUserId: result[0][0].id }], result[1]];
    res.send(response);
  } catch (err) {
    console.error(err);
    res.status(500).send({ message: "Error inserting new user" });
  }
};

exports.inquiry = async (req, res) => {
  const jwtPrivateKey = privateKey
  const { username, password } = req.body;

  try {
    // Find the user in the database
    const user = await db.users.findOne({ where: { username } });
    if (!user) {
      return res.send([{ result: 'notfound' }]);
    }

    // Compare hashed password with the provided password
    const isPasswordMatch = await bcrypt.compare(password, user.password);

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
