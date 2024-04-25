const db = require("../models");
const { QueryTypes } = require("sequelize");
const config = require("../config/db.config");
const Ongoingbarcode = db.ongoingbarcodes;
const ScanLog = db.scanlog;
const Op = db.Sequelize.Op;

// Create and Save a new Ongoingbarcode
exports.create = (req, res) => {
  if (!req.body.uuid) {
    return res.status(400).send({ message: "UUID can not be empty!" });
  }

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

  Ongoingbarcode.create(newOngoingbarcode)
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({ message: err.message || "Some error occurred while creating the Ongoingbarcode." });
    });
};

// Retrieve all Ongoingbarcodes from the database.
exports.findAll = (req, res) => {
  const { uuid, favoritecode } = req.query;
  let condition = {};

  if (uuid) {
    condition.uuid = { [Op.like]: `%${uuid}%` };
  }

  if (favoritecode) {
    condition.favoritecode = { [Op.like]: `%${favoritecode}%` };
  }

  Ongoingbarcode.findAll({ where: condition })
    .then(data => {
      res.send(data);
    })
    .catch(err => {
      res.status(500).send({ message: err.message || "Some error occurred while retrieving ongoingbarcodes." });
    });
};
// Find a single Ongoingbarcode with an id
exports.findOne = (req, res) => {
  const _uuid = req.params.uuid;

  Ongoingbarcode.findOne({ where: { uuid: _uuid } })
    .then((data) => {
      if (data) {
        res.send(data);
      } else {
        res.status(404).send({ message: "Ongoingbarcode not found with uuid=" + _uuid });
      }
    })
    .catch((err) => {
      res.status(500).send({
        message: "Error retrieving Ongoingbarcode with uuid=" + _uuid + ": " + err.message,
      });
    });
};

// Update an existing Ongoingbarcode by the id in the request
exports.update = (req, res) => {
  const uuid = req.params.uuid;

  // Optionally validate req.body here
  if (Object.keys(req.body).length === 0) {
    return res.status(400).send({ message: "Data to update can not be empty!" });
  }

  Ongoingbarcode.update(req.body, {
    where: { uuid: uuid },
  })
    .then((num) => {
      if (num == 1) {
        res.send({
          message: "Ongoingbarcode was updated successfully.",
        });
      } else {
        res.send({
          message: `Cannot update Ongoingbarcode with uuid=${uuid}. Maybe Ongoingbarcode was not found or req.body is empty!`,
        });
      }
    })
    .catch((err) => {
      res.status(500).send({
        message: `Error updating Ongoingbarcode with uuid= ${uuid}: ${err.message}`,
      });
    });
};

exports.updatefavcode = async (req, res) => {
  const { uuid, favoritecode, userid, state, orderType, checkTheFollow } = req.body;

  try {
    const sql = `CALL UpdateFavCodeProcedure(:uuid, :favoritecode, :userid, :state, :orderType, :checkTheFollow);`;

    const result = await sequelize.query(sql, {
      replacements: { uuid, favoritecode, userid, state, orderType, checkTheFollow },
      type: QueryTypes.UPDATE
    });

    res.send(result);
  } catch (err) {
    console.error(err);
    res.status(500).send({ message: "An error occurred during the operation." });
  }
};

exports.countOrder = (req, res) => {
  const _whorderid = req.body.whorderid;
  const _orderType = req.body.orderType;
  console.log(`inside countOrder   ${_whorderid}`);
  switch (_orderType) {
    case "outgoing":
      Ongoingbarcode.count({ where: { whorderid: _whorderid, levelid: 0 } })
        .then((data) => {
          res.send(data + "");
        })
        .catch((err) => {
          res.status(500).send({
            message: "Error retrieving Ongoingbarcode count",
          });
        });
      break;
    default:
      ScanLog.count({ where: { whorderid: _whorderid } })
        .then((data) => {
          res.send(data + "");
        })
        .catch((err) => {
          res.status(500).send({
            message: "Error retrieving ScanLog count",
          });
        });
  }
};



exports.countOrderLevels = (req, res) => {
  const _whorderid = req.body.whorderid;
  const _orderType = req.body.orderType;

  const Sequelize = require("sequelize");
  const sequelize = new Sequelize(config.DB, config.USER, config.PASSWORD, {
    host: config.HOST,
    dialect: config.dialect,
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000,
    },
    operatorsAliases: false,
  });

  console.log(`inside countOrder   ${_whorderid}`);
  switch (_orderType) {
    case "outgoing":
      // The raw SQL query for the Ongoingbarcode.findAll method
      const sql1 = `SELECT COALESCE(levelid, 0) AS levelid, COUNT(levelid) AS count FROM Ongoingbarcode WHERE whorderid = ${_whorderid} OR levelid IS NULL GROUP BY COALESCE(levelid, 0)`;
      sequelize.query(sql1, {
        type: Sequelize.QueryTypes.SELECT, // The type of query to execute
        model: Ongoingbarcode, // The model to map the results to
        mapToModel: true // Pass true here if you have any mapped fields
      })
        .then((data) => {
          // data will be an array of Ongoingbarcode instances
          res.send(data);
        })
        .catch((err) => {
          res.status(500).send({
            message: "Error retrieving Ongoingbarcode count",
          });
        });
      break;
    default:
      // The raw SQL query for the ScanLog.findAll method
      const sql2 = `SELECT COALESCE(substring(uuid, 6, 1), 0) AS levelid, COUNT(uuid) AS count FROM ScanLogs WHERE whorderid = ${_whorderid} OR uuid IS NULL GROUP BY COALESCE(substring(uuid, 6, 1), 0)`;
      sequelize.query(sql2, {
        type: Sequelize.QueryTypes.SELECT, // The type of query to execute
        model: ScanLog, // The model to map the results to
        mapToModel: true // Pass true here if you have any mapped fields
      })
        .then((data) => {
          // data will be an array of ScanLog instances
          res.send(data);
        })
        .catch((err) => {
          res.status(500).send({
            message: "Error retrieving ScanLogs count",
          });
        });
  }
}


async function isRndEsalatFound(key) {
  console.log("isRndEsalatFound", key);
  const _result = await Ongoingbarcode.findOne({ where: { rndesalat: key } });
  if (_result === null) {
    console.log("No rndesalat found for key " + key);
    return false;
  } else {
    console.log("Found rndesalat " + _result.rndesalat);
    return true;
  }

  // Ongoingbarcode.count({ where: { rndesalat: key } }).then((count) => {
  //   return count > 0 ? true : false;
  // });
}
async function isUuidFound(key) {
  console.log("isUuidFound", key);
  const _result = await Ongoingbarcode.findOne({ where: { uuid: key } });
  if (_result === null) {
    console.log("No uuid found for key " + key);
    return false;
  } else {
    console.log("Found uuid " + _result.uuid);
    return true;
  }
}
async function isBarcodeFound(key) {
  console.log("isBarcodeFound", key);
  _key = key.substring(18, 38);
  const _result = await Ongoingbarcode.findOne({ where: { uuid: _key } });
  if (_result === null) {
    console.log("No uuid found for key " + _key);
    return false;
  } else {
    console.log("Found uuid " + _result.uuid);
    return true;
  }

  // Ongoingbarcode.count({ where: { rndesalat: key } }).then((count) => {
  //   return count > 0 ? true : false;
  // });
}

exports.trackBarcode = async (req, res) => {
  const _userId = req.body.userId;
  const _method = req.body.method;
  const _key = req.body.key;
  console.log(_key, _method, _userId);
  if (_method == "rndEsalat") {
    if (await isRndEsalatFound(_key)) {
      res.send("Found");
      console.log("Found");
      return;
    } else {
      res.send("notFound");
    }
  }
  if (_method == "uuid") {
    if (await isUuidFound(_key)) {
      res.send("Found");
      console.log("Found");
      return;
    } else {
      res.send("notFound");
    }
  }
  if (_method == "barcode") {
    if (await isBarcodeFound(_key)) {
      res.send("Found");
      console.log("Found");
      return;
    } else {
      res.send("notFound");
    }
  }
};
// Delete an Ongoingbarcode with the specified id in the request
exports.delete = (req, res) => {
  const nationalid = req.params.nationalid;

  Ongoingbarcode.destroy({
    where: { nationalid: nationalid },
  })
    .then((num) => {
      if (num == 1) {
        res.send({
          message: "Ongoingbarcode was deleted successfully!",
        });
      } else {
        res.send({
          message: `Cannot delete Ongoingbarcode with nationalid=${nationalid}. Maybe Ongoingbarcode was not found!`,
        });
      }
    })
    .catch((err) => {
      res.status(500).send({
        message: "Could not delete Ongoingbarcode with id=" + id,
      });
    });
};

// Delete all Ongoingbarcodes from the database.
exports.deleteAll = (req, res) => {
  Ongoingbarcode.destroy({
    where: {},
    truncate: false,
  })
    .then((nums) => {
      res.send({
        message: `${nums} Ongoingbarcodes were deleted successfully!`,
      });
    })
    .catch((err) => {
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
  console.log('find children of $_uuid : ', _uuid + req.params);
  Ongoingbarcode.findAll({ where: { parent: _uuid } })
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      res.status(500).send({
        message:
          err.message ||
          "Some error occurred while retrieving children list.",
      });
    });
};

exports.warehouseOrderProductCount = async (req, res) => {
  const _uuid = req.body.uuid;
  const _favoritecode = req.body.favoritecode;
  const Sequelize = require("sequelize");
  const sequelize = new Sequelize(config.DB, config.USER, config.PASSWORD, {
    host: config.HOST,
    dialect: config.dialect,
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000,
    },
    operatorsAliases: false,
  });

  sql = "DECLARE @uuid VARCHAR(20), \n"
    + "        @favoritecode VARCHAR(20), \n"
    + "        @orderid VARCHAR(20), \n"
    + "        @orderType VARCHAR(20), \n"
    + "        @gtin VARCHAR(20), \n"
    + "        @productCount INT = 0 \n"
    + " \n"
    + "DECLARE @rec TABLE \n"
    + "( \n"
    + "	Barcode VARCHAR(20), \n"
    + "	LevelNum INT \n"
    + ")  \n"
    + "SET @uuid = :uuid    \n"
    + "SET @favoritecode = :favoritecode    \n"
    + "SELECT @Orderid = orderid \n"
    + "FROM   OnGoingBarCodes \n"
    + "WHERE  uuid = @uuid \n"
    + "     \n"
    + "SELECT @gtin = productcode \n"
    + "FROM   orders \n"
    + "WHERE  ordercode = @orderid \n"
    + "     \n"
    + "SELECT @productCount = ( \n"
    + "           SELECT COUNT(0) \n"
    + "           FROM   OnGoingBarCodes AS ogbc \n"
    + "           WHERE  ogbc.WhOrderId = @favoritecode  \n"
    + "                  AND ogbc.OrderId IN (SELECT OrderCode From Orders WHERE productcode = @gtin) \n"
    + "                  AND levelId = 0 \n"
    + "       ) \n"
    + " \n"
    + "SELECT 'ok'           AS result, \n"
    + "       @orderid       AS orderid, \n"
    + "       @productCount  AS productcount  ";
  await sequelize
    .query(sql, {
      replacements: { favoritecode: _favoritecode, uuid: _uuid },
      type: QueryTypes.UPDATE,
    })
    .then((rows) => {
      console.log(rows);
      res.send(rows);
    })
    .catch((err) => {
      res.send(err);
      console.log(err);
    });
};


exports.getBarcodeFromUid = async (req, res) => {
  const _uuid = req.body.uuid;
  console.log(_uuid);
  const Sequelize = require("sequelize");
  const sequelize = new Sequelize(config.DB, config.USER, config.PASSWORD, {
    host: config.HOST,
    dialect: config.dialect,
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000,
    },
    operatorsAliases: false,
  });


  sql = "SELECT dbo.MakeBarcodeFromUid(:uuid) AS barcode";

  await sequelize
    .query(sql, {
      replacements: { uuid: _uuid },
      type: QueryTypes.SELECT,
    })
    .then((rows) => {
      console.log(rows);
      res.send(rows);
    })
    .catch((err) => {
      res.send(err);
      console.log(err);
    });
};