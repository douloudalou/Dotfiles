var express = require("express"); //using the express framework
var db = require('./db-connections');
var app = express(); // set variable app to be an instance of express framework. From now on, app is the express

app.use(express.json()); // json() is a method inbuilt in express to recognize the incoming Request Object from the web client as a JSON Object.

app.route('/test').get( function (req, res){
  res.json({ message: 'Welcome to my server'});
});

app.route('/test').post( function (req, res){
    res.json({ message: 'This is a post method'});
});

app.route('/test').put( function (req, res){
  res.json({ message: 'This is a put method'});
});

app.route('/test').delete( function (req, res){
  res.json({ message: 'This is a delete method'});
});
  
app.route('/user').get( function (req, res){
  res.json({ message: 'This is a user get method'});
});

app.route('/user').post( function (req, res){
  res.json({message: "This is a user post method", type:"Announcement"});
});

// Sample GET route
app.route('/user/:id').get( function (req, res) {
  // Accessing URL parameters, for example: /user/123
  const userId = req.params.id;

  // Accessing the query string, for example: /user/123?type=admin
  const userType = req.query.type;

  // Send response back with the captured parameters
  // sending message not in JSON format
  res.send(`User ID is: ${userId}, User Type is: ${userType}`);
});

// Sample POST route
app.route('/student').post( function(req, res) {
  // Accessing JSON body sent by client
  const studentName = req.body.name;
  const studentEmail = req.body.email;

  // Send response back with the parsed body content
  // sending message not in JSON format
  res.send(`Received new user: Name is ${studentName}, Email is ${studentEmail}`);
});

// Sample GET route
app.route('/lecturer/:id').get( function (req, res) {
  // Accessing URL parameters, for example: /user/123
  const userId = req.params.id;

  // Accessing the query string, for example: /user/123?type=admin
  const age = req.query.age;

  // Send response back with the captured parameters
  // sending message not in JSON format
  res.send(`User ID is: ${userId}, User age is: ${age}`);
});

// Sample POST route
app.route('/lecturer').post(function (req, res) {
  // Accessing JSON body sent by client
  const name = req.body.name;
  const position = req.body.position;

  // Send response back with the parsed body content
  // sending message not in JSON format
  res.send(`Received new user: Name is ${name}, Position is ${position}`);
});

app.route('/restaurant').get( function (req, res) {

    // the database retrieval code
    //implement SELECT query to retrieve all RESTAURANTS
    var sql = "SELECT * FROM RESTAURANT_REVIEW.RESTAURANT";
    //perform query to database from web server
    db.query(sql, function(error, result){
        if(error){
            throw error;
        }else{
            //return result as json
            res.json(result);
        }
    });

});

app.route('/restaurant/:id').get( function (req, res) {

  // the database retrieval code
  //implement SELECT query to retrieve all RESTAURANTS
  var sql = "SELECT * FROM RESTAURANT_REVIEW.RESTAURANT where id = ?";
  
  // the parameter to replace the ?
  var parameter = [req.params.id]
  
  db.query(sql,parameter, function(error, result){
      if(error){
          throw error;
      }else{
          //return result as json
          res.json(result);
      }
  });

});

app.route('/restaurant').post( function (req, res) {

  //implement insert query to insert data into the restaurant using placeholder values
  // we do not need the id, it will be auto increment
  var sql = "INSERT INTO RESTAURANT_REVIEW.RESTAURANT (name, address, description, rating, cuisine_type, opening_date, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)";

  //get the values from the req.body
  //the variable sequence should be the same as the insert sequence in the insert sql
  var parameters = [req.body.name, req.body.address, req.body.description, req.body.rating, req.body.cuisine_type, req.body.opening_date, req.body.image_url];
  
  db.query(sql, parameters, function(error, result){
      if(error){
          throw error;
      }else{
          //return result as json
          res.json(result);
      }
  });

});

app.route('/restaurant/:id').put( function (req, res) {

  // update sql statement for one restaurant 
  var sql = "UPDATE RESTAURANT_REVIEW.RESTAURANT SET name = ?, address = ?, description = ?, rating = ?, cuisine_type = ?, opening_date = ?, image_url = ? WHERE id = ?";

  //get the values from the req.body
  //the variable sequence should be the same as the update sequence in the insert sql
  var parameters = [req.body.name, req.body.address, req.body.description, 
    req.body.rating, req.body.cuisine_type, req.body.opening_date, req.body.image_url,
    req.params.id // Assuming the ID of the restaurant to update is passed as a URL parameter
  ];
  
  db.query(sql, parameters, function(error, result){
      if(error){
          throw error;
      }else{
          //return result as json
          res.json(result);
      }
  });

});

app.route('/restaurant/:id').delete( function (req, res) {

  // update sql statement for one restaurant 
  var sql = "DELETE FROM RESTAURANT_REVIEW.RESTAURANT WHERE id = ?";

  var parameters = [req.params.id]; // the ID of the restaurant to delete is passed as a URL parameter
  
  db.query(sql, parameters, function(error, result){
      if(error){
          throw error;
      }else{
          //return result as json
          res.json(result);
      }
  });

});

app.route('/review').get( function (req, res) {

  // the database retrieval code
  //implement SELECT query to retrieve all RESTAURANTS
  var sql = "SELECT * FROM RESTAURANT_REVIEW.REVIEW";
  //perform query to database from web server
  db.query(sql, function(error, result){
      if(error){
          throw error;
      }else{
          //return result as json
          res.json(result);
      }
  });

});


app.route('/review').post( function (req, res) {

  //implement insert query to insert data into the restaurant using placeholder values
  // we do not need the id, it will be auto increment
  var sql = "INSERT INTO RESTAURANT_REVIEW.REVIEW (restaurant_id, content, date, reviewer_name) VALUES (?, ?, ?, ?)";

  var now = new Date();
  //get the values from the req.body
  //the variable sequence should be the same as the insert sequence in the insert sql
  var parameters = [req.body.restaurant_id, req.body.content,now, req.body.reviewer_name];
  
  db.query(sql, parameters, function(error, result){
      if(error){
          throw error;
      }else{
          //return result as json
          res.json(result);
      }
  });

});

app.route('/review/:id').put( function (req, res) {

  // update sql statement for one restaurant 
  var sql = "UPDATE RESTAURANT_REVIEW.REVIEW SET content = ?, date = ? WHERE id = ?";

  var now = new Date();
  //get the values from the req.body
  //the variable sequence should be the same as the update sequence in the insert sql
  var parameters = [req.body.content, now, 
    req.params.id // Assuming the ID of the restaurant to update is passed as a URL parameter
  ];
  
  db.query(sql, parameters, function(error, result){
      if(error){
          throw error;
      }else{
          //return result as json
          res.json(result);
      }
  });

});

app.route('/review/:id').delete( function (req, res) {

  // update sql statement for one restaurant 
  var sql = "DELETE FROM RESTAURANT_REVIEW.REVIEW WHERE id = ?";

  var parameters = [req.params.id]; // the ID of the restaurant to delete is passed as a URL parameter
  
  db.query(sql, parameters, function(error, result){
      if(error){
          throw error;
      }else{
          //return result as json
          res.json(result);
      }
  });

});

app.listen(8080, "127.0.0.1"); // start the nodejs to be listening for incoming request @ port 8080
console.log("web server running @ http://127.0.0.1:8080"); // output to console 