var plot;
var data = [], totalPoints = 100;
var updateInterval = 30;
var currentDeviceID;
var currentDeviceInforID;
var tid;
function onGetDeviceInfor(device_id) {
	currentDeviceID = device_id;
	var csrftoken = $.cookie('csrftoken');
	var posting = $.post("/device-infor", {
		'csrfmiddlewaretoken' : csrftoken,
		'device_id' : device_id,
	});
	posting.done(function(data) 
	{
		resetChart(data.device_infor[0].properties.min,data.device_infor[0].properties.max);
		updateData(data.device_infor[0].value);
		currentDeviceInforID = data.device_infor[0].id;
		updateDeviceInfor(data.device, data.device_infor);
		abortTimer();
		tid = setTimeout(mycode, 1000);
	});
}

function getCurrentDeviceInfor()
{
	var csrftoken = $.cookie('csrftoken');
	var posting = $.post("/device-infor", {
		'csrfmiddlewaretoken' : csrftoken,
		'device_id' : currentDeviceID,
	});
	posting.done(function(data) {
		updateDeviceInfor(data.device, data.device_infor);
		updateData(data.device_infor[0].value);
	});
}

function updateDeviceInfor(device, infors)
{
	//update device name
	var deviceName = $('#device-name');
	deviceName.html("<a href=\"#\">"+device.code+" </a> - "+device.address);
	var deviceMac = $('#device-mac');
	deviceMac.html("MAC: "+device.mac_add);
	var deviceServer = $('#device-server');
	deviceServer.html("Connected server: "+nvl(device.connected_server,"Chưa kết nối"));
	var deviceStatus = $('#device-status');
	if(device.status=="1")
		deviceStatus.attr("src","images/ic_green.png");
	else if(device.status=="2")
		deviceStatus.attr("src","images/ic_red.png")
	else if(device.status=="0")
		deviceStatus.attr("src","images/ic_blue.png");
//	deviceName.html("<a href=\"#\">"+device.code+" </a> - "+device.address);
	var deviceIssue = $('#device-issue');
//	if(device.status=="2")
//	{
//		deviceIssue.css("display","");
//	}
//	else
//		deviceIssue.css("display","none");
//	deviceName.html("<a href=\"#\">"+device.code+" </a> - "+device.address);
	//update device information
	var deviceInfor = $('#device-infor');
	deviceInfor.empty();
	for (var i = 0; i < infors.length; i++) {
		var infor = infors[i];
		var row = $('<div>');
		row.attr("class", "row");

		var separator = $('<div>');
		separator.attr("class", "mb10");
		separator.appendTo(row);

		addProperty(device,row, infor, "0")
		if (i < infors.length - 2) {
			i++;
			infor = infors[i];
			addProperty(device,row, infor, "1")
		}
		row.appendTo(deviceInfor);
	}
}

function addProperty(device,row, infor, status)
{
	var column = $('<div>');
	column.attr("class", "col-sm-6");
	if(device.status ="0")
	{
		column.html("<p>" + infor.properties.name
				+ "</p> <h4 style=\"color: gray\">" + "__ " + "</h4>");
	}
	else if (infor.value == 0) {
		column.html("<p>" + infor.properties.name
				+ "</p> <h4 style=\"color: gray\">" + "__ " + "</h4>");
	} else if (status == "0") {
		column.html("<p>" + infor.properties.name
				+ "</p> <h4 style=\"color: red\">" + infor.value + " "
				+ infor.properties.symbol + "</h4>");
	} else if (status == "1") {
		column.html("<p>" + infor.properties.name
				+ "</p> <h4 style=\"color: green\">" + infor.value + " "
				+ infor.properties.symbol + "</h4>");
	}
	column.appendTo(row);
}
function mycode() {
	getCurrentDeviceInfor();
	
	updateChart();
	// do some stuff...
	tid = setTimeout(mycode, 1000); // repeat myself
}
function abortTimer() { // to be called when you want to stop the timer
	clearTimeout(tid);
}


function getNewData(){
	data = []

	while (data.length < totalPoints) {

		var prev = data.length > 0 ? data[data.length - 1] : 50, y = 0;

		data.push(y);
	}

	// Zip the generated y values with the x values

	var res = [];
	for (var i = 0; i < data.length; ++i) {
		res.push([ i, data[i] ])
	}

	return res;
}
function updateData(value)
{
	data.splice(data.length-1,1);
	
	data.unshift(value); 
}

function getData()
{
	var res = [];
	for (var i = 0; i < data.length; ++i) {
		res.push([ i, data[i] ])
	}
	return res;
}
function getRandomData() {

	if (data.length > 0)
		data = data.slice(1);

	// Do a random walk
	
	while (data.length < totalPoints) {

		var prev = data.length > 0 ? data[data.length - 1] : 50, y = prev
				+ Math.random() * 10 - 5;

		if (y < 0) {
			y = 0;
		} else if (y > 100) {
			y = 100;
		}

		data.push(y);
	}

	// Zip the generated y values with the x values

	var res = [];
	for (var i = 0; i < data.length; ++i) {
		res.push([ i, data[i] ])
	}

	return res;
}
var chartTID = setTimeout(updateChart, updateInterval);
function resetChart(min,max)
{
	plot = $.plot("#placeholder", [ getNewData() ], {
		series: {
			shadowSize: 0	// Drawing is faster without shadows
		},
		yaxis: {
			min: min,
			max: max
		},
		xaxis: {
			show: false
		}
	});
	
}

function updateChart() {

	plot.setData([getData()]);
	// Since the axes don't change, we don't need to call plot.setupGrid()
	plot.draw();
}

function nvl(obj,strNull)
{
	if(obj)
		return obj.toString();
	else
		return strNull;
}