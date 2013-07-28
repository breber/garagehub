$(".range").click(function() {
    fetchData(new Number(this.id));
});

google.load("visualization", "1", {
    packages : [ "corechart" ]
});
google.setOnLoadCallback(fetchData);

function startLoading() {
    $("#empty").hide();
    $("#charts").hide();
    $("#loading").show();
    $("#empty").removeClass("hidden");
    $("#charts").removeClass("hidden");
}

function stopLoading() {
    $("#loading").hide();
    $("#empty").hide();
    $("#charts").show();
}

function fetchData(dateRange) {
    startLoading();
    var vehicleId = getVehicleId();

    if (!(dateRange instanceof Number)) {
        dateRange = 120;
    }

    // TODO: new api method for getting based on date range
    $.getJSON("/api/expense/fuel/" + vehicleId[1] + "/" + dateRange, function(data) {
        drawFuelChart(data);
    });

    $.getJSON("/api/expense/category/" + vehicleId[1] + "/" + dateRange, function(data) {
        drawCategoryChart(data);
    });
}

function drawFuelChart(content) {
    if (content.length < 2) {
        $("#loading").hide();
        $("#charts").hide();
        $("#empty").show();

        return;
    }

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Date');
    data.addColumn('number', 'MPG');
    data.addColumn('number', '$/Gal');

    var arr = [];
    $.each(content.records, function(index, item) {
        if (item.odometerStart !== -1) {
            var tmp = [];
            tmp.push(item.date.str);
            if (item.mpg !== undefined) {
                tmp.push(item.mpg);
            } else {
                tmp.push((item.odometerEnd - item.odometerStart) / item.gallons);
            }
            tmp.push(item.costPerGallon);

            arr.push(tmp);
        }
    });

    data.addRows(arr);

    var options = {
        title : 'Average Gas Milage',
        // backgroundColor : '#f5f5f5',
        series : [ {
            visibleInLegend : true
        }, {
            targetAxisIndex : 1
        } ],
        vAxes : [ {
            title : 'Miles / Gallon',
        }, {
            title : '$ / Gallon',
        } ]
    };

    stopLoading();

    var chartDiv = document.getElementById('fuel_chart_div');
    var chart = new google.visualization.LineChart(chartDiv);
    chart.draw(data, options);
}

function drawCategoryChart(content) {
    if (content.length === 0) {
        $("#loading").hide();
        $("#charts").hide();
        $("#empty").show();

        return;
    }

    var fullData = [ [ 'Category', 'Cost' ] ].concat(content);
    var data = google.visualization.arrayToDataTable(fullData);

    var options = {
        title : 'Categorized Expenditures',
        // backgroundColor : '#f5f5f5',
    };

    stopLoading();

    var chartDiv = document.getElementById('category_chart_div');
    var chart = new google.visualization.PieChart(chartDiv);
    chart.draw(data, options);
}
