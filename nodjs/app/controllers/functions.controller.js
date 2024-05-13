const db = require("../models");
const { WhUser, User_token } = require("./user_token.controller");
require('dotenv').config({ path: `${process.cwd()}/../.env` });
const jwt = require('jsonwebtoken');

async function InsertOrUpdateUserToken(userId) {
  let jwtSecretKey = process.env.JWT_SECRET_KEY;
  let data = {
    time: Date(),
    userId: userId,
  };
  const token = jwt.sign(data, jwtSecretKey);
  // Create a User
  const user_token = {
    // id: req.body.id,
    whUserId: userId,
    key: token
  };

  // Check if userid exists in whusers table
  return WhUser.findOne({ where: { id: userId } }) // add return here
    .then(user => {
      if (user) {
        // Find or create user_token in the database
        return User_token.findOrCreate({ where: { whUserId: userId }, defaults: user_token }) // add return here
          .then(([data, created]) => {
            if (created) {
              // Return the new user_token
              // console.log(`INSIDE CREATED:\n ${data}`);
              return (data.key); // add return here
            } else {
              // Update the existing user_token with the new key
              return data.update({ key: token }) // add return here
                .then(updated => {
                  // Return the updated user_token
                  console.log("Updated user_ token with new key " + token);
                  return (token); // add return here
                })
                .catch(err => {
                  return ({ // add return here
                    message: err.message || "Some error occurred while updating the UserToken."
                  });
                });
            }
          })
          .catch(err => {
            return res.status(500).send({ // add return here
              message: err.message || "Some error occurred while finding or creating the UserToken."
            });
          });
      } else {
        // Return error if userid does not exist
        return ({ // add return here
          message: "User id does not exist in WhUsers table."
        });
      }
    })
    .catch(err => {
      return res.status(500).send({ // add return here
        message: err.message || "Some error occurred while checking the user id."
      });
    });
}


exports.InsertOrUpdateUserToken = InsertOrUpdateUserToken;

async function checkTheUserToken(req) {
  try {
    let tokenHeaderKey = process.env.TOKEN_HEADER_KEY;
    const _token = req.get(tokenHeaderKey);
    // console.log("token: " + _token+"\n");
    // decode the token
    const decoded = jwt.decode(_token);
    const userId = decoded.userId;


    // check if the token exists in the database
    const userToken = await db.user_tokens.findOne({ where: { whUserId: userId, key: _token } });
    return userToken;
  } catch (error) {
    console.log(error);
    return null;
  }
}
exports.checkTheUserToken = checkTheUserToken;

