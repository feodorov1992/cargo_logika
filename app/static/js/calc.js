$('.digits').keyup(function(e){
    let code = e.keyCode || e.which;
    if(code !== '9') {
        $(this).val( $(this).val().replace(/ю/gi,'.').replace(/б/gi,'.').replace(/,/gi,'.').replace(/[^0-9.,]/gi,'') );
    }
});

$('#send_precise').change( function() {
    const el = $(this);
    if( el.is(':checked') ) {
        $( '#send_precise_address' ).prop('disabled', false);
    } else {
        $( '#send_precise_address' ).prop('disabled', true);
    }
});

$('#receive_precise').change( function() {
    const el = $(this);
    if( el.is(':checked') ) {
        $( '#receive_precise_address' ).prop('disabled', false);
    } else {
        $( '#receive_precise_address' ).prop('disabled', true);
    }
});

$('#inner_transfer').change( function () {
    const el = $(this);
    if( el.is(':checked') ) {
        if ($('#receive_precise').is(':checked')){
            $('#receive_precise').click();
        }
        $( '#receive_precise' ).prop('disabled', true).val('');
        $( '#receiver_addr' ).prop('disabled', true).val('');
    } else {
        $( '#receive_precise' ).prop('disabled', false);
        $( '#receiver_addr' ).prop('disabled', false);
    }
})

$('#insurance').change( function () {
    const el = $(this);
    if( el.is(':checked') ) {
        $( '#cargo_value' ).prop('disabled', false);
    } else {
        $( '#cargo_value' ).prop('disabled', true).val('');
    }
})

$("#calc_form").submit(function(e){
    e.preventDefault();
    if (!$('#sub_phone').val() && !$('#sub_email').val()) {
        $('#not_full').css('display', 'table-row');
        document.getElementById("content").scrollIntoView({block: "start", behavior: "smooth"})
    } else {
        $('#not_full').css('display', 'none');
        let raw_data = $("#calc_form").serialize();
        $.post(
            "/php/redirect_calc.php",
            raw_data,
            function() {
                $('#alert').css('display', 'flex');
            }
        );
        $("#calc_form").trigger('reset');
        $( '#receive_precise' ).prop('disabled', false);
        $( '#receiver_addr' ).prop('disabled', false);
    }
});

$('#cross').click( function(){
    $('#alert').removeAttr('style');
    }
)
