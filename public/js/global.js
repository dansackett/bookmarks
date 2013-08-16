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
        if (current_class == 'star icon-star'){
            icon.removeClass('icon-star');
            icon.addClass('icon-star-empty');
        }
        // If bookmark is not currently starred, change to
        else {
            icon.removeClass('icon-star-empty');
            icon.addClass('icon-star');
        }
    };

    ajax_submit('.favorite-bookmark', favorite_bookmark);

    // Complete Task Callback
    function complete_task(response) {
        var task = $('.' + response + ' .item button');

        if (task.css('text-decoration') == 'line-through') {
            task.css('text-decoration', 'none');
        }
        else {
            task.css('text-decoration', 'line-through');
        }
    };

    ajax_submit('.complete-task', complete_task);

    // Delete Task Callback
    function delete_task(response) {
        var task_items = $('.' + response);
        task_items.each(function() {
            $(this).hide();
        });
    };

    ajax_submit('.delete-task', delete_task);

    // Delete Todolist Callback
    function delete_todolist(response) {
        var todolists = $('.' + response);
        tasks.each(function() {
            $(this).hide();
        });
    };

    ajax_submit('.delete-todolist', delete_todolist);


    ///////////////////////////////////////////
    //////////// External Libraries ///////////
    ///////////////////////////////////////////

    // Use iCheck for checkboxes
    $('input').iCheck({
        checkboxClass: 'icheckbox_square-grey',
        radioClass: 'iradio_square-grey',
    });

    // jquery UI datepicker
    $('#id_date').datetimepicker({
        dateFormat: "yy-mm-dd",
        addSliderAccess: true,
        sliderAccessArgs: { touchonly: false }
    });

    // Set initial color picked color to color already selected
    var initial_color = $('#id_hex_code').val();
    $('#id_hex_code').css('background', '#' + initial_color);

    // jquery color picker
    $('#id_hex_code').ColorPicker({
        onChange: function(hsb, hex, rgb) {
            $('#id_hex_code').css('backgroundColor', '#' + hex);
            $('#id_hex_code').val(hex);
        },
    })
    .bind('keyup', function(){
        $(this).ColorPickerSetColor(this.value);
    });

    $('.calendar td').click(function(){
        var url = $(this).find('a').attr('href');
        window.open(url, "_self");
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

});
