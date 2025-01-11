let aliveSecond = 0;
let heartbeatRate = 5000;

var myChannel = "RoomTemp";

pubnub = new PubNub({
    publishKey : "pub-c-212e735b-5718-4ccb-8ba0-4b9e7ec25b03",
    subscribeKey : "sub-c-c9a67ff9-4ad3-42ad-867d-63ca15c0cd02",
    userId: "32fb700d-8e42-4d20-9a55-c6b20f9de693"
});

pubnub.addListener({
	status: function(statusEvent) {
		if (statusEvent.category === "PNConnectedCategory"){
			console.log("Connected to PubNub!");
		}
	},
	message: function(message){
		var msg = message.message;;
		console.log(msg);

	presence: function(presenceEvent){
		
	}
	
})

pubnub.subscribe({
	channels: [myChannel]	
});

function publishUpdate(channel, message)
{
    pubnub.publish({
        channel: channel,
        message: message
    });
}


function time()
{
	let d = new Date();
	let currentSecond = d.getTime();
	if(currentSecond - aliveSecond > heartbeatRate + 1000)
	{
		document.getElementById("connection_id").innerHTML = "DEAD!!!!";
	}
	else
	{
		document.getElementById("connection_id").innerHTML = "Alive";
	}
	setTimeout('time()', 1000);
}

function keepAlive()
{
	fetch('/keep_alive')
	.then(response => {
		if(response.ok){
			let date = new Date();
			aliveSecond = date.getTime();
			return response.json();
		}
		throw new Error('Server offline');
	})
	.then(responseJson=>{
		if(responseJson.motion == 1){
			document.getElementById("temperature_id").innerHTML = "Temperature";
		}
		else{
			document.getElementById("motion_id").innerHTML = "No Temperature";
		}
	})		 
	.catch(error => console.log(error));
	setTimeout('keepAlive()', heartbeatRate);
}
	

function sendEvent(value)
{
	fetch("/status="+value,
		{
			method:"POST",
		})
}