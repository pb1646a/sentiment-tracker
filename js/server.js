const app = require("./app");
const http = require("http");
const { Subject } = require("rxjs");
const port = process.env.PORT || 3000;
let connections = 0;
app.set("port", port);

const server = http.createServer(app);

function sendData(x) {
  console.log({ data: x, time: new Date() })
  io.emit("data", JSON.stringify({ data: x, time: new Date() }));

}

let $$item = new Subject();
function populateSubject() {
  console.log('started');
  $$item.next(Math.floor(Math.random() * Math.floor(10)));
  setTimeout(populateSubject, 5000);
}
populateSubject();

const io = require("socket.io")(server);
server.on("error", error => console.log(error));
server.on("listening", () => console.log("opened server" + port));

io.on("connection", socket => {
  console.log("connected to webserver");
  socket.emit("connection", "true");

  socket.on('close',()=>{
    console.log('request to disconnect')
    socket.disconnect();
  })
  socket.on("disconnect", () => {
    console.log('disconnected');
    socket.disconnect(true,5000)
  });
});

$$item.subscribe(x => {
  console.log('sending');
  return sendData(x);
});
server.listen(port);
