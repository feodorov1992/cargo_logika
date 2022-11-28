$("#order_form").submit(function(e){
    e.preventDefault();
    $("input[type=text]").prop('disabled',false);
    $("input[type=tel]").prop('disabled',false);
    $("select").prop('disabled',false);
    rawdata = $("#order_form").serialize();
    $.post(
        "/php/redirect_order.php",
        rawdata,
        function(data) {
            $('#order_num').html(data);
            $('#alert').css('display', 'flex');
        }
    );
    $("#order_form").trigger('reset');
    $('#sender_name').prop('disabled',false).val('');
    $('#sender_name').removeAttr("style");
    $('#sender_phone').prop('disabled',false).val('');
    $('#sender_phone').removeAttr("style");
    $('#sender_contact').prop('disabled',false).val('');
    $('#sender_contact').removeAttr("style");
    $('#sender_type').prop('disabled',false);
    $('#sender_type').removeAttr("style");
    $('#sender_passport').prop('disabled',false).val('');
    $('#sender_passport').removeAttr("style");
    $('#sender_inn').prop('disabled',false).val('');
    $('#sender_inn').removeAttr("style");
    $('#receiver_name').prop('disabled',false).val('');
    $('#receiver_name').removeAttr("style");
    $('#receiver_phone').prop('disabled',false).val('');
    $('#receiver_phone').removeAttr("style");
    $('#receiver_contact').prop('disabled',false).val('');
    $('#receiver_contact').removeAttr("style");
    $('#receiver_type').prop('disabled',false);
    $('#receiver_type').removeAttr("style");
    $('#receiver_passport').prop('disabled',false).val('');
    $('#receiver_passport').removeAttr("style");
    $('#receiver_inn').prop('disabled',false).val('');
    $('#receiver_inn').removeAttr("style");
});

$( '#payer_type' ).change( function() {
    var type = $( '#payer_type' ).val();

    if ( type === 'Физ. лицо' ) {

        $( 'tr#payer_passport_row' ).show();
        $( '#payer_passport' ).prop('required',true);
        $( 'tr#payer_inn_row' ).hide();
        $( '#payer_inn' ).prop('required',false);


    } else if ( type === 'Юр. лицо' ) {

        $( 'tr#payer_passport_row' ).hide();
        $( '#payer_passport' ).prop('required',false);
        $( 'tr#payer_inn_row' ).show();
        $( '#payer_inn' ).prop('required',true);

    }

    if ( $('#sender_payer').is(':checked') ) {
        $('#sender_type').val( $('#payer_type').val() );
        sender_type_change();
    };

    if ( $('#receiver_payer').is(':checked') ) {
        $('#receiver_type').val( $('#payer_type').val() );
        receiver_type_change();
    };

});

function sender_type_change() {
    var type = $( '#sender_type' ).val();

    if ( type === 'Физ. лицо' ) {

        $( 'tr#sender_passport_row' ).show();
        $( '#sender_passport' ).prop('required',true);
        $( 'tr#sender_inn_row' ).hide();
        $( '#sender_inn' ).prop('required',false);

    } else if ( type === 'Юр. лицо' ) {

        $( 'tr#sender_passport_row' ).hide();
        $( '#sender_passport' ).prop('required',false);
        $( 'tr#sender_inn_row' ).show();
        $( '#sender_inn' ).prop('required',true);
    }
}

function receiver_type_change() {
    var type = $( '#receiver_type' ).val();

    if ( type === 'Физ. лицо' ) {

        $( 'tr#receiver_passport_row' ).show();
        $( '#receiver_passport' ).prop('required',true);
        $( 'tr#receiver_inn_row' ).hide();
        $( '#receiver_inn' ).prop('required',false);

    } else if ( type === 'Юр. лицо' ) {

        $( 'tr#receiver_passport_row' ).hide();
        $( '#receiver_passport' ).prop('required',false);
        $( 'tr#receiver_inn_row' ).show();
        $( '#receiver_inn' ).prop('required',true);
    }
}

$( '#sender_type' ).change( function() {sender_type_change()});
$( '#receiver_type' ).change( function() {receiver_type_change()});

$('#sender_payer').on('change',function(e){
    var el = $(this);
    if( el.is(':checked') ){
        if( $('#receiver_payer').is(':checked') ){
            $('#receiver_payer').click();
        }
        $('#sender_name').prop('disabled',true).val( $('#payer_name').val() );
        $('#sender_name').css("color", "white");
        $('#sender_phone').prop('disabled',true).val( $('#payer_phone').val() );
        $('#sender_phone').css("color", "white");
        $('#sender_contact').prop('disabled',true).val( $('#payer_contact').val() );
        $('#sender_contact').css("color", "white");

        $('#sender_type').prop('disabled',true).val( $('#payer_type').val() );

        sender_type_change();

        $('#sender_passport').prop('disabled',true).val( $('#payer_passport').val() );
        $('#sender_passport').css("color", "white");
        $('#sender_inn').prop('disabled',true).val( $('#payer_inn').val() );
        $('#sender_inn').css("color", "white");
    }else{
        $('#sender_name').prop('disabled',false).val('');
        $('#sender_name').removeAttr("style");
        $('#sender_phone').prop('disabled',false).val('');
        $('#sender_phone').removeAttr("style");
        $('#sender_contact').prop('disabled',false).val('');
        $('#sender_contact').removeAttr("style");
        $('#sender_type').prop('disabled',false);
        $('#sender_passport').prop('disabled',false).val('');
        $('#sender_passport').removeAttr("style");
        $('#sender_inn').prop('disabled',false).val('');
        $('#sender_inn').removeAttr("style");
    }
});

$('#receiver_payer').on('change',function(e){
    var el = $(this);
    if( el.is(':checked') ){
        if( $('#sender_payer').is(':checked') ){
            $('#sender_payer').click();
        }
        $('#receiver_name').prop('disabled',true).val( $('#payer_name').val() );
        $('#receiver_name').css("color", "white");
        $('#receiver_phone').prop('disabled',true).val( $('#payer_phone').val() );
        $('#receiver_phone').css("color", "white");
        $('#receiver_contact').prop('disabled',true).val( $('#payer_contact').val() );
        $('#receiver_contact').css("color", "white");

        $('#receiver_type').prop('disabled',true).val( $('#payer_type').val() );

        receiver_type_change();

        $('#receiver_passport').prop('disabled',true).val( $('#payer_passport').val() );
        $('#receiver_passport').css("color", "white");
        $('#receiver_inn').prop('disabled',true).val( $('#payer_inn').val() );
        $('#receiver_inn').css("color", "white");
    }else{
        $('#receiver_name').prop('disabled',false).val('');
        $('#receiver_name').removeAttr("style");
        $('#receiver_phone').prop('disabled',false).val('');
        $('#receiver_phone').removeAttr("style");
        $('#receiver_contact').prop('disabled',false).val('');
        $('#receiver_contact').removeAttr("style");
        $('#receiver_type').prop('disabled',false);
        $('#receiver_passport').prop('disabled',false).val('');
        $('#receiver_passport').removeAttr("style");
        $('#receiver_inn').prop('disabled',false).val('');
        $('#receiver_inn').removeAttr("style");
    }
});

$("#payer_name").on("keyup", function(e){
    //--------------
    var el = $(this);
    //-------------
    if( $('#sender_payer').is(':checked') ){
        $('#sender_name').val( el.val() );
    }
    //-------------
    if( $('#receiver_payer').is(':checked') ){
        $('#receiver_name').val( el.val() );
    }
})

$("#payer_phone").on("keyup", function(e){
    //--------------
    var el = $(this);
    //-------------
    if( $('#sender_payer').is(':checked') ){
        $('#sender_phone').val( el.val() );
    }
    //-------------
    if( $('#receiver_payer').is(':checked') ){
        $('#receiver_phone').val( el.val() );
    }
})

$("#payer_contact").on("keyup", function(e){
    //--------------
    var el = $(this);
    //-------------
    if( $('#sender_payer').is(':checked') ){
        $('#sender_contact').val( el.val() );
    }
    //-------------
    if( $('#receiver_payer').is(':checked') ){
        $('#receiver_contact').val( el.val() );
    }
})

$('#send_precise').change( function() {
    var el = $(this);
    if( el.is(':checked') ) {
        $( '#send_precise_address' ).prop('disabled', false);
    } else {
        $( '#send_precise_address' ).prop('disabled', true);
    }
});

$('#receive_precise').change( function() {
    var el = $(this);
    if( el.is(':checked') ) {
        $( '#receive_precise_address' ).prop('disabled', false);
    } else {
        $( '#receive_precise_address' ).prop('disabled', true);
    }
});

$('#cross').click( function(){
        $('#alert').css('display', 'none');
    }
)
