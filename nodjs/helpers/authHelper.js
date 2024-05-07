const pbkdf2 = require('pbkdf2');
const crypto = require('crypto');

function hashPassword(password, salt = crypto.randomBytes(16).toString('hex')) {
    const iterations = 600000;
    const keyLength = 32;
    const digest = 'sha256';
    return new Promise((resolve, reject) => {
        pbkdf2.pbkdf2(password, salt, iterations, keyLength, digest, (err, derivedKey) => {
            if (err) reject(err);
            else resolve(`pbkdf2_sha256$${iterations}$${salt}$${derivedKey.toString('base64')}`);
        });
    });
}

function validatePassword(inputPassword, storedHash) {
    const [algorithm, iterations, salt, hash] = storedHash.split('$');
    return hashPassword(inputPassword, salt).then(computedHash => computedHash === storedHash);
}

module.exports = {
    hashPassword,
    validatePassword
};
