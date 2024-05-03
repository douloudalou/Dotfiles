// install the mysql2 library
var mysql = require('mysql2');

var connection = mysql.createConnection({
    host:'localhost',
    port: '3306',
    user:'root',
    password:'adev',
    database: 'restaurant_review'
});

connection.connect(err => {  // test out connetion and console.log error if there is one
    if (err) throw err;
    console.log('Connected To DB');
}); 
module.exports = connection;

