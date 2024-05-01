// Import the ScanLog model
const db = require("../models");
const ScanLog = db.scanlog;
const Op = db.Sequelize.Op;
const sequelize = require("sequelize");
const config = require("../config/db.config");
const { QueryTypes } = require("sequelize");


// Create and save a new ScanLog
exports.create = async (req, res) => {
    // Validate request
    if (!req.body.uuid) {
        return res.status(400).send({
            message: "UUID can not be empty!"
        });
    }

    // Create a ScanLog object
    const scanLog = {
        whOrderId: req.body.whOrderId,
        whUserId: req.body.whUserId,
        uuid: req.body.uuid
    };

    try {
        // Save ScanLog in the database using Sequelize ORM
        const data = await ScanLog.create(scanLog);
        res.send(data);
    } catch (err) {
        res.status(500).send({
            message: err.message || "Some error occurred while creating the ScanLog."
        });
    }
};

// Retrieve all ScanLogs from the database.
exports.findAll = async (req, res) => {
    const uuid = req.query.uuid;
    var condition = uuid ? { uuid: { [Op.like]: `%${uuid}%` } } : null;

    try {
        const data = await ScanLog.findAll({ where: condition });
        res.send(data);
    } catch (err) {
        res.status(500).send({
            message: err.message || "Some error occurred while retrieving ScanLogs."
        });
    }
};

// Find a single ScanLog with an id
exports.findOne = async (req, res) => {
    const id = req.params.id;

    try {
        const data = await ScanLog.findByPk(id);
        if (data) {
            res.send(data);
        } else {
            res.status(404).send({
                message: `ScanLog with id=${id} not found.`
            });
        }
    } catch (err) {
        res.status(500).send({
            message: `Error retrieving ScanLog with id=${id}`
        });
    }
};

// Update a ScanLog by the id in the request
exports.update = async (req, res) => {
    const id = req.params.id;

    try {
        const num = await ScanLog.update(req.body, {
            where: { id: id }
        });
        if (num == 1) {
            res.send({
                message: "ScanLog was updated successfully."
            });
        } else {
            res.status(404).send({
                message: `Cannot update ScanLog with id=${id}. Maybe ScanLog was not found or req.body is empty!`
            });
        }
    } catch (err) {
        res.status(500).send({
            message: `Error updating ScanLog with id=${id}`
        });
    }
};

// Delete a ScanLog with the specified id in the request
exports.delete = async (req, res) => {
    const id = req.params.id;

    try {
        const num = await ScanLog.destroy({
            where: { id: id }
        });
        if (num == 1) {
            res.send({
                message: "ScanLog was deleted successfully!"
            });
        } else {
            res.status(404).send({
                message: `Cannot delete ScanLog with id=${id}. Maybe ScanLog was not found!`
            });
        }
    } catch (err) {
        res.status(500).send({
            message: "Could not delete ScanLog with id=" + id
        });
    }
};

// Delete all ScanLogs from the database.
exports.deleteAll = async (req, res) => {
    try {
        const nums = await ScanLog.destroy({
            where: {},
            truncate: false
        });
        res.send({ message: `${nums} ScanLogs were deleted successfully!` });
    } catch (err) {
        res.status(500).send({
            message: err.message || "Some error occurred while removing all ScanLogs."
        });
    }
};

// Find all ScanLogs with a uuid and sort by date
exports.findByUUId = async (req, res) => {
    const uuid = req.params.uuid;

    try {
        const data = await ScanLog.findAll({
            where: { uuid: uuid },
            order: [['createdAt', 'DESC']]
        });
        res.send(data);
    } catch (err) {
        res.status(500).send({
            message: "Error retrieving ScanLogs with uuid=" + uuid
        });
    }
};

exports.findOrderTypeByUUId = async (req, res) => {
    const uuid = req.params.uuid;

    try {
        const latestScan = await ScanLog.findOne({
            where: { uuid: uuid },
            order: [['createdAt', 'DESC']],
            attributes: ['whOrderId']
        });

        if (latestScan) {
            const order = await WarehouseOrder.findOne({
                where: { id: latestScan.whOrderId },
                attributes: ['ordertype']
            });

            if (order) {
                res.send({ ordertype: order.ordertype });
            } else {
                res.status(404).send({ message: 'Order not found' });
            }
        } else {
            res.status(404).send({ message: 'ScanLog not found' });
        }
    } catch (err) {
        res.status(500).send({ message: "Error retrieving order type with uuid=" + uuid + ": " + err.message });
    }
};

// exports.countOrder = (req, res) => {
//     const _whorderid = req.body.whorderid;
//     console.log(`inside countOrder   ${_whorderid}`);
//     ScanLog.count({ where: { whorderid: _whorderid } })
//         .then((data) => {
//             res.send(data + "");
//         })
//         .catch((err) => {
//             res.status(500).send({
//                 message: "Error retrieving ScanLog count",
//             });
//         });
// };
exports.countOrder = async (req, res) => {
    const _whorderid = req.body.whorderid;
    console.log(`inside countOrder   ${_whorderid}`);
    try {
        // Using Sequelize to count entries with a conditional clause on the 'uuid'
        const count = await ScanLog.count({
            where: {
                whOrderId: _whorderid,
                uuid: {
                    [Op.and]: [
                        sequelize.where(
                            sequelize.fn('substring', sequelize.col('uuid'), 6, 1),
                            '0'
                        )
                    ]
                }
            }
        });
        res.send(count.toString()); // Send count as a string
    } catch (err) {
        console.error(`Error retrieving ScanLog count for whOrderId ${_whorderid}: ${err.message}`);
        res.status(500).send({
            message: "Error retrieving ScanLog count"
        });
    }
};
