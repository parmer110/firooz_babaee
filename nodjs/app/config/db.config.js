module.exports = {
  HOST: "localhost",
  PORT: "5432",
  USER: "djangouser",
  PASSWORD: "amf@psql2022",
  DB: "amf_frz_db2",
  dialect: "postgres",
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  }
};
