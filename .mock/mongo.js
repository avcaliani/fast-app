/**
 * LOCAL DEVELOPMENT ONLY!
 * DO NOT USE PRODUCTION DATA HERE!
 */

/* API User at MongoDB */
db.createUser({
    user: "fast-app-api",
    pwd: "123456",
    roles: [{role: "readWrite", db: "fastAppDB"}]
});
