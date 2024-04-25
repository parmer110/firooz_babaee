const db = require("../models");
const Order = db.orders;
const Op = db.Sequelize.Op;
const config = require("../config/db.config");
const { Sequelize, QueryTypes } = require("sequelize");
const sequelize = require('../config/database.js');


// Create and Save a new Order
exports.create = (req, res) => {
  // Validate request
  if (!req.body.orderid) {
    res.status(400).send({
      message: "Order ID cannot be empty!",
    });
    return;
  }

  // Create an Order
  const newOrder = {
    orderid: req.body.orderid,
    gtin: req.body.gtin,
    batchnumber: req.body.batchnumber,
    expdate: req.body.expdate,
    userid: req.body.userid,
    insertdate: req.body.insertdate,
    lastxmldate: req.body.lastxmldate,
    distributercompanynid: req.body.distributercompanynid,
    ordertype: req.body.ordertype,
    details: req.body.details,
  };

  // Save Order in the database
  Order.create(newOrder)
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      res.status(500).send({
        message: err.message || "Some error occurred while creating the Order.",
      });
    });
};

// Retrieve all Orders from the database.
exports.findAll = (req, res) => {
  const orderid = req.query.orderid;
  var condition = orderid ? { orderid: { [Op.like]: `%${orderid}%` } } : null;

  Order.findAll({ where: condition })
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      res.status(500).send({
        message: err.message || "Some error occurred while retrieving orders.",
      });
    });
};
exports.findAllByDeviceId = (req, res) => {
  const _deviceId = req.params.deviceid;
  // console.log(`_deviceId: ${_deviceId}`);
  Order.findAll({ where: { deviceId: _deviceId } })
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving Orders."
      });
    });
};

exports.UpdateOneByDeviceId = (req, res) => {
  const _deviceId = req.params.deviceid;
  const updateData = {
    // اطلاعاتی که قرار است به‌روزرسانی شود
    gtin: req.body.gtin,
    batchnumber: req.body.batchnumber,
    // دیگر فیلدها...
  };

  Order.update(updateData, { where: { deviceId: _deviceId } })
    .then(num => {
      if (num == 1) {
        res.send({ message: "Order was updated successfully." });
      } else {
        res.status(404).send({ message: `Cannot update Order. No Order found with deviceId=${_deviceId} or data is the same as existing.` });
      }
    })
    .catch(err => {
      res.status(500).send({
        message: `Error updating Order with deviceId=${_deviceId}`
      });
    });
};

// Find a single Order with an id
exports.findOne = (req, res) => {
  const id = req.params.id;

  Order.findByPk(id)
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      res.status(500).send({
        message: "Error retrieving Order with id=" + id,
      });
    });
};

// Find a single Order with an id for count
exports.findOneCount = async (req, res) => {
  const _whorderid = req.body.whorderid;

  try {
    const data = await sequelize.query(
      "SELECT COUNT(0) as qty FROM ongoingbarcodes WHERE whorderid = :whorderid AND LevelId = 0",
      { replacements: { whorderid: _whorderid }, type: QueryTypes.SELECT }
    );
    res.send(data);
  } catch (err) {
    res.status(500).send({
      message: "Error retrieving Order count with id=" + _whorderid + ": " + err.message,
    });
  }
};

// Find a distributer's name for an Order
exports.findOneDistributerName = async (req, res) => {
  const id = req.params.id;

  try {
    const order = await Order.findByPk(id);
    const data = await sequelize.query(
      "SELECT CompanyFaName FROM Companies WHERE NationalId = :NationalId",
      { replacements: { NationalId: order.distributercompanynid }, type: QueryTypes.SELECT }
    );
    res.send(data);
  } catch (err) {
    res.status(500).send({
      message: "Error retrieving Order's distributer name with id=" + id + ": " + err.message,
    });
  }
};

// Update an existing Order by the id in the request
exports.update = (req, res) => {
  // const id = req.params.id;
  const _orderid = req.params.orderid;

  Order.update({ deviceid: req.body.deviceid }, {
    where: { orderid: _orderid },
  })
    .then((num) => {
      if (num == 1) {
        res.send({
          message: "Order was updated successfully.",
        });
      } else {
        res.send({
          message: `Cannot update Order with orderid=${_orderid}. Maybe Order was not found or req.body is empty!`,
        });
      }
    })
    .catch((err) => {
      res.status(500).send({
        message: "Error updating Order with id=" + _orderid + " \\n  " + err.message,
      });
    });
};

// Delete an Order with the specified id in the request
exports.delete = async (req, res) => {
  const _orderId = req.params.orderId;
  
  try {
    // پیچیدگی‌های SQL به جای توضیحات بالا
    const sql = "تعریف کوئری مورد نظر";
    const result = await sequelize.query(sql, {
      replacements: { whOrderid: _orderId },
      type: QueryTypes.INSERT, // بررسی نوع عملیات
    });
    console.log(result);
    res.send(result);
  } catch (err) {
    console.error(err);
    res.status(500).send({
      message: `Error while deleting order with id=${_orderId}: ${err.message}`
    });
  }
};

// Delete all Orders from the database.
exports.deleteAll = (req, res) => {
  Order.destroy({
    where: {},
    truncate: false,
  })
    .then((nums) => {
      res.send({ message: `${nums} Orders were deleted successfully!` });
    })
    .catch((err) => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while removing all orders.",
      });
    });
};

// find all published Order
exports.findAllPublished = (req, res) => {
  Order.findAll({ where: { published: true } })
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      res.status(500).send({
        message: err.message || "Some error occurred while retrieving orders.",
      });
    });
};

exports.Insert = async (req, res) => {
  const { orderid, distributernid, qty, isNewOrder, deviceId, orderType, details, userid } = req.body;

  try {
    const result = await sequelize.transaction(async (t) => {
      if (isNewOrder) {
        const newOrderId = await sequelize.query("SELECT MAX(OrderId) + 1 as newOrderId FROM WarehouseOrders", { type: QueryTypes.SELECT, transaction: t });
        orderid = newOrderId[0].newOrderId || 1;
      }

      await Order.update(
        { DistributerCompanyNid: distributernid, DeviceId: deviceId, OrderType: orderType, Details: details, userId: userid },
        { where: { OrderId: orderid }, transaction: t }
      );

      await sequelize.query(
        "INSERT INTO WarehouseOrderLevels (OrderId, LevelId, NumberOfOrder) VALUES (:orderid, 0, :qty) ON DUPLICATE KEY UPDATE NumberOfOrder = :qty",
        { replacements: { orderid, qty }, transaction: t }
      );

      // Add more operations as needed
      return orderid;
    });

    res.send({ result: "Order processed successfully", orderid: result });
  } catch (err) {
    console.error(err);
    res.status(500).send({ message: "Error processing order: " + err.message });
  }
};

exports.updateStats = async (req, res) => {
  const orderStats = req.body;
  console.log(orderStats);  // در نظر داشته باشید که در محیط تولید، از خروجی‌های محرمانه جلوگیری شود.

  try {
    const promises = orderStats.map(async (element) => {
      const { whorderid, gtin, maxlimit: maxLimit } = element;
      const query = 'EXEC dbo.[spInsertStatsFromApp] @whorderid = :whorderid, @gtin= :gtin, @max= :max';
      return sequelize.query(query, {
        replacements: { whorderid, gtin, max: maxLimit },
        type: QueryTypes.INSERT,
      });
    });

    await Promise.all(promises);
    res.status(200).json({ message: 'All stats inserted successfully' });
  } catch (err) {
    console.error(err);  // چاپ خطا در کنسول برای تحلیل‌های بیشتر
    res.status(500).json({ message: 'Something went wrong', error: err.message });
  }
};
