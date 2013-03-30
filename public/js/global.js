$(document).ready(function() {
    // JS allowing responsive/retractable sidebar to function correctly
    var $menu = $('#menu'),
                $menulink = $('.menu-link'),
                $wrap = $('#wrap');

    $menulink.click(function() {
        $menulink.toggleClass('active');
        $wrap.toggleClass('active');
        return false;
    });

    // AJAX submission of form
    $('.favorite-bookmark').submit(function() {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                if(response) {
                    // Gather elements to manipulate
                    icon = $('.' + response + ' .link-button i');
                    current_class = icon.attr('class');
                    favorite_class = $('.update-favorite');

                    // If bookmark is currently starred, change to un-starred
                    // and update the favorites count
                    if (current_class == 'star icon-star'){
                        icon.removeClass('icon-star');
                        icon.addClass('icon-star-empty');
                        favorite_count = Number(favorite_class.html())
                        favorite_class.html(favorite_count-1)
                    }
                    // If bookmark is not currently starred, change to
                    // starred and update favorites count
                    else {
                        icon.removeClass('icon-star-empty');
                        icon.addClass('icon-star');
                        favorite_count = Number(favorite_class.html())
                        favorite_class.html(favorite_count+1)
                    }
                }
            }
        });
        return false;
    });

    // Use iCheck for checkboxes
    $('input').iCheck({
        checkboxClass: 'icheckbox_square-grey',
        radioClass: 'iradio_square-grey',
    });
});

