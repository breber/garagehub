
$(document).ready(function() {
	var dTable = $('#expense-table').dataTable({
		"sDom" : "<'row'<'span6'l><'span6'f>r>t",
		"bPaginate" : false,
		"bLengthChange" : false,
		"bFilter" : false,
		"bSort" : true,
		"bInfo" : false,
		"bAutoWidth" : false,
		"aaSorting" : [ [ 0, 'desc' ] ]
	});
	
	addDatepickerToJEditable();
	
	/* Apply the jEditable handlers to the table */
	$('.edit-date').editable( '../examples_support/editable_ajax.php', {
        "callback": function( sValue, y ) {
            var aPos = dTable.fnGetPosition( this );
            dTable.fnUpdate( sValue, aPos[0], aPos[1] );
        },
        "submitdata": function ( value, settings ) {
            return {
                "row_id": this.parentNode.getAttribute('id'),
                "column": dTable.fnGetPosition( this )[2]
            };
        },
        type   : 'datepicker',
        "height": "14px",
        "width": "100%"
    } );
	
	/* Apply the jEditable handlers to the table */
	$('.edit-category').editable( '../examples_support/editable_ajax.php', {
        "callback": function( sValue, y ) {
            var aPos = dTable.fnGetPosition( this );
            dTable.fnUpdate( sValue, aPos[0], aPos[1] );
        },
        "submitdata": function ( value, settings ) {
            return {
                "row_id": this.parentNode.getAttribute('id'),
                "column": dTable.fnGetPosition( this )[2]
            };
        },
        type   : 'select',
        "height": "14px",
        "width": "100%"
    } );
	
	/* Apply the jEditable handlers to the table */
	$('.edit-category').editable( '../examples_support/editable_ajax.php', {
        "callback": function( sValue, y ) {
            var aPos = dTable.fnGetPosition( this );
            dTable.fnUpdate( sValue, aPos[0], aPos[1] );
        },
        "submitdata": function ( value, settings ) {
            return {
                "row_id": this.parentNode.getAttribute('id'),
                "column": dTable.fnGetPosition( this )[2]
            };
        },
        type   : 'select',
        "height": "14px",
        "width": "100%"
    } );
	
	/* Apply the jEditable handlers to the table */
	$('.edit-location').editable( '../examples_support/editable_ajax.php', {
        "callback": function( sValue, y ) {
            var aPos = dTable.fnGetPosition( this );
            dTable.fnUpdate( sValue, aPos[0], aPos[1] );
        },
        "submitdata": function ( value, settings ) {
            return {
                "row_id": this.parentNode.getAttribute('id'),
                "column": dTable.fnGetPosition( this )[2]
            };
        },
        type   : 'textarea',
        "height": "14px",
        "width": "100%"
    } );
	
	/* Apply the jEditable handlers to the table */
	$('.edit-description').editable( '../examples_support/editable_ajax.php', {
        "callback": function( sValue, y ) {
            var aPos = dTable.fnGetPosition( this );
            dTable.fnUpdate( sValue, aPos[0], aPos[1] );
        },
        "submitdata": function ( value, settings ) {
            return {
                "row_id": this.parentNode.getAttribute('id'),
                "column": dTable.fnGetPosition( this )[2]
            };
        },
        type   : 'textarea',
        "height": "14px",
        "width": "100%"
    } );
	
	/* Apply the jEditable handlers to the table */
	$('.edit-amount').editable( '../examples_support/editable_ajax.php', {
        "callback": function( sValue, y ) {
            var aPos = dTable.fnGetPosition( this );
            dTable.fnUpdate( sValue, aPos[0], aPos[1] );
        },
        "submitdata": function ( value, settings ) {
            return {
                "row_id": this.parentNode.getAttribute('id'),
                "column": dTable.fnGetPosition( this )[2]
            };
        },
        type   : 'textarea',
        "height": "14px",
        "width": "100%"
    } );
	
});

$('.receiptlink').click( function() {
	$('#displayimage').modal();
	$('#modalimage').attr('src', this.getAttribute('value'));
});

function addDatepickerToJEditable(){
	$.editable.addInputType('datepicker', {
	    element : function(settings, original) {
	        var input = $('<input>');
	        if (settings.width  != 'none') { input.width(settings.width);  }
	    	if (settings.height != 'none') { input.height(settings.height); }
	        input.attr('autocomplete','off');
	    	$(this).append(input);
	    	return(input);
	    },
	    plugin : function(settings, original) {
	        /* Workaround for missing parentNode in IE */
	    	var form = this;
	    	settings.onblur = 'ignore';
	    	$(this).find('input').datepicker().bind('click', function() {
	    		$(this).datepicker('show');
	            return false;
	        }).bind('dateSelected', function(e, selectedDate, $td) {
	            $(form).submit();
	        });
	    }
	});
}



//TODO
// 	make modal to upload images in editable table mode
//	make editable table mode and display the columns that need to be able to be edited
