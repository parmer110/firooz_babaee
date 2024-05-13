const db = require("../models");
const Product = db.products;
const Op = db.Sequelize.Op;
const { checkTheUserToken } = require("./functions.controller");

// Create and Save a new Product
exports.create = (req, res) => {
  // Validate request
  if (!req.body.id) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
    return;
  }

  // Create a Product
  const Product = {
    gtin: req.body.gtin,
    // id: req.body.id,
    productfrname: req.body.productfrname,
    irc: req.body.irc,
    producercompanycode: req.body.producercompanycode,
  };

  // Save Product in the database
  Product.create(product)
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while creating the Product."
      });
    });
};

exports.controllerSelector = async (req, res) => {

}
exports.findAll = async (req, res) => {
  console.log("Retrieving all Products from the database");
      getProductsList(req, res);
};

function getProductsList(req, res) {
  const gtin = req.query.gtin;
  var condition = gtin ? { gtin: { [Op.like]: `%${gtin}%` } } : null;
  
  Product.findAll({ where: condition })
    .then(data => {
      const formattedData = data.map(item => {
        return {
          id: item.id.toString(),
          gtin: item.GTIN ? item.GTIN.trim() : '',
          productfrname: item.ProductFrName,
          irc: item.irc,
          producercompanycode: item.ProducerCompanyCode ? item.ProducerCompanyCode.toString() : '',
          createdAt: item.createdAt.toISOString(),
          updatedAt: item.updatedAt.toISOString()
        };
      });
      res.send(formattedData);
    })
    .catch(err => {
      console.error(err);
      res.status(500).send({
        message: err.message || "Some error occurred while retrieving products."
      });
    });
}

// Find a single Product with a gtin
exports.findOne = (req, res) => {
  const gtin = req.params.gtin;

  Product.findByPk(gtin)
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({
        message: "Error retrieving Product with gtin=" + gtin
      });
    });
};

// Update an existing Product by the id in the request
exports.update = (req, res) => {
  const id = req.params.id;

  Product.update(req.body, {
    where: { id: id }
  })
    .then(num => {
      if (num == 1) {
        res.send({
          message: "Product was updated successfully."
        });
      } else {
        res.send({
          message: `Cannot update Product with id=${id}. Maybe Product was not found or req.body is empty!`
        });
      }
    })
    .catch(err => {
      res.status(500).send({
        message: "Error updating Product with id=" + id
      });
    });
};

// Delete an Product with the specified id in the request
exports.delete = (req, res) => {
  const id = req.params.id;

  Product.destroy({
    where: { id: id }
  })
    .then(num => {
      if (num == 1) {
        res.send({
          message: "Product was deleted successfully!"
        });
      } else {
        res.send({
          message: `Cannot delete Product with id=${id}. Maybe Product was not found!`
        });
      }
    })
    .catch(err => {
      res.status(500).send({
        message: "Could not delete Product with id=" + id
      });
    });
};

// Delete all Orders from the database.
exports.deleteAll = (req, res) => {
  Product.destroy({
    where: {},
    truncate: false
  })
    .then(nums => {
      res.send({ message: `${nums} Orders were deleted successfully!` });
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while removing all products."
      });
    });
};

// find all published Product
exports.findAllPublished = (req, res) => {
  Product.findAll({ where: { published: true } })
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving products."
      });
    });
};