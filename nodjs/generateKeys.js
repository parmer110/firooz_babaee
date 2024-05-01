const crypto = require('crypto');
const fs = require('fs');

crypto.generateKeyPair('rsa', {
  modulusLength: 2048,
}, (err, publicKey, privateKey) => {
  if (err) throw err;

  fs.writeFileSync('privateKey.pem', privateKey.export({ type: 'pkcs1', format: 'pem' }));
  fs.writeFileSync('publicKey.pem', publicKey.export({ type: 'spki', format: 'pem' }));
});