const express = require('express');
const app = express();
const bodyParser = require('body-parser');


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use('/scripts', express.static(__dirname + '/node_modules/'));
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader(
    "Access-Control-Allow-Headers",
    "Origin, X-requested-With, Content-Type, Accept, Authorization"
  );
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET, POST, PATCH, PUT, DELETE, OPTIONS, PUT"
  );

  next();
});



app.get('', function(req, res){
   // res.sendFile(__dirname + '/index.html');
   res.json({data:'test'})
  });

module.exports=app;