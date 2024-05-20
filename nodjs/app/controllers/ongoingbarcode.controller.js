const db = require("../models");
const { QueryTypes } = require("sequelize");
const config = require("../config/db.config");
const Ongoingbarcode = db.barcode;
const ScanLog = db.scanlog;
const Op = db.Sequelize.Op;
const Order = db.Order;
const WarehouseOrder = db.WarehouseOrder;
const sequelize = db.sequelize;

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

// Helper function to simulate CheckUidByOrderType
const checkUidByOrderType = async (uuid, currentOrderType, transaction) => {
  const lastOrder = await ScanLog.findOne({
    attributes: ['whOrderId'],
    include: [{
      model: WarehouseOrder,
      attributes: ['ordertype']
    }],
    where: { uuid },
    order: [['whOrderId', 'DESC']],
    transaction
  });

  if (!lastOrder) return 'OK';

  const lastOrderType = lastOrder.WarehouseOrder.ordertype;

  switch (currentOrderType) {
    case 'incoming':
      if (!lastOrderType) return 'OK';
      if (['outgoing', 'returning'].includes(lastOrderType)) return 'FollowError';
      if (lastOrderType === 'incoming') return 'Duplicate';
      break;
    case 'outgoing':
      if (!lastOrderType) return 'FollowError';
      if (['incoming', 'returning'].includes(lastOrderType)) return 'OK';
      if (lastOrderType === 'outgoing') return 'Duplicate';
      break;
    case 'returning':
      if (lastOrderType === 'returning') return 'Duplicate';
      if (['incoming', ''].includes(lastOrderType)) return 'FollowError';
      if (lastOrderType === 'outgoing') return 'OK';
      break;
    default:
      return 'notExist';
  }

  return 'notExist';
};

const getRecursiveBarcodes = async (uuid, transaction) => {
  const barcodes = [];

  const getBarcodes = async (uuid, levelNum) => {
    try {
      const children = await db.barcode.findAll({
        where: { parent: uuid },
        attributes: ['uuid', 'levelid'],
        transaction: transaction
      });

      for (const child of children) {
        if (!child || !child.uuid) {
          continue;
        }

        barcodes.push({ Barcode: child.uuid, LevelNum: levelNum });

        await getBarcodes(child.uuid, levelNum - 1);
      }
    } catch (error) {
      console.error(`Error fetching barcodes: ${error.message}`);
      console.error(`Stack trace: ${error.stack}`);
      throw error;
    }
  };

  const levelId = parseInt(uuid.substr(5, 1), 10);
  barcodes.push({ Barcode: uuid, LevelNum: levelId });

  await getBarcodes(uuid, levelId - 1);
  return barcodes;
};

const calculateChildrenCount = async (uuid, transaction) => {
  let count = 0;

  const getChildren = async (uuid) => {
    const children = await Ongoingbarcode.findAll({
      where: { parent: uuid },
      attributes: ['uuid'],
      transaction
    });

    count += children.length;

    for (const child of children) {
      await getChildren(child.uuid);
    }
  };

  await getChildren(uuid);
  return count;
};

// Update an existing Ongoingbarcode by the uuid in the request when scanning a specific  barcode
exports.updatefavcode = async (req, res) => {
  const { uuid, favoritecode, userid, state, orderType, checkTheFollow } = req.body;
  const levelId = parseInt(uuid.substr(5, 1), 10);

  try {
    const result = await db.sequelize.transaction(async (t) => {
      const ongoingCheck = await Ongoingbarcode.findOne({
        where: { uuid },
        transaction: t
      });
      
      let orderid = '';
      let gtin = '';
      let childrenCount = 0;
      let productCount = 0;
      let levelCounts = Array(10).fill(0);

      const followResult = await checkUidByOrderType(uuid, orderType, t);
      if (!ongoingCheck) {
        const barcodeCheck = await Ongoingbarcode.findOne({
          where: { uuid: uuid.substr(5, 15) },
          transaction: t
        });

        if (!barcodeCheck) {
          return res.json([
            [
              {
                result: 'notFound',
                orderid,
                gtin,
                childrencount: childrenCount,
                productcount: productCount,
                level2count: levelCounts[2],
                level1count: levelCounts[1],
                level0count: levelCounts[0]
              }
            ]
          ]);
        }

      }

      orderid = ongoingCheck.getDataValue('orderId').toString();

      if (checkTheFollow === 'TRUE' && followResult === 'Duplicate' && state === 'ADD') {
        const order = await Order.findOne({
          where: { OrderCode: orderid },
          attributes: ['ProductCode'],
          transaction: t
        });
        gtin = order ? order.getDataValue('ProductCode') : '';

        return res.json([
          [
            {
              result: 'duplicate',
              orderid,
              gtin,
              childrencount: childrenCount,
              productcount: productCount,
              level2count: levelCounts[2],
              level1count: levelCounts[1],
              level0count: levelCounts[0]
            }
          ]
        ]);
      }

      const order = await Order.findOne({
        where: { OrderCode: orderid },
        attributes: ['ProductCode'],
        transaction: t
      });
      gtin = order ? order.getDataValue('ProductCode') : '';

      if (state === 'ADD') {
        if (checkTheFollow === 'TRUE' && followResult === 'OK') {
          const rec = await getRecursiveBarcodes(uuid, t);

          for (let i = 0; i < 10; i++) {
            levelCounts[i] = rec.filter(r => r.LevelNum === i).length;
          }

          if (orderType === 'outgoing') {
            await Ongoingbarcode.update({
              whOrderId: favoritecode,
              whUserId: userid,
              whScanDate: new Date()
            }, {
              where: {
                uuid: {
                  [Op.in]: rec.map(r => r.Barcode)
                },
                whOrderId: null
              },
              transaction: t
            });

            await Ongoingbarcode.update({
              whOrderId: favoritecode,
              whUserId: userid,
              whScanDate: new Date()
            }, {
              where: { uuid },
              transaction: t
            });
          }

          await ScanLog.bulkCreate(rec.map(r => ({
            whOrderId: favoritecode,
            whUserId: userid,
            uuid: r.Barcode,
            createdAt: new Date()
          })), { transaction: t });

          childrenCount = await calculateChildrenCount(uuid, t);

          const whereConditions = {
            whOrderId: favoritecode,
            uuid: {
              [Op.in]: rec.map(r => r.Barcode),
              [Op.like]: '_____0%'
            }
          };
                    
          if (orderType === 'incoming') {
            productCount = await ScanLog.count({
              where: whereConditions,
              transaction: t
            });
          } else if (orderType === 'outgoing') {
            productCount = await ScanLog.count({
              where: {
                ...whereConditions,
                whOrderId: favoritecode
              },
              transaction: t
            });
          } else if (orderType === 'returning') {
            productCount = await ScanLog.count({
              where: whereConditions,
              transaction: t
            });
          }

          return res.json([
            [
              {
                result: 'ok',
                orderid,
                gtin,
                childrencount: childrenCount,
                productcount: productCount,
                level2count: levelCounts[2],
                level1count: levelCounts[1],
                level0count: levelCounts[0]
              }
            ]
          ]);
        } else {
          return res.json([
            [
              {
                result: 'notfound',
                orderid,
                gtin,
                childrencount: childrenCount,
                productcount: productCount,
                level2count: levelCounts[2],
                level1count: levelCounts[1],
                level0count: levelCounts[0]
              }
            ]
          ]);
        }
      }
    });

  } catch (error) {
    console.error('Error during the transaction:', error);
    return res.status(500).json({ error: error.message });
  }
};

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
    console.error(err);
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
      // Finding the OrderId from the OngoingBarcodes model
      const ongoingBarcode = await Ongoingbarcode.findOne({
        where: { uuid: uuid },
        attributes: ['OrderId'],
        transaction: t
      });

      if (!ongoingBarcode) {
        throw new Error("The barcode not found!");
      }

      const orderId = ongoingBarcode.OrderId;

      // Getting the product code from the orders model
      const order = await Order.findOne({
        where: { OrderCode: orderId },
        attributes: ['ProductCode'],
        transaction: t
      });

      if (!order) {
        throw new Error("Order not found.");
      }

      const productCode = order.ProductCode;

      console.log(`Order ID: ${orderId}, Product Code: ${productCode}`);

      // Counting the products with the same product code and favorite code at levelid = 0
      const productCount = await Ongoingbarcode.count({
        where: {
          WhOrderId: favoritecode,
          levelid: 0,
          OrderId: orderId, // Ensure this is included
        },
        include: [{
          model: Order,
          where: { ProductCode: productCode },
          attributes: []
        }],
        transaction: t
      });

      return [{ result: 'ok', orderid: orderId, productcount: productCount }];
    });
    res.send([result]);
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

    let gtin = barcodeData.Order.ProductCode;
    if (gtin.length < 14) {
      gtin = barcodeData.LevelId + gtin.padStart(13, '0');
    } else {
      gtin = barcodeData.LevelId + gtin.substring(1);
    }

    const expDate = makeExpForBarcode(barcodeData.Order.ExpDate);

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
