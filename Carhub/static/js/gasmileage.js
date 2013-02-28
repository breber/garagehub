jQuery.fn.dataTableExt.oSort['number-range-asc'] = function(a, b) {
    var aEnd;
    var bEnd;

    a = a.replace(/\s+/g, " ");
    b = b.replace(/\s+/g, " ");

    if (/- (.+)/.test(a)) {
        aEnd = RegExp.$1;
    }

    if (/- (.+)/.test(b)) {
        bEnd = RegExp.$1;
    }

    var x = (a == "-") ? 0 : aEnd.replace(",", "");
    var y = (b == "-") ? 0 : bEnd.replace(",", "");
    x = parseFloat(x);
    y = parseFloat(y);
    return ((x < y) ? -1 : ((x > y) ? 1 : 0));
};

jQuery.fn.dataTableExt.oSort['number-range-desc'] = function(a, b) {
    var aEnd;
    var bEnd;

    a = a.replace(/\s+/g, " ");
    b = b.replace(/\s+/g, " ");

    if (/- (.+)/.test(a)) {
        aEnd = RegExp.$1;
    }

    if (/- (.+)/.test(b)) {
        bEnd = RegExp.$1;
    }

    var x = (a == "-") ? 0 : aEnd.replace(",", "");
    var y = (b == "-") ? 0 : bEnd.replace(",", "");
    x = parseFloat(x);
    y = parseFloat(y);
    return ((x < y) ? 1 : ((x > y) ? -1 : 0));
};

$(document).ready(function() {
    var dTable = $('#gasmileagetable').dataTable({
        "sDom" : "t",
        "bPaginate" : false,
        "bLengthChange" : false,
        "bFilter" : false,
        "bSort" : true,
        "bInfo" : false,
        "bAutoWidth" : false,
        "aaSorting" : [ [ 6, 'desc' ] ],
        "aoColumns" : [ null, null, null, null, null, null, {
            "sType" : "number-range"
        }, null ]
    });

    // Setup the handlers for the edit/delete buttons
    setupHandlers();

    // make rows selectable
    $('#gasmileagetable tbody').click(function(event) {
        $(dTable.fnSettings().aoData).each(function() {
            $(this.nTr).removeClass('active');
        });

        $(event.target.parentNode).addClass('active');
    });

    $('.receiptlink').click(function() {
        $('#displayimage').modal();
        $('#modalimage').attr('src', this.getAttribute('value'));
    });
});
