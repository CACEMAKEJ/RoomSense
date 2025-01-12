let aliveSecond = 0;
let heartbeatRate = 5000;

var myChannel = "RoomTemp";

let pubnub = new PubNub({
  publishKey: "pub-c-212e735b-5718-4ccb-8ba0-4b9e7ec25b03",
  subscribeKey: "sub-c-c9a67ff9-4ad3-42ad-867d-63ca15c0cd02",
  userId: "32fb700d-8e42-4d20-9a55-c6b20f9de693",
});

pubnub.addListener({
  status: function (statusEvent) {
    if (statusEvent.category === "PNConnectedCategory") {
      console.log("Connected to PubNub!");
    }
  },
  message: function (message) {
    var msg = message.message;
	console.log(message);
	if (msg.hasOwnProperty("temperature")) {
	document.getElementById("temperature_id").innerHTML = msg.temperature;
	document.getElementById("temperature_spinner").style.display = "none";
	document.getElementById("temperature_container").style.display = "block";
	} else {
	console.error("Invalid or missing temperature data");
	}

	if (msg.hasOwnProperty("humidity")) {
    document.getElementById("humidity_id").innerHTML = msg.humidity;
    document.getElementById("humidity_spinner").style.display = "none";
    document.getElementById("humidity_container").style.display = "block";
  } else {
    console.error("Invalid or missing humidity data");
  }
	if (msg.hasOwnProperty("lightStatus")) {
	document.getElementById("lightstatus_id").innerHTML = msg.lightstatus;
	document.getElementById("lightstatus_spinner").style.display = "none";
	document.getElementById("lightstatus_container").style.display = "block";
	} else {
	console.error("Invalid or missing light status data");
	}
},
});
pubnub.subscribe({
  channels: [myChannel],
});

function publishUpdate(channel, message) {
  pubnub.publish({
    channel: channel,
    message: message,
  });
}

function time() {
  let d = new Date();
  let currentSecond = d.getTime();
  if (currentSecond - aliveSecond > heartbeatRate + 1000) {
    document.getElementById("connection_id").innerHTML = "&#10007;";
  } else {
    document.getElementById("connection_id").innerHTML = "&#10003;";
  }
  setTimeout(time, 1000);
}
 

function keepAlive() {
  fetch("/keep_alive")
    .then((response) => {
      if (response.ok) {
        let date = new Date();
        aliveSecond = date.getTime();
        return response.json();
      }
      throw new Error("Server offline");
    })
    .then((responseJson) => {
      if (responseJson.motion == 1) {
        document.getElementById("temperature_id").innerHTML = "Temperature";
      }
    })
    .catch((error) => console.log(error));
  setTimeout(keepAlive, heartbeatRate);
}

function sendEvent(value) {
  fetch(`/status=${value}`, {
    method: "POST",
  });
}
