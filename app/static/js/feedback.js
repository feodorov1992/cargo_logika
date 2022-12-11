$("#feedback_form").submit(function (event) {
    if (!$('#id_sub_phone').val() && !$('#id_sub_email').val()) {
        $('#not_full').css('display', 'table-row');
        document.getElementById("content").scrollIntoView({block: "start", behavior: "smooth"})
        event.preventDefault()
    } else {
        return true
    }
});