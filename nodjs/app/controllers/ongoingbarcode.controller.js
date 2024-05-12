const db = require("../models");
const { QueryTypes } = require("sequelize");
const config = require("../config/db.config");
const Ongoingbarcode = db.ongoingbarcodes;
const ScanLog = db.scanlog;
const Op = db.Sequelize.Op;

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
    const sql = `CALL UpdateFavCodeProcedure(:uuid, :favoritecode, :userid, :state, :orderType, :checkTheFollow);`;

    const result = await sequelize.query(sql, {
      replacements: { uuid, favoritecode, userid, state, orderType, checkTheFollow },
      type: QueryTypes.UPDATE
    });

    // ارسال پاسخ با تعداد رکوردهای تغییر یافته
    res.send({ updatedRows: result[1], message: "Favorite code updated successfully" });
  } catch (err) {
    console.error(err);
    res.status(500).send({ message: `An error occurred during the operation: ${err.message}` });
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
    console.error(err);  // لاگ خطا در کنسول
    res.status(500).send({ message: `Error retrieving count for orderType=${orderType}: ${err.message}` });
  }
};

exports.countOrderLevels = async (req, res) => {
  const { whorderid, orderType } = req.body;

  try {
    let data;
    if (orderType === "outgoing") {
      data = await Ongoingbarcode.findAll({
        where: { whorderid },
        attributes: [
          [sequelize.fn('COALESCE', sequelize.col('levelid'), 0), 'levelid'],
          [sequelize.fn('COUNT', sequelize.col('levelid')), 'count']
        ],
        group: ['levelid']
      });
    } else {
      data = await ScanLog.findAll({
        where: { whorderid },
        attributes: [
          [sequelize.fn('COALESCE', sequelize.fn('substring', sequelize.col('uuid'), 6, 1), 0), 'levelid'],
          [sequelize.fn('COUNT', sequelize.col('uuid')), 'count']
        ],
        group: [sequelize.fn('substring', sequelize.col('uuid'), 6, 1)]
      });
    }

    res.json(data);
  } catch (err) {
    console.error(err);
    res.status(500).send({ message: `Error retrieving counts for orderType=${orderType}: ${err.message}` });
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
    // ابتدا UUID را بررسی کنید تا orderid مربوطه را بیابید
    const ongoingBarcode = await Ongoingbarcode.findOne({ where: { uuid }, attributes: ['orderid'], raw: true });
    if (!ongoingBarcode) {
      return res.status(404).send({ message: "UUID not found." });
    }

    // سپس productcode مرتبط با orderid را بیابید
    const order = await Order.findOne({ where: { orderid: ongoingBarcode.orderid }, attributes: ['productcode'], raw: true });
    if (!order) {
      return res.status(404).send({ message: "Order not found for the given UUID." });
    }

    // در نهایت، تعداد محصولات را بر اساس productcode و favoritecode شمارش کنید
    const count = await Ongoingbarcode.count({
      where: {
        whOrderId: favoritecode,
        orderid: order.productcode,  // این فرض بر این است که orderid باید با productcode مطابقت داشته باشد
        levelId: 0
      }
    });

    res.send({ result: "ok", orderid: ongoingBarcode.orderid, productcount: count });
  } catch (err) {
    console.error(err);
    res.status(500).send({ message: "An error occurred during the operation.", error: err.message });
  }
};

exports.getBarcodeFromUid = async (req, res) => {
  const _uuid = req.body.uuid;
  console.log(_uuid);

  try {
    // فرض بر این است که تابع makeBarcodeFromUid به صورت ماژول جاوااسکریپت نوشته شده است
    const barcode = makeBarcodeFromUid(_uuid);
    res.send({ barcode });
  } catch (err) {
    console.error(err);
    res.status(500).send({ message: "An error occurred during barcode generation.", error: err.message });
  }
};

function makeBarcodeFromUid(uuid) {
  // اینجا یک الگوریتم برای تولید بارکد از UUID قرار می‌گیرد
  // به عنوان مثال، ترکیبی از تاریخ و زمان فعلی به UUID اضافه می‌کنیم تا یک بارکد منحصر به فرد تولید کنیم
  return 'BRCD-' + Date.now() + '-' + uuid.slice(0, 8);
}
