const db = require("../models");
const { QueryTypes } = require("sequelize");
const config = require("../config/db.config");
const Ongoingbarcode = db.barcode;
const ScanLog = db.scanlog;
const Op = db.Sequelize.Op;
const Order = db.Order;

// Create and Save a new Ongoingbarcode
exports.create = async (req, res) => {
  // Validate request
  if (!req.body.uuid) {
    return res.status(400).send({ message: "UUID cannot be empty!" });
  }

  // Construct a new Ongoingbarcode object
  const newOngoingbarcode = {
    id: req.body.id,
    orderid: req.body.orderid,
    levelid: req.body.levelid,
    parent: req.body.parent,
    uuid: req.body.uuid,
    rndesalat: req.body.rndesalat,
    orderserial: req.body.orderserial,
    favoritecode: req.body.favoritecode,
  };

  try {
    const data = await Ongoingbarcode.create(newOngoingbarcode);
    res.send(data);
  } catch (err) {
    res.status(500).send({
      message: err.message || "Some error occurred while creating the Ongoingbarcode."
    });
  }
};

// Retrieve all Ongoingbarcodes from the database.
exports.findAll = async (req, res) => {
  const { uuid, favoritecode } = req.query;
  let condition = {};

  if (uuid) {
    condition.uuid = { [Op.like]: `%${uuid}%` };
  }

  if (favoritecode) {
    condition.favoritecode = { [Op.like]: `%${favoritecode}%` };
  }

  try {
    const data = await Ongoingbarcode.findAll({ where: condition });
    res.send(data);
  } catch (err) {
    res.status(500).send({
      message: err.message || "Some error occurred while retrieving ongoingbarcodes."
    });
  }
};

// Find a single Ongoingbarcode with a UUID
exports.findOne = async (req, res) => {
  const _uuid = req.params.uuid;

  try {
    const data = await Ongoingbarcode.findOne({ where: { uuid: _uuid } });
    if (data) {
      res.send(data);
    } else {
      res.status(404).send({ message: "Ongoingbarcode not found with uuid=" + _uuid });
    }
  } catch (err) {
    res.status(500).send({
      message: "Error retrieving Ongoingbarcode with uuid=" + _uuid + ": " + err.message,
    });
  }
};

// Update an existing Ongoingbarcode by the uuid in the request
exports.update = async (req, res) => {
  const uuid = req.params.uuid;

  // Optionally validate req.body here
  if (Object.keys(req.body).length === 0) {
    return res.status(400).send({ message: "Data to update cannot be empty!" });
  }

  try {
    const num = await Ongoingbarcode.update(req.body, {
      where: { uuid: uuid },
    });
    
    if (num == 1) {
      res.send({
        message: "Ongoingbarcode was updated successfully.",
      });
    } else {
      res.send({
        message: `Cannot update Ongoingbarcode with uuid=${uuid}. Maybe Ongoingbarcode was not found or req.body is empty!`,
      });
    }
  } catch (err) {
    res.status(500).send({
      message: `Error updating Ongoingbarcode with uuid= ${uuid}: ${err.message}`,
    });
  }
};

exports.updatefavcode = async (req, res) => {
  const { uuid, favoritecode, userid, state, orderType, checkTheFollow } = req.body;

  try {
    const result = await db.sequelize.transaction(async (t) => {
      const levelId = uuid.substr(5, 1);

      let ongoingCheck = await Ongoingbarcode.findOne({
        where: { uuid },
        transaction: t
      });

      if (!ongoingCheck) {
        let barcodeCheck = await Ongoingbarcode.findOne({
          where: { uuid: uuid.substr(5, 15) },
          transaction: t
        });
        if (!barcodeCheck) {
          return res.status(404).send({ message: "Barcode not found." });
        }

        // Implementing the CheckUidByOrderType logic here
        let followResult = await checkUidByOrderType(uuid, orderType, t);

        if (checkTheFollow === 'TRUE' && followResult === 'Duplicate' && state === 'ADD') {
          return res.send({ result: 'duplicate', orderid: barcodeCheck.orderid });
        } else {
          return res.send({ result: 'notStarted', orderid: barcodeCheck.orderid });
        }
      } else {
        let followResult = await checkUidByOrderType(uuid, orderType, t);

        if (checkTheFollow === 'TRUE' && followResult === 'Duplicate' && state === 'ADD') {
          return res.send({ result: 'duplicate', orderid: ongoingCheck.orderid });
        } else {
          return res.send({ result: 'ok', orderid: ongoingCheck.orderid });
        }
      }
    });
  } catch (error) {
    console.error('Error during the transaction:', error);
    res.status(500).send(error);
  }
};

// Helper function to simulate CheckUidByOrderType
async function checkUidByOrderType(uuid, currentOrderType, transaction) {
  try {
      // با استفاده از جوین و زیرپرسمان، آخرین نوع سفارش را بر اساس UUID می‌یابیم
      const lastOrder = await ScanLog.findOne({
          where: { uuid },
          include: [{
              model: db.WarehouseOrder,
              attributes: ['OrderType'],
          }],
          order: [['createdAt', 'DESC']],
          transaction
      });

      if (!lastOrder || !lastOrder.WarehouseOrder) {
          return 'notExist';
      }

      const orderType = lastOrder.WarehouseOrder.OrderType || '';

      // بررسی شرایط بر اساس نوع سفارش فعلی و آخرین نوع سفارش ثبت شده
      switch (currentOrderType) {
          case 'incoming':
              if (orderType === '') return 'OK';
              if (['outgoing', 'returning'].includes(orderType)) return 'FollowError';
              if (orderType === 'incoming') return 'Duplicate';
              break;
          case 'outgoing':
              if (orderType === '') return 'FollowError';
              if (['incoming', 'returning'].includes(orderType)) return 'OK';
              if (orderType === 'outgoing') return 'Duplicate';
              break;
          case 'returning':
              if (['incoming', ''].includes(orderType)) return 'FollowError';
              if (orderType === 'returning') return 'Duplicate';
              if (orderType === 'outgoing') return 'OK';
              break;
          default:
              return 'notExist';
      }
  } catch (error) {
      console.error('Error in checkUidByOrderType:', error);
      throw error;
  }
}

exports.countOrder = async (req, res) => {
  const { whorderid, orderType } = req.body;
  console.log(`Inside countOrder for whorderid=${whorderid}, orderType=${orderType}`);

  try {
    let count;
    switch (orderType) {
      case "outgoing":
        count = await Ongoingbarcode.count({ where: { whorderid: whorderid, levelid: 0 } });
        break;
      default:
        count = await ScanLog.count({ where: { whorderid: whorderid } });
        break;
    }
    res.json({ count: count });
  } catch (err) {
    console.error(err);  // لاگ خطا در کنسول
    res.status(500).send({ message: `Error retrieving count for orderType=${orderType}: ${err.message}` });
  }
};

exports.countOrderLevels = async (req, res) => {
  const { whorderid, orderType } = req.body;

  try {
    let data;
    switch (orderType) {
      case "outgoing":
        // Using Sequelize model to query Ongoingbarcode
        data = await Ongoingbarcode.findAll({
          attributes: [
            [Sequelize.fn('COALESCE', Sequelize.col('levelid'), 0), 'levelid'],
            [Sequelize.fn('COUNT', Sequelize.col('levelid')), 'count']
          ],
          where: {
            [Sequelize.Op.or]: [
              { whorderid: whorderid },
              { levelid: { [Sequelize.Op.is]: null } }
            ]
          },
          group: [Sequelize.fn('COALESCE', Sequelize.col('levelid'), 0)],
          raw: true
        });
        break;
      default:
        // Using Sequelize model to query ScanLog
        data = await ScanLog.findAll({
          attributes: [
            [Sequelize.fn('COALESCE', Sequelize.fn('substring', Sequelize.col('uuid'), 6, 1), 0), 'levelid'],
            [Sequelize.fn('COUNT', Sequelize.col('uuid')), 'count']
          ],
          where: {
            [Sequelize.Op.or]: [
              { whorderid: whorderid },
              { uuid: { [Sequelize.Op.is]: null } }
            ]
          },
          group: [Sequelize.fn('COALESCE', Sequelize.fn('substring', Sequelize.col('uuid'), 6, 1), 0)],
          raw: true
        });
    }

    res.send(data);
  } catch (error) {
    console.error('Error during the query or connection:', error);
    res.status(500).send({
      message: "Error retrieving data",
    });
  }
};

async function isRndEsalatFound(key) {
  console.log("isRndEsalatFound", key);
  const count = await Ongoingbarcode.count({ where: { rndesalat: key } });
  if (count === 0) {
    console.log("No rndesalat found for key " + key);
    return false;
  } else {
    console.log("Found rndesalat with count: " + count);
    return true;
  }
}

async function isBarcodeFound(key) {
  console.log("isBarcodeFound", key);
  const _key = key.substring(18, 38);  // Ensure this index slicing is correct based on your data format.
  const count = await Ongoingbarcode.count({ where: { uuid: _key } });
  if (count === 0) {
    console.log("No uuid found for key " + _key);
    return false;
  } else {
    console.log("Found uuid with count: " + count);
    return true;
  }
}

async function isBarcodeFound(key) {
  console.log("isBarcodeFound", key);
  const extractedKey = key.substring(18, 38); // Ensure the substring indices are correct for your key structure.
  const result = await Ongoingbarcode.findOne({ where: { uuid: extractedKey } });
  if (result === null) {
    console.log("No uuid found for key " + extractedKey);
    return false;
  } else {
    console.log("Found uuid " + result.uuid);
    return true;
  }
}

async function checkFound(method, key) {
  switch (method) {
    case "rndEsalat":
      return await isRndEsalatFound(key);
    case "uuid":
      return await isUuidFound(key);
    case "barcode":
      return await isBarcodeFound(key);
    default:
      return false;
  }
}

exports.trackBarcode = async (req, res) => {
  const { userId, method, key } = req.body;
  console.log(key, method, userId);
  
  const found = await checkFound(method, key);
  if (found) {
    console.log("Found");
    res.send("Found");
  } else {
    console.log("Not Found");
    res.send("Not Found");
  }
};

// Delete an Ongoingbarcode with the specified nationalid in the request
exports.delete = (req, res) => {
  const nationalid = req.params.nationalid;

  Ongoingbarcode.destroy({
    where: { nationalid: nationalid }
  })
    .then(num => {
      if (num === 1) {
        res.send({
          message: "Ongoingbarcode was deleted successfully!",
        });
      } else {
        res.send({
          message: `Cannot delete Ongoingbarcode with nationalid=${nationalid}. Maybe Ongoingbarcode was not found!`
        });
      }
    })
    .catch(err => {
      res.status(500).send({
        message: "Could not delete Ongoingbarcode with nationalid=" + nationalid,
      });
    });
};

// Delete all Ongoingbarcodes from the database using truncate for efficiency.
exports.deleteAll = (req, res) => {
  Ongoingbarcode.destroy({
    where: {},
    truncate: true  // Truncates the table, which can be faster and resets auto-incrementing keys.
  })
    .then(() => {
      res.send({
        message: "All Ongoingbarcodes were deleted successfully!",
      });
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message ||
          "Some error occurred while removing all ongoingbarcodes.",
      });
    });
};

// find all published Ongoingbarcode
exports.findAllPublished = (req, res) => {
  Ongoingbarcode.findAll({ where: { published: true } })
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      res.status(500).send({
        message:
          err.message ||
          "Some error occurred while retrieving ongoingbarcodes.",
      });
    });
};

exports.findChildren = (req, res) => {
  const _uuid = req.query.uuid;
  if (!_uuid) {
    return res.status(400).send({ message: "UUID must be provided." });
  }
  console.log('Finding children of UUID:', _uuid);
  
  Ongoingbarcode.findAll({ where: { parent: _uuid } })
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      console.error("Error while retrieving children list:", err);
      res.status(500).send({
        message:
          "Some error occurred while retrieving children list.",
      });
    });
};

exports.warehouseOrderProductCount = async (req, res) => {
  const { uuid, favoritecode } = req.body;

  try {
    const result = await sequelize.transaction(async (t) => {
      // Finding the orderId from the OngoingBarcodes model
      const ongoingBarcode = await Ongoingbarcode.findOne({
        where: { uuid: uuid },
        attributes: ['orderid'],
        transaction: t
      });

      if (!ongoingBarcode) {
        throw new Error("No ongoing barcode found.");
      }

      const orderId = ongoingBarcode.orderid;

      // Getting the product code from the orders model
      const order = await Order.findOne({
        where: { ordercode: orderId },
        attributes: ['productcode'],
        transaction: t
      });

      if (!order) {
        throw new Error("Order not found.");
      }

      const productCode = order.productcode;

      // Counting the products with the same product code and favorite code at levelId = 0
      const productCount = await Ongoingbarcode.count({
        where: {
          whorderid: favoritecode,
          orderid: orderId,
          levelid: 0,
          '$order.productcode$': productCode
        },
        include: [{
          model: Order,
          attributes: [],
          where: { productcode: productCode }
        }],
        transaction: t
      });

      return { result: 'ok', orderid: orderId, productcount: productCount };
    });

    res.send(result);
  } catch (error) {
    console.error('Error during the transaction:', error);
    res.status(500).send({
      message: error.message || "Error retrieving product count",
    });
  }
};

exports.getBarcodeFromUid = async (req, res) => {
  const { uuid } = req.body;

  try {
    // ابتدا UUID را بررسی می‌کنیم
    const barcodeData = await Barcode.findOne({
      where: {
        uuid: uuid.length === 15 ? uuid : { [Op.substring]: uuid.slice(5, 20) }
      },
      include: [{
        model: Order,
        attributes: ['ProductCode', 'ExpDate', 'BatchNumber', 'OrderId']
      }]
    });

    if (!barcodeData) {
      throw new Error("Barcode not found.");
    }

    // تولید GTIN برای بارکد
    let gtin = barcodeData.Order.ProductCode;
    if (gtin.length < 14) {
      gtin = barcodeData.LevelId + gtin.padStart(13, '0');
    } else {
      gtin = barcodeData.LevelId + gtin.substring(1);
    }

    // فرمت تاریخ انقضا
    const expDate = makeExpForBarcode(barcodeData.Order.ExpDate);

    // تولید بارکد نهایی
    const barcode = `01${gtin}21${uuid}17${expDate}10${barcodeData.Order.BatchNumber}`;

    res.send({ barcode });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).send({ message: error.message });
  }
};

function makeExpForBarcode(expDate) {
  if (!expDate || expDate.trim() === 'NE') {
    return '000000';
  }
  let [year, month, day] = expDate.split('/');
  month = month.padStart(2, '0');
  day = day.padStart(2, '0');
  return year.slice(-2) + month + day;
}
