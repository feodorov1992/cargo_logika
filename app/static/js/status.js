$('#status_form').submit( function(e){
    e.preventDefault();
	const raw_data = $('#status_form').serialize();
    let number = $('#order_num').val();
    alert(raw_data);
    // if (number) {
    //     $.post(
    //         '/php/redirect_status.php',
    //         raw_data,
    //         function(data) {
    //             $('#order_num_out').html(number);
    //             $('#status_output').html(data);
    //             $('#alert').css('display', 'flex');
    //         }
    //     );
    // }
});

$('#cross').click( function(){
    $('#alert').removeAttr('style');
    }
)