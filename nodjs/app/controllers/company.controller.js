const db = require("../models");
const Company = db.companies;
const Op = db.Sequelize.Op;
const { checkTheUserToken } = require("./functions.controller");
const logger = require('../config/logger');


// Create and Save a new Company
exports.create = (req, res) => {
  // Validate request
  if (!req.body.Orderid) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
    return;
  }

// Create a new company object
const newCompany = {
  nationalid: req.body.nationalid,
  companyfaname: req.body.companyfaname,
  prefix: req.body.prefix,
  defaultDc: req.body.defaultDc
};

// Save Company in the database
Company.create(newCompany)
  .then(data => {
    res.send(data);
  })
  .catch(err => {
    res.status(500).send({
      message:
        err.message || "Some error occurred while creating the Company."
    });
  });
};

// Retrieve all Orders from the database.
exports.findAll = async (req, res) => {

  console.log("Retrieving all Companies from the database");
  // logger.error(`Testing winston logger`);
  const userToken = await checkTheUserToken(req);
  try {
    if (userToken) {
      getCompaniesList(req, res);
    } else {
      // Access Denied 
      return res.status(401).send('Access Denied');
    }
  } catch (error) {
    // Access Denied 
    console.log(error);
    return res.status(401).send('Access Denied');
  }
};

// Find a single Company with an id
exports.findOne = (req, res) => {
  const nationalid = req.params.nationalid;

  Company.findByPk(nationalid)
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({
        message: "Error retrieving Company with id=" + nationalid
      });
    });
};

// Update an existing Company by the id in the request
exports.update = (req, res) => {
  const id = req.params.id;

  Company.update(req.body, {
    where: { nationalid: nationalid }
  })
    .then(num => {
      if (num == 1) {
        res.send({
          message: "Company was updated successfully."
        });
      } else {
        res.send({
          message: `Cannot update Company with nationalid=${nationalid}. Maybe Company was not found or req.body is empty!`
        });
      }
    })
    .catch(err => {
      res.status(500).send({
        message: "Error updating Company with nationalid=" + nationalid
      });
    });
};

// Delete an Company with the specified id in the request
exports.delete = (req, res) => {
  const nationalid = req.params.nationalid;

  Company.destroy({
    where: { nationalid: nationalid }
  })
    .then(num => {
      if (num == 1) {
        res.send({
          message: "Company was deleted successfully!"
        });
      } else {
        res.send({
          message: `Cannot delete Company with nationalid=${nationalid}. Maybe Company was not found!`
        });
      }
    })
    .catch(err => {
      res.status(500).send({
        message: "Could not delete Company with id=" + id
      });
    });
};

// Delete all Orders from the database.
exports.deleteAll = (req, res) => {
  Company.destroy({
    where: {},
    truncate: false
  })
    .then(nums => {
      res.send({ message: `${nums} Orders were deleted successfully!` });
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while removing all companies."
      });
    });
};

// find all published Company
exports.findAllPublished = (req, res) => {
  Company.findAll({ where: { published: true } })
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving companies."
      });
    });
};

function getCompaniesList(req, res) {
  const nationalid = req.query.nationalid;
  var condition = nationalid ? { nationalid: { [Op.like]: `%${nationalid}%` } } : null;
  
  Company.findAll({ where: condition })
    .then(data => {
      // تبدیل شناسه هر شرکت به رشته
      const formattedData = data.map(company => ({
        ...company.toJSON(),
        id: company.id.toString(),  // تبدیل شناسه به رشته
        prefix: parseInt(company.prefix, 10),
      }));
      res.send(formattedData);
    })
    .catch(err => {
      res.status(500).send({
        message: err.message || "Some error occurred while retrieving companies."
      });
    });
}
