google.load("visualization", "1", {
	packages : [ "corechart" ]
});
google.setOnLoadCallback(drawChart);

function drawChart() {
	var data = new google.visualization.DataTable();
	data.addColumn('string', 'Date');
	data.addColumn('number', 'MPG');
	data.addColumn('number', '$/Gal');

	var currentDate = new Date();
	var arr = [];
	for ( var i = 10; i >= 0; i--) {
		var rand = Math.random();
		var result = 35;
		if (rand > .5) {
			result += (rand * 5);
		} else {
			result -= (rand * 5);
		}

		var tmp = [];
		var tmpDate = new Date(currentDate.getTime() - (i * 604800000));
		tmp.push((tmpDate.getMonth() + 1) + "/" + tmpDate.getDate());
		tmp.push(result);

		rand = Math.random();
		if (rand > .5) {
			tmp.push(3.5 + rand);
		} else {
			tmp.push(3.5 - rand);
		}

		arr.push(tmp);
	}

	data.addRows(arr);

	var options = {
		title : 'Average Gas Milage',
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
	var chartDiv = document.getElementById('chart_div');
	var chart = new google.visualization.LineChart(chartDiv);
	chart.draw(data, options);
};