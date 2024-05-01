const { checkTheUserToken } = require("../controllers/functions.controller.js");
module.exports = app => {
  const users = require("../controllers/user.controller.js");

  var router = require("express").Router();

  // Middleware for checking the token
  const checkToken = async (req, res, next) => {
    console.log("Checking the user token");
    const userToken = await checkTheUserToken(req);
    if (!userToken) {
      // Access Denied 
      console.log('Access Denied');
      return res.status(401).send('Access Denied');
    }
    next();
  };

  // Retrieve all Users
  router.get("/", checkToken, users.findAll); //NEED TOKEN

  // Insert a new User 
  router.post("/insert", users.insert);

  // Insert a new User 
  router.post("/inquiry", users.inquiry);

  // Logout User
  router.post("/logout", checkToken, users.logout);

  app.use('/api/Users', router);
};
