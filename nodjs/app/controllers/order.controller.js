const db = require("../models");
const { orders: WarehouseOrder, order_product: WarehouseOrderProducts, 
  order_product_levels: WareHouseOrderLevels, BarCodes} = db;
const Op = db.Sequelize.Op;
const config = require("../config/db.config");
const { Sequelize, QueryTypes } = require("sequelize");
const sequelize = require('../config/database.js');


// Create and Save a new Order
exports.create = async (req, res) => {
  // Validate request
  if (!req.body.orderid) {
    return res.status(400).send({
      message: "Order ID cannot be empty!"
    });
  }

  // Create an Order object
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
    details: req.body.details
  };

  try {
    // Save Order in the database
    const data = await Order.create(newOrder);
    res.send(data);
  } catch (err) {
    res.status(500).send({
      message: err.message || "Some error occurred while creating the Order."
    });
  }
};

// Retrieve all Orders from the database.
exports.findAll = async (req, res) => {
  const orderid = req.query.orderid;
  const condition = orderid ? { orderid: { [Op.like]: `%${orderid}%` } } : null;

  try {
    const data = await Order.findAll({ where: condition });
    res.send(data);
  } catch (err) {
    res.status(500).send({
      message: err.message || "Some error occurred while retrieving orders."
    });
  }
};

// Retrieve all Orders by Device ID
exports.findAllByDeviceId = async (req, res) => {
  const _deviceId = req.params.deviceid;

  try {
    const data = await Order.findAll({ where: { deviceId: _deviceId } });
    res.send(data);
  } catch (err) {
    res.status(500).send({
      message: err.message || "Some error occurred while retrieving Orders."
    });
  }
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

// Find a single Order with an id using async/await
exports.findOne = async (req, res) => {
  const id = req.params.id;

  try {
    const data = await Order.findByPk(id);
    if (data) {
      res.send(data);
    } else {
      res.status(404).send({
        message: `Order with id=${id} not found.`
      });
    }
  } catch (err) {
    res.status(500).send({
      message: `Error retrieving Order with id=${id}: ${err.message}`
    });
  }
};

// Find the count of ongoing barcodes for a single Order
exports.findOneCount = async (req, res) => {
  const _whorderid = req.body.whorderid;

  try {
    const data = await sequelize.query(
      "SELECT COUNT(*) as qty FROM ongoingbarcodes WHERE whorderid = :whorderid AND LevelId = 0",
      { replacements: { whorderid: _whorderid }, type: QueryTypes.SELECT }
    );
    res.send(data[0]);
  } catch (err) {
    res.status(500).send({
      message: `Error retrieving Order count for id=${_whorderid}: ${err.message}`
    });
  }
};

// Find a distributor's name for an Order
exports.findOneDistributerName = async (req, res) => {
  const id = req.params.id;

  try {
    const order = await Order.findByPk(id);
    if (!order) {
      return res.status(404).send({
        message: `Order with id=${id} not found.`
      });
    }
    
    if (!order.distributercompanynid) {
      return res.status(404).send({
        message: `Distributor ID not found for Order with id=${id}.`
      });
    }

    const data = await sequelize.query(
      "SELECT CompanyFaName FROM Companies WHERE NationalId = :NationalId",
      { replacements: { NationalId: order.distributercompanynid }, type: QueryTypes.SELECT }
    );

    if (data.length > 0) {
      res.send(data[0]);
    } else {
      res.status(404).send({
        message: `Distributor not found for Order with id=${id}.`
      });
    }
  } catch (err) {
    res.status(500).send({
      message: `Error retrieving distributor's name for Order with id=${id}: ${err.message}`
    });
  }
};

// Update an existing Order by the id in the request
exports.update = async (req, res) => {
  const _orderid = req.params.orderid;

  try {
    const updated = await Order.update(req.body, {
      where: { orderid: _orderid }
    });

    if (updated[0] === 1) {
      res.send({
        message: "Order was updated successfully."
      });
    } else {
      res.status(404).send({
        message: `Cannot update Order with orderid=${_orderid}. Maybe Order was not found or no new data provided.`
      });
    }
  } catch (err) {
    res.status(500).send({
      message: `Error updating Order with orderid=${_orderid}: ${err.message}`
    });
  }
};

// Delete an Order with the specified id in the request
exports.delete = async (req, res) => {
  const _orderId = req.params.orderId;

  try {
    const num = await Order.destroy({
      where: { orderid: _orderId }
    });

    if (num === 1) {
      res.send({
        message: "Order was deleted successfully!"
      });
    } else {
      res.status(404).send({
        message: `Cannot delete Order with orderid=${_orderId}. Maybe Order was not found!`
      });
    }
  } catch (err) {
    res.status(500).send({
      message: `Error deleting Order with orderid=${_orderId}: ${err.message}`
    });
  }
};

// Delete all Orders from the database.
exports.deleteAll = async (req, res) => {
  const t = await db.sequelize.transaction();

  try {
    const nums = await Order.destroy({
      where: {},
      truncate: false,
      transaction: t
    });

    await t.commit();

    if (nums > 0) {
      res.send({ message: `${nums} Orders were deleted successfully!` });
    } else {
      res.send({ message: "No orders to delete." });
    }
  } catch (err) {
    await t.rollback();
    res.status(500).send({
      message: err.message || "Some error occurred while removing all orders."
    });
  }
};

// find all published Order
exports.findAllPublished = async (req, res) => {
  try {
    // Check if the 'published' attribute is part of the Order model
    if (!Order.rawAttributes.published) {
      return res.status(400).send({
        message: "Error: 'published' attribute does not exist on Order model."
      });
    }

    const data = await Order.findAll({
      where: { published: true }
    });

    if (data.length > 0) {
      res.send(data);
    } else {
      res.send({ message: "No published orders found." });
    }
  } catch (err) {
    res.status(500).send({
      message: err.message || "Some error occurred while retrieving published orders."
    });
  }
};

// افزودن یا به روز رسانی سطح سفارش
async function manageOrderLevels(orderId, transaction, numberOfOrder="", levelId="") {

  const existingLevel = await WareHouseOrderLevels.findOne({
    where: { orderId: orderId, LevelId: levelId },
    transaction
  });

  if (existingLevel) {
    await existingLevel.update({ NumberOfOrder: numberOfOrder }, { transaction });
  } else {
    await WareHouseOrderLevels.create({
      orderId: orderId,
      LevelId: levelId,
      NumberOfOrder: numberOfOrder
    }, { transaction });
  }
}

// افزودن یا به روز رسانی محصولات سفارش
async function manageOrderProducts(orderId, transaction, gtin="") {

  const existingProduct = await WarehouseOrderProducts.findOne({
    where: { orderId: orderId, Gtin: gtin },
    transaction
  });

  if (existingProduct) {
    // اگر محصول قبلا ثبت شده، به‌روزرسانی اطلاعات
    await existingProduct.update({ /* بروزرسانی داده‌ها */ }, { transaction });
  } else {
    // اگر محصول جدید است، ایجاد رکورد جدید
    await WarehouseOrderProducts.create({
      orderId: orderId,
      Gtin: gtin,
      /* دیگر فیلدها */
    }, { transaction });
  }
}

exports.Insert = async (req, res) => {
  const { distributernid, isNewOrder, deviceId, orderType, details, userid } = req.body;

  try {
    const transaction = await sequelize.transaction();

    const newId = (await WarehouseOrder.max('id', { transaction: transaction })) + 1 || 1;
    const effectiveOrderType = orderType || 'outgoing';

    let order = null;
    if (req.body.orderid) {
      order = await WarehouseOrder.findOne({ where: { OrderId: parseInt(req.body.orderid) }, transaction: transaction });
    }

    const lastOrder = await WarehouseOrder.findOne({ order: [['OrderId', 'DESC']] });
    const newOrderId = lastOrder ? lastOrder.OrderId + 1 : 1;

    if (isNewOrder && !order) {
      order = await WarehouseOrder.create({
        id: newId,
        OrderId: newOrderId,
        DistributerCompanyNid: distributernid || null,
        DeviceId,
        ordertype: orderType,
        details,
        userId: userid && userid !== '' ? parseInt(userid) : null
      }, { transaction: transaction });
    } else if (!isNewOrder && order) {
      await order.update({
        DistributerCompanyNid: distributorIdValue,
        DeviceId: deviceId,
        ordertype: orderType,
        details: details,
        userId: userIdValue
      }, { transaction: transaction });
    } else {
      await transaction.rollback();
      return res.status(404).send({ message: "Order condition not met or OrderId is missing in the update case" });
    }
    
    // console.log(Object.keys(WarehouseOrderProducts.rawAttributes));
    const relatedWarehouseOrderProducts = await WarehouseOrderProducts.findOne({
      where: { orderId: order.OrderId },
      transaction: transaction
    });

    const relatedWarehouseOrderLevels = await WareHouseOrderLevels.findOne({
      where: { orderId: order.OrderId },
      transaction: transaction
    });

    const Gtin = relatedWarehouseOrderProducts ? relatedWarehouseOrderProducts.Gtin : null;
    const NumberOfOrder = relatedWarehouseOrderLevels ? relatedWarehouseOrderLevels.NumberOfOrder : null;
    const LevelId = relatedWarehouseOrderLevels ? relatedWarehouseOrderLevels.LevelId : null;

    // کد مربوط به سطوح سفارش 
    await manageOrderLevels(order.OrderId, transaction, NumberOfOrder, LevelId);
    // کد مربوط به محصولات سفارش
    await manageOrderProducts(order.OrderId, transaction, Gtin);

    await transaction.commit();
    res.send([
        [
            { "result": order.OrderId }
        ]
    ]);
  } catch (err) {
    console.error(err);
    if (transaction) await transaction.rollback();
    res.status(500).send({ message: err.message || "Error processing order" });
  }
};

async function handleOrderProducts(whOrderId, transaction) {
  const barCodes = await OnGoingBarCodes.findAll({
      where: { WhOrderId: whOrderId },
      attributes: [[Sequelize.fn('DISTINCT', Sequelize.col('uuid')), 'GTIN']],
      transaction
  });

  for (let { GTIN } of barCodes) {
      const product = await WarehouseOrderProducts.findOne({
          where: { OrderId: whOrderId, Gtin: GTIN },
          transaction
      });

      let insertedWhOrderId = product ? product.id : await WarehouseOrderProducts.create({
          OrderId: whOrderId,
          Gtin: GTIN,
          createdAt: new Date()
      }, { transaction }).id;

      const levels = await OnGoingBarCodes.findAll({
          where: { WhOrderId: whOrderId, uuid: GTIN },
          attributes: [[Sequelize.fn('DISTINCT', Sequelize.col('levelid')), 'levelid']],
          transaction
      });

      for (let { levelid } of levels) {
          const countInLevel = await OnGoingBarCodes.count({
              where: { WhOrderId: whOrderId, LevelId: levelid, uuid: GTIN },
              transaction
          });

          const level = await WarehouseOrderProductLevels.findOne({
              where: { OrderProductid: insertedWhOrderId, Levelid: levelid },
              transaction
          });

          if (level) {
              await WarehouseOrderProductLevels.update({ qty: countInLevel }, {
                  where: { OrderProductid: insertedWhOrderId, Levelid: levelid },
                  transaction
              });
          } else {
              await WarehouseOrderProductLevels.create({
                  OrderProductid: insertedWhOrderId,
                  Levelid: levelid,
                  qty: countInLevel
              }, { transaction });
          }
      }
  }
}

exports.updateStats = async (req, res) => {
  const orderStats = req.body;
  console.log(orderStats);  // Consider security best practices for production environments.

  try {
    const promises = orderStats.map((element) => {
      const { whorderid, gtin, maxlimit: maxLimit } = element;
      // Assuming you have a corresponding function or a directly executable query in PostgreSQL.
      const query = 'SELECT * FROM updateStatsFromApp(:whorderid, :gtin, :max);';
      return sequelize.query(query, {
        replacements: { whorderid, gtin, max: maxLimit },
        type: QueryTypes.SELECT, // Changed to SELECT assuming a function is being called.
      });
    });

    await Promise.all(promises);
    res.status(200).json({ message: 'All stats updated successfully' });
  } catch (err) {
    console.error(err);  // Log detailed error for further analysis
    res.status(500).json({ message: 'Something went wrong', error: err.message });
  }
};
