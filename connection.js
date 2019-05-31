const WebSocket = require('faye-websocket').Client;

const conn = new WebSocket((process.env.SHOWDOWN_PORT === "443" ? 'wss' : 'ws') + "://" + process.env.SHOWDOWN_HOST + ":" + process.env.SHOWDOWN_PORT + "/showdown/websocket");

conn.onopen = function() {

};

conn.onerror = function(error) {
  restartBot();
};

conn.onclose = function(close) {
  restartBot();
};

conn.onmessage = function(message) {
  Parser.parse(message.data);
};

Connection = conn;
