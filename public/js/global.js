// JS allowing responsive/retractable sidebar to function correctly
$(document).ready(function() {
    var $menu = $('#menu'),
                $menulink = $('.menu-link'),
                $wrap = $('#wrap');

    $menulink.click(function() {
        $menulink.toggleClass('active');
        $wrap.toggleClass('active');
        return false;
    });
});
