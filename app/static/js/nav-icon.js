$('#nav-icon').click(function(){
    $(this).toggleClass('open');
    let menu = $('#menu')
    if (menu.css('display') === 'none') {
        $('html').css('overflow', 'hidden');
		$('#retro_head').css('position', 'fixed');
        menu.css('display', 'flex');
    } else {
        $('html').removeAttr('style');
        $('#retro_head').removeAttr('style');
        menu.removeAttr('style');
    }
});
