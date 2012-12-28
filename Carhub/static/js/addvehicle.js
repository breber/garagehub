$().ready(function() {
    $("#addVehicle").on("show", function () {
        if ($("#makes > option").length <= 1) {
            $.get('/cars/raw',
                    function(data) {
                        var optionString = [];

                        optionString.push("<option>Select a make</option>");

                        $.each(data, function(i) {
                            optionString.push("<option>" + data[i] + "</option>");
                        });

                        $("#makes").html(optionString.join(""));
                        $("#models").html("<option>Select a model</option>");
                        $("#years").html("<option>Select a year</option>");
                        
                        $("#makes").removeAttr("disabled");
                        $("#models").attr("disabled", "disabled");
                        $("#years").attr("disabled", "disabled");
                    }
            );
        }
    });
	
    // When the user chooses a new make, get the models
    // for the updated make
    $("#makes").change(function() {
        if ($("#makes").prop("selectedIndex") !== 0) {
            $.get('/cars/raw/' + $("#makes").val(),
                function(data) {
                    var optionString = [];

                    optionString.push("<option>Select a model</option>");

                    $.each(data, function(i) {
                        optionString.push("<option>" + data[i] + "</option>");
                    });

                    $("#models").html(optionString.join(""));
                    $("#years").html("<option>Select a year</option>");
                    
                    $("#models").removeAttr("disabled");
                    $("#years").attr("disabled", "disabled");
                }
            );
        } else {
            $("#models").html("<option>Select a model</option>");
            $("#years").html("<option>Select a year</option>");
            $("#models").attr("disabled", "disabled");
            $("#years").attr("disabled", "disabled");
        }
    });

    $("#models").change(function() {
        if ($("#models").prop("selectedIndex") !== 0) {
            $.get('/cars/raw/' + $("#makes").val() + '/' + $("#models").val(),
                function(data) {
                    var optionString = [];

                    optionString.push("<option>Select a year</option>");

                    $.each(data, function(i) {
                        optionString.push("<option>" + data[i] + "</option>");
                    });

                    $("#years").html(optionString.join(""));
                    $("#years").removeAttr("disabled");
                }
            );
        } else {
            $("#years").html("<option>Select a year</option>");
            $("#years").attr("disabled", "disabled");
        }
    });
});
