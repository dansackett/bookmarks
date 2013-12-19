$(document).ready(function() {
    ///////////////////////////////////////////
    ///////////////// AJAX ////////////////////
    ///////////////////////////////////////////

    // AJAX submission function
    function ajax_submit(selector, _function) {
        $(selector).submit(function() {
            $.ajax({
                data: $(this).serialize(),
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                success: function(response) {
                    if(response) {
                        _function(response);
                    }
                }
            });
            return false;
        });
    };

    // Favorite Bookmark Callback
    function favorite_bookmark(response) {
        // Gather elements to manipulate
        var icon = $('.' + response + ' .link-button i');
        var current_class = icon.attr('class');

        // If bookmark is currently starred, change to un-starred
        if (current_class == 'star fa fa-star'){
            icon.removeClass('fa-star');
            icon.addClass('fa-star-o');
        }
        // If bookmark is not currently starred, change to
        else {
            icon.removeClass('fa-star-o');
            icon.addClass('fa-star');
        }
    };

    ajax_submit('.favorite-bookmark', favorite_bookmark);

    // Complete Task Callback
    function complete_task(response) {
        var task = $('.' + response + ' .item button');

        if (task.parents().eq(2).hasClass('completed')) {
            task.parents().eq(2).removeClass('completed');
        }
        else {
            task.parents().eq(2).addClass('completed');
        }
    };

    ajax_submit('.complete-task', complete_task);

    // Delete Item Callback
    function delete_item(response) {
        $('.' + response).hide();
    };

    ajax_submit('.delete-form', delete_item);


    ///////////////////////////////////////////
    //////////// External Libraries ///////////
    ///////////////////////////////////////////

    // Use iCheck for checkboxes
    $('input').iCheck({
        checkboxClass: 'icheckbox_flat-green',
        radioClass: 'iradio_flat-green',
    });

    // jquery UI datepicker
    $('#id_date').datetimepicker({
        dateFormat: "yy-mm-dd",
        addSliderAccess: true,
        sliderAccessArgs: { touchonly: false }
    });


    ///////////////////////////////////////////
    ////////////// App Functions //////////////
    ///////////////////////////////////////////

    // Show placeholder if there is no value
    $('.field-widget').each(function() {
        var input = $(this).children(),
            name = input.attr('name'),
            placeholder = name.replace(/_/g, ' ');

        if(input.val() == '') {
            input.attr('placeholder', 'Enter a ' + placeholder);
        }

        if(input.attr('type') == 'password') {
            input.attr('placeholder', '********');
        }
    });

    // Hide or show individual item tools
    $('.toggle-indv-item-tools').click(function() {
        var iit = $('.indv-item-tools');
        if (iit.eq(0).css('display') == 'none') {
            iit.each(function() {
                $(this).show();
            });
        }
        else {
            iit.each(function() {
                $(this).hide();
            });
        }
    });

    // Search box will hide and show items on the page dynamically
    $('.search-box').keyup(function(e) {
        var term = $(this).val().toLowerCase();

        $('.item-block .item').each(function() {
            // If they press backspace, let's show pertaining options again
            if (e.keyCode == 8) {
                $(this).parent().show();
            }

            // If the search term doesn't match, hide it
            if ($(this).text().toLowerCase().search(term) == -1) {
                $(this).parent().hide();
            }
        });
    });

    $('.search-box').parents().eq(1).submit(function() {
        return false;
    });


    ///////////////////////////////////////////
    //////////// General Functions ////////////
    ///////////////////////////////////////////
});
