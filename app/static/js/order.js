function resetInput(input, blank_val = true) {
    input.prop('disabled', false);
    if (blank_val) {
        input.val('');
    }
    input.removeAttr("style");
}

$("#order_form").on('submit', function() {
    $("input[type=text]").prop('disabled', false);
    $("input[type=number]").prop('disabled', false);
    $("input[type=tel]").prop('disabled', false);
    $("select").prop('disabled', false);
    return true;
});

$('#id_payer_type').change(function() {
    const type = $(this).val();

    if (type === 'individual') {
        $('tr#payer_passport_row').show();
        $('#id_payer_passport').prop('required',true);
        $('label[for="id_payer_passport"]').addClass('required')
        $('tr#payer_inn_row').hide();
        $('#id_payer_tin').prop('required',false);
        $('label[for="id_payer_tin"]').removeClass('required')
    } else {
        $('tr#payer_passport_row').hide();
        $('#id_payer_passport').prop('required',false);
        $('label[for="id_payer_passport"]').removeClass('required')
        $('tr#payer_inn_row').show();
        $('#id_payer_tin').prop('required',true);
        $('label[for="id_payer_tin"]').addClass('required')
    }

    if ( $('#sender_payer').is(':checked')) {
        let target =  $('#id_sender_type')
        target.val(type);
        target.change();
    }

    if ( $('#receiver_payer').is(':checked') ) {
        let target =  $('#id_receiver_type')
        target.val(type);
        target.change();
    }

});

$('#id_sender_type').change(function() {
    const type = $(this).val();
    if (type === 'individual') {
        $('tr#sender_passport_row').show();
        $('#id_sender_passport').prop('required',true);
        $('label[for="id_sender_passport"]').addClass('required')
        $('tr#sender_inn_row').hide();
        $('#id_sender_tin').prop('required',false);
        $('label[for="id_sender_tin"]').removeClass('required')
    } else {
        $('tr#sender_passport_row').hide();
        $('#id_sender_passport').prop('required',false);
        $('label[for="id_sender_passport"]').removeClass('required')
        $('tr#sender_inn_row').show();
        $('#id_sender_tin').prop('required',true);
        $('label[for="id_sender_tin"]').addClass('required')
    }
});

$('#id_receiver_type').change(function() {
    const type = $(this).val();
    if (type === 'individual') {
        $('tr#receiver_passport_row').show();
        $('#id_receiver_passport').prop('required',true);
        $('label[for="id_receiver_passport"]').addClass('required')
        $('tr#receiver_inn_row').hide();
        $('#id_receiver_tin').prop('required',false);
        $('label[for="id_receiver_tin"]').removeClass('required')
    } else {
        $('tr#receiver_passport_row').hide();
        $('#id_receiver_passport').prop('required',false);
        $('label[for="id_receiver_passport"]').removeClass('required')
        $('tr#receiver_inn_row').show();
        $('#id_receiver_tin').prop('required',true);
        $('label[for="id_receiver_tin"]').addClass('required')
    }
});

$('#sender_payer').on('change',function(){
    if($(this).is(':checked')){
        let otherSide = $('#receiver_payer')
        if(otherSide.is(':checked')){otherSide.click()}
        $('#id_sender_name').prop('disabled',true).val($('#id_payer_name').val());
        $('#id_sender_phone').prop('disabled',true).val($('#id_payer_phone').val());
        $('#id_sender_contact').prop('disabled',true).val($('#id_payer_contact').val());
        $('#id_sender_type').prop('disabled',true).val($('#id_payer_type').val()).change();
        $('#id_sender_passport').prop('disabled',true).val( $('#id_payer_passport').val() );
        $('#id_sender_tin').prop('disabled',true).val( $('#id_payer_tin').val());
    }else{
        let resetBlank = [
            '#id_sender_name', '#id_sender_phone', '#id_sender_contact', '#id_sender_passport', '#id_sender_tin'
        ]

        let resetNoBlank = [
            '#id_sender_type'
        ]

        resetBlank.forEach(el => resetInput($(el)))
        resetNoBlank.forEach(el => resetInput($(el), false))
    }
});

$('#receiver_payer').on('change',function(){
    if($(this).is(':checked')){
        let otherSide = $('#sender_payer')
        if(otherSide.is(':checked')){otherSide.click()}
        $('#id_receiver_name').prop('disabled',true).val($('#id_payer_name').val());
        $('#id_receiver_phone').prop('disabled',true).val($('#id_payer_phone').val());
        $('#id_receiver_contact').prop('disabled',true).val($('#id_payer_contact').val());
        $('#id_receiver_type').prop('disabled',true).val($('#id_payer_type').val()).change();
        $('#id_receiver_passport').prop('disabled',true).val($('#id_payer_passport').val());
        $('#id_receiver_tin').prop('disabled',true).val($('#id_payer_tin').val());
    }else{
        let resetBlank = [
            '#id_receiver_name', '#id_receiver_phone', '#id_receiver_contact', '#id_receiver_passport', '#id_receiver_tin'
        ]

        let resetNoBlank = [
            '#id_receiver_type'
        ]

        resetBlank.forEach(el => resetInput($(el)))
        resetNoBlank.forEach(el => resetInput($(el), false))
    }
});

$("#id_payer_name").on("keyup", function(){
    if($('#sender_payer').is(':checked')){
        $('#id_sender_name').val($(this).val());
    }
    if($('#receiver_payer').is(':checked')){
        $('#id_receiver_name').val($(this).val());
    }
})

$("#id_payer_phone").on("keyup", function(){
    if($('#sender_payer').is(':checked') ){
        $('#id_sender_phone').val($(this).val());
    }
    if($('#receiver_payer').is(':checked')){
        $('#id_receiver_phone').val($(this).val());
    }
})

$("#id_payer_contact").on("keyup", function(){
    if($('#sender_payer').is(':checked')){
        $('#id_sender_contact').val( $(this).val() );
    }
    if($('#receiver_payer').is(':checked')){
        $('#id_receiver_contact').val($(this).val());
    }
})

$("#id_payer_passport").on("keyup", function(){
    if($('#sender_payer').is(':checked')){
        $('#id_sender_passport').val($(this).val());
    }
    if($('#receiver_payer').is(':checked')){
        $('#id_receiver_passport').val($(this).val());
    }
})

$("#id_payer_tin").on("keyup", function(){
    if($('#sender_payer').is(':checked')){
        $('#id_sender_tin').val($(this).val());
    }
    if($('#receiver_payer').is(':checked')){
        $('#id_receiver_tin').val($(this).val());
    }
})

$('#send_precise').change( function() {
    if($(this).is(':checked')) {
        $('#id_send_precise_address').prop('disabled', false);
    } else {
        $('#id_send_precise_address').prop('disabled', true);
    }
});

$('#receive_precise').change( function() {
    if($(this).is(':checked')) {
        $('#id_receiver_precise_address').prop('disabled', false);
    } else {
        $('#id_receiver_precise_address').prop('disabled', true);
    }
});
