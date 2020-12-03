use dbproject
db.createCollection("metadata")
db.createCollection("log")
use admin
db.createUser({user: 'yt',pwd: 'password',roles: [{ role: 'userAdminAnyDatabase', db: 'admin' },{ role: 'readWriteAnyDatabase', db: 'admin' },{ role: 'dbAdminAnyDatabase',   db: 'admin' }]});
