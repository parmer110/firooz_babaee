const db = require("../models");
const Order_product = db.order;
const OrderProduct = db.orderProduct;
const Op = db.Sequelize.Op;
const config = require("../config/db.config");
const { QueryTypes } = require("sequelize");
const { order_product } = require("../models");
const WarehouseOrderProduct = db.WarehouseOrderProduct;
const Product = db.Product;



// Create and Save a new OrderProduct
exports.create = async (req, res) => {
  // Validate request
  if (!req.body.orderid || !req.body.gtin) {
    res.status(400).send({
      message: "Order ID and GTIN cannot be empty!",
    });
    return;
  }

  // Create a OrderProduct
  const orderProduct = {
    orderid: req.body.orderid,
    gtin: req.body.gtin,
  };

  // Save OrderProduct in the database
  try {
    const data = await OrderProduct.create(orderProduct);
    res.send(data);
  } catch (err) {
    res.status(500).send({
      message: err.message || "Some error occurred while creating the OrderProduct.",
    });
  }
};

// Retrieve all OrderProducts from the database.
// exports.findAll = (req, res) => {
//   const orderid = req.query.orderid;
//   console.log('Orderid is: '+orderid);
//   var condition = orderid ? { orderid: { [Op.like]: `%${orderid}%` } } : null;

//   Order_product.findAll({ where: condition })
//     .then((data) => {
//       res.send(data);
//     })
//     .catch((err) => {
//       res.status(500).send({
//         message: err.message || "Some error occurred while retrieving orderProductss.",
//       });
//     });
// };

// Find a single OrderProduct with an id

// Retrieve all OrderProducts from the database
exports.findAll = async (req, res) => {
  const orderid = req.query.orderid;
  const condition = orderid ? { orderid: { [Op.like]: `%${orderid}%` } } : null;

  try {
    const data = await OrderProduct.findAll({ where: condition });
    res.send(data);
  } catch (err) {
    res.status(500).send({
      message: err.message || "Some error occurred while retrieving OrderProducts."
    });
  }
};

exports.findAllWithJoinProducts = async (req, res) => {
  const _orderid = req.query["orderid"];

  try {
    const data = await WarehouseOrderProduct.findAll({
      where: _orderid ? { orderid: _orderid } : {}, // شرط بندی فقط در صورتی که _orderid وجود داشته باشد
      include: [{
        model: Product, // اطمینان حاصل کنید که ارتباط در مدل ها تعریف شده است
        attributes: ['productfrname'], // فقط نام محصول را دریافت می‌کنیم
        on: {
          col1: db.sequelize.where(db.sequelize.col("WarehouseOrderProduct.gtin"), '=', db.sequelize.col("Product.gtin"))
        }
      }],
      attributes: ['id', 'orderid', 'gtin'] // مشخص کردن فیلدهایی که می‌خواهیم برگردانده شوند
    });
    res.send(data);
  } catch (err) {
    res.status(500).send({
      message: err.message || "Some error occurred while retrieving orders."
    });
  }
};

exports.findOne = async (req, res) => {
  const id = req.params.id;

  try {
    const data = await Order_product.findByPk(id);
    if (data) {
      res.send(data);
    } else {
      res.status(404).send({
        message: `No OrderProduct found with the id=${id}.`
      });
    }
  } catch (err) {
    res.status(500).send({
      message: `Error retrieving OrderProduct with id=${id}: ${err.message}`
    });
  }
};

// Find a single OrderProduct with an id
exports.findOneCount = async (req, res) => {
  const _orderid = req.body.orderid;

  try {
    const count = await Order_product.count({
      where: { orderid: _orderid }
    });

    res.send({ qty: count });
  } catch (err) {
    res.status(500).send({
      message: `Error retrieving OrderProduct count with orderid=${_orderid}: ${err.message}`,
    });
  }
};

exports.update = async (req, res) => {
  const id = req.params.id;

  try {
    // ابتدا بررسی کنید که آیا OrderProduct با ID مورد نظر وجود دارد
    const orderProduct = await Order_product.findByPk(id);
    if (!orderProduct) {
      return res.status(404).send({
        message: `OrderProduct with id=${id} not found.`
      });
    }

    // بروزرسانی OrderProduct با استفاده از فیلدهای موجود در body درخواست
    const { gtin, otherFieldsIfNecessary } = req.body; // اطمینان حاصل کنید که فقط فیلدهای قابل به‌روزرسانی دریافت می‌شوند
    await orderProduct.update({ gtin, otherFieldsIfNecessary });

    res.send({
      message: "Order_product was updated successfully.",
    });
  } catch (err) {
    res.status(500).send({
      message: `Error updating OrderProduct with id=${id}: ${err.message}`,
    });
  }
};

// Delete an Order_product with the specified id in the request
exports.delete = async (req, res) => {
  const id = req.params.id;

  try {
    const num = await Order_Product.destroy({
      where: { id: id },
    });

    if (num === 1) {
      res.send({
        message: "Order_product was deleted successfully!",
      });
    } else {
      res.status(404).send({
        message: `Cannot delete Order_product with id=${id}. Maybe Order_product was not found!`,
      });
    }
  } catch (err) {
    res.status(500).send({
      message: `Could not delete Order_product with id=${id}: ${err.message}`,
    });
  }
};

// Delete all Orders from the database.
exports.deleteAll = async (req, res) => {
  try {
    const nums = await Order_product.destroy({
      where: {},
      truncate: false,
    });

    res.send({
      message: `${nums} Order_products were deleted successfully!`,
    });
  } catch (err) {
    res.status(500).send({
      message: err.message || "Some error occurred while removing all order_products.",
    });
  }
};
