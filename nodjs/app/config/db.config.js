require('dotenv').config();
const { parse } = require('pg-connection-string');
const config = parse(process.env.DATABASE_URL);
// console.log(config);
module.exports = {
  HOST: config.host,
  PORT: config.port,
  USER: config.user,
  PASSWORD: config.password,
  DB: config.database,
  dialect: "postgres",
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  },
};

// module.exports = {

//   connectionString: process.env.DATABASE_URL_2
// };


// module.exports = {
//   HOST: "localhost",
//   PORT: "5432",
//   USER: "djangouser",
//   PASSWORD: "amf@psql2022",
//   DB: "amf_frz_db2",
//   dialect: "postgres",
//   pool: {
//     max: 5,
//     min: 0,
//     acquire: 30000,
//     idle: 10000
//   }
// };
