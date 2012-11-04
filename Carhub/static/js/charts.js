$("#empty").hide();
$("#chart_div").hide();
$("#loading").show();

google.load("visualization", "1", {
	packages : [ "corechart" ]
});
google.setOnLoadCallback(fetchData);

function fetchData() {
	// TODO: better way to get vehicle ID
	var locationStr = window.location.pathname;
	var vehicleId = /\/vehicle\/([^\/]+)/.exec(locationStr);
	var dateRange = 120;
	
	$.getJSON("/api/fuel/" + vehicleId[1] + "/" + dateRange, function(data) {
		drawFuelChart(data);
	});
};

function drawFuelChart(content) {
	if (content.length < 2) {
		$("#loading").hide();
		$("#chart_div").hide();
		$("#empty").show();
	}
	
	var data = new google.visualization.DataTable();
	data.addColumn('string', 'Date');
	data.addColumn('number', 'MPG');
	data.addColumn('number', '$/Gal');

	var currentDate = new Date();
	var arr = [];
	$.each(content, function(index, item) {
		if (item.odometerStart !== -1) {
			var tmp = [];
			tmp.push(item.date);
			tmp.push((item.odometerEnd - item.odometerStart) / item.gallons);
			tmp.push(item.costPerGallon);
			
			arr.push(tmp);
		}
	});

	data.addRows(arr);

	var options = {
		title : 'Average Gas Milage',
		backgroundColor: '#f5f5f5',
		series : [{
			visibleInLegend : true
		}, {
			targetAxisIndex : 1
		}],
		vAxes : [{
			title : 'Miles / Gallon',
		}, {
			title : '$ / Gallon',
		}]
	};

	$("#loading").hide();
	$("#empty").hide();
	$("#chart_div").show();
	
	var chartDiv = document.getElementById('chart_div');
	var chart = new google.visualization.LineChart(chartDiv);
	chart.draw(data, options);
};
