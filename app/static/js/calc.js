$('.digits').keyup(function(e){
    let code = e.keyCode || e.which;
    if(code !== '9') {
        $(this).val( $(this).val().replace(/ю/gi,'.').replace(/б/gi,'.').replace(/,/gi,'.').replace(/[^0-9.,]/gi,'') );
    }
});

$('#id_send_precise').change( function() {
    let target = $( '#id_send_precise_address' )
    if( $(this).is(':checked') ) {
        target.prop('disabled', false);
        target.prop('required', true);
        $('label[for="id_send_precise"]').addClass('required');
    } else {
        target.prop('disabled', true).val('');
        target.prop('required', false);
        $('label[for="id_send_precise"]').removeClass('required');
    }
});

$('#id_receive_precise').change( function() {
    let target = $( '#id_receive_precise_address' )
    if( $(this).is(':checked') ) {
        target.prop('disabled', false);
        target.prop('required', true);
        $('label[for="id_receive_precise"]').addClass('required');
    } else {
        target.prop('disabled', true).val('');
        target.prop('required', false);
        $('label[for="id_receive_precise"]').removeClass('required');
    }
});

$('#id_inner_transfer').change( function () {
    let target_check = $('#id_receive_precise')
    let target_field = $( '#id_receiver_addr' )
    if( $(this).is(':checked') ) {
        if (target_check.is(':checked')){
            target_check.click();
        }
        target_check.prop('disabled', true);
        target_field.prop('disabled', true).val('');
        target_field.prop('required', false);
        $('label[for="id_receiver_addr"]').removeClass('required');
    } else {
        target_check.prop('disabled', false);
        target_field.prop('disabled', false);
        target_field.prop('required', true);
        $('label[for="id_receiver_addr"]').addClass('required');
    }
})

$('#id_insurance').change( function () {
    let target = $('#id_cargo_value')
    if( $(this).is(':checked') ) {
        target.prop('disabled', false);
        target.prop('required', true);
        $('label[for="id_cargo_value"]').addClass('required')
    } else {
        target.prop('disabled', true).val('');
        target.prop('required', false);
        $('label[for="id_cargo_value"]').removeClass('required')
    }
})

$("#calc_form").submit(function(e) {
    if (!$('#id_sub_phone').val() && !$('#id_sub_email').val()) {
        e.preventDefault()
        $('#not_full').css('display', 'table-row');
        document.getElementById("content").scrollIntoView({block: "start", behavior: "smooth"})
        return false
    } else {
        $("input[type=text]").prop('disabled', false);
        $("input[type=tel]").prop('disabled', false);
        return true
    }
});
