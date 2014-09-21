// Ready function
$(document).ready(function() {
    // When the page is ready, hide the table and loading
    // sections so there isn't a huge blank space in the page
    $("#gaspricetable").hide();
    $("#loading").hide();
    $("#gaspricetable").removeClass("hidden");

    // Setup click handlers
    $("#location").click(hideZipCode);
    $("#fetchPrices").click(getGasPrices);

    //Favorite Handler
    $("#saveAsFavorite").click(favoriteHandler);

    //Update Handler
    $("#priceUpdate").click(updateHandler);
    $("#priceUpdateClose").click(updateCloseHandler);
    $("#priceUpdateSubmit").click(updateSubmitHandler);


    datatablesObject = null;

    getGasPrices();
});

function favoriteHandler() {
    //alert("Favorite Handler");
    var id = $("#hiddenId").text();
    $.post("/userfavorites/gasstation", { stationid: id}, function(data) {
        //Can do something here on response
    });
}

function updateHandler(name, location) {
    //modalPriceUpdate
    $("#modalMap").hide();
    $("#modalPriceUpdate").modal();
}

function updateSubmitHandler() {
    //alert("post");
    //TODO fix this so it works
//    $.post("http://api.mygasfeed.com/locations/price/zax22arsix.json", { price: "3.63", fueltype: "2", stationid: "1" }, function(data) {
//        alert(data);
//    });
}

function updateCloseHandler() {
    //modalPriceUpdate
    $("#modalMap").modal();
}

$(document).on("click", "#gaspricetable tr td", function() {
    var lat = $(this).parent().find('td').eq(5).text();
    var lon = $(this).parent().find('td').eq(6).text();
    var id = $(this).parent().find('td').eq(7).text();
    var name = $(this).parent().find('td').eq(0).text();
    var location = $(this).parent().find('td').eq(1).text();
    $('#stationNameModal').empty();
    $('#stationNameModal').append(name+' - '+location);
    $('#stationNamePriceModal').empty();
    $('#stationNamePriceModal').append(name+' - '+location);
    $('#hiddenId').empty();
    $('#hiddenId').append(id);

    var mapOptions = {
        zoom : 14,
        center : new google.maps.LatLng(lat, lon),
        mapTypeId : google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map($("#map_canvas")[0], mapOptions);

    var latLng = new google.maps.LatLng(lat, lon); // Makes a latlng
    addMarker(map, latLng);

    $('#modalMap').on('shown.bs.modal', function() {
    google.maps.event.trigger(map, "resize");
    map.panTo(latLng);
    });

    $("#modalMap").modal();
});

// Function for adding a marker to the map
function addMarker(map, location) {
    var marker = new google.maps.Marker({
        position : location,
        map : map
    });
}

function getGasPrices() {
    if ($('#location').attr('checked')) {
        getLocation();
    } else {
        useZipCode();
    }
}

function hideZipCode() {
    if ($("#location").attr("checked")) {
        $("#zip").prop("disabled", true);
    } else {
        $("#zip").prop("disabled", false);
    }
}

function sendJSONRequest(lat, lon) {
    var radius = $("#radius").val();

    if (!radius) {
        radius = 0;
        $("#radius").val(radius);
    }

    var grade = $("#grade").val();
    var sort = $("#sort").val();
    var baseURL = "http://api.mygasfeed.com/stations/radius/%s/%s/%s/%s/%s/zax22arsix.json?callback=?";
    var jsonURL = sprintf(baseURL, lat, lon, radius, grade, sort);
    displayGasPrices(jsonURL);
}

function useZipCode() {
    var geocoder = new google.maps.Geocoder();
    var address = $("#zip").val();
    if (address) {
        geocoder.geocode({
            'address' : address
        }, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var latLon = String(results[0].geometry.location);
                var word = latLon.split(",")
                var lat = word[0].substring(1);
                var lon = word[1].substring(1, word[1].length - 1);
                sendJSONRequest(lat, lon);
            }
        });
    } else {
        newAlert('Please enter a zip code or use the Detect My Location option');
    }
}

function useLocation(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    sendJSONRequest(lat, lon);
}

function getLocation(){
   if (navigator.geolocation) {
      // 30 seconds
      var options = {timeout:30000};
      navigator.geolocation.getCurrentPosition(useLocation,
                                               errorHandler,
                                               options);
   } else {
       newAlert("Sorry, your browser does not support geolocation.");
   }
}

function errorHandler(err) {
    if (err.code == 1) {
        newAlert("Error: Access is denied! Please check your location settings.");
    } else if (err.code == 2) {
        newAlert("Error: Position is unavailable!");
    }
}

function showLoading() {
    $("#loading").removeClass("hidden");
    $("#loading").show();

    $("#gaspricetable").hide();
}

function stopLoading() {
    $("#loading").hide();
    $("#gaspricetable").show();
}

function displayGasPrices(JSONGasFeed) {
    showLoading();

    if (datatablesObject !== null) {
        datatablesObject.fnDestroy();
    }

    $.getJSON(JSONGasFeed,
        function(json) {
            var grade = $('#grade').val();
            var sort = $("#sort").val();
            var sortByColumn = 2;
            if (sort === "distance") {
                sortByColumn = 3;
            }
            var data = [];
            $.each(json.stations, function(i, item) {
                var station = {};
                station["0"] = item.station;
                station["1"] = item.address;
                if (grade === "Mid") {
                    station["2"] = item.mid_price;
                    station["4"] = item.mid_date;
                } else if (grade === "Premium") {
                    station["2"] = item.pre_price;
                    station["4"] = item.pre_date;
                } else if (grade === "Diesel") {
                    station["2"] = item.diesel_price;
                    station["4"] = item.diesel_date;
                } else {
                    station["2"] = item.reg_price;
                    station["4"] = item.reg_date;
                }
                station["3"] = item.distance;
                station["5"] = item.lat;
                station["6"] = item.lng;
                station["7"] = item.id;
                station["DT_RowClass"] = "linkable";

                if (station["2"] !== "N/A") {
                    data.push(station);
                }
            });

            datatablesObject = $('#gaspricetable').dataTable( {
                "bProcessing": true,
                "bPaginate" : false,
                "bLengthChange" : false,
                "bFilter" : false,
                "bSort" : true,
                "bInfo" : false,
                "bAutoWidth" : false,
                "aaData": data,
                "aaSorting": [[ sortByColumn, 'asc' ]]
            } );

            $('#gaspricetable td:nth-child(6)').hide();
            $('#gaspricetable th:nth-child(6)').hide();
            $('#gaspricetable td:nth-child(7)').hide();
            $('#gaspricetable th:nth-child(7)').hide();
            $('#gaspricetable td:nth-child(8)').hide();
            $('#gaspricetable th:nth-child(8)').hide();
            stopLoading();
        }
    );
}
