feedback_form = $("#feedback_form")
feedback_form.submit(function (event) {
    event.preventDefault()
    if (!$('#sub_phone').val() && !$('#sub_email').val()) {
        $('#not_full').css('display', 'table-row');
        document.getElementById("content").scrollIntoView({block: "start", behavior: "smooth"})
    } else {
        $('#not_full').css('display', 'none');
        const raw_data = feedback_form.serialize();
        $.post(
            "/php/redirect_feedback.php",
            raw_data,
            function() {
                $('#alert').css('display', 'flex');
            }
        );
        $('#alert').css('display', 'flex');
        feedback_form.trigger("reset");
    }
});

$('#cross').click(
    function(){
        $('#alert').css('display', 'none');
    }
)