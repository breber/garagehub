$().ready(function() {
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
                }
            );
        } else {
            $("#models").html("<option>Select a model</option>");
            $("#years").html("<option>Select a year</option>");
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
                }
            );
        } else {
            $("#years").html("<option>Select a year</option>");
        }
    });
});
