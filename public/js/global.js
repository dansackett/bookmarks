$(document).ready(function() {
    // AJAX submission of favoriting bookmark
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
                }
            }
        });
        return false;
    });

    // AJAX submission of completing task
    $('.complete-task').submit(function() {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                if(response) {
                    // Gather elements to manipulate
                    icon = $('.' + response + ' .link-button i');
                    current_class = icon.attr('class');
                    item = $('.item-content.' + response + ' span');

                    // If task is currently completed, change to incomplete
                    if (current_class == 'star icon-circle'){
                        icon.removeClass('icon-circle');
                        icon.addClass('icon-circle-blank');
                        item.css('text-decoration', 'none');
                    }
                    // If task is not currently completely, change
                    else {
                        icon.removeClass('icon-circle-blank');
                        icon.addClass('icon-circle');
                        item.css('text-decoration', 'line-through');
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

    // If you click anywhere in the item div then you should get linked
    $('.item').click(function(){
        var url = $(this).find('.item-content').find('a').attr('href');
        window.open(url, "_self");
    });

    // Grab the data color stored on the item and animate it on hover
    $('.item').hover(function(){
        var bg_color = $(this).data('color');
        var link_color = $(this).data('link-color');
        if (!$(this).hasClass('open')) {
            $(this).animate({'background-color': '#' + bg_color, 'color': 'FFF'}, 'slow');
            $(this).find('a').animate({'color': '#FFF'}, 'slow');
        }
    },
    function(){
        var link_color = $(this).data('link-color');
        if (!$(this).hasClass('open')) {
            $(this).animate({'background-color': '#FFF', 'color': '#444'}, 'slow');
            $(this).find('a').animate({'color': '#' + link_color}, 'slow');
        }
    });

    // Hovering the page title will change the text to show we're going home
    $('.page-title').hover(function(){
        $(this).find('.current-title').hide();
        $(this).find('.home-title').show();
    },
    function(){
        $(this).find('.home-title').hide();
        $(this).find('.current-title').show();
    });

    // Manage links will open tools for item
    $('.item .manage').click(function(){
        var tools = $($(this).parent().parent().nextAll()[0]);
        var item = $(this).parent().parent();
        var color = $(item).data('color');
        // If it's open
        if ($(tools).hasClass('open')) {
            $(this).html('Manage');
            tools.removeClass('open').addClass('closed').hide('slow');
            item.removeClass('open').addClass('closed');
            item.css('background-color', '#FFF').css('color', '#444');
            item.find('a').css('color', '#' + color);
        }
        // If it's closed
        else {
            $(this).html('Close');
            tools.removeClass('closed').addClass('open').show('slow');
            item.removeClass('closed').addClass('open');
            item.css('background-color', '#' + color).css('color', '#FFF');
            item.find('a').css('color', '#FFF');
        }
        return false;
    });

    // Manage links will open tools for tag-item
    $('.tag-item .manage, .reminder-item .manage').click(function(){
        var tools = $($(this).parent().parent().nextAll()[0]);
        var item = $(this).parent().parent();
        // If it's open
        if ($(tools).hasClass('open')) {
            $(this).html('Manage');
            tools.removeClass('open').addClass('closed').hide('slow');
            item.removeClass('open').addClass('closed');
        }
        // If it's closed
        else {
            $(this).html('Close');
            tools.removeClass('closed').addClass('open').show('slow');
            item.removeClass('closed').addClass('open');
        }
        return false;
    });

    // Hover events for calendar items
    $('.calendar td').hover(function() {
        if($(this).hasClass('today') ) {
            $(this).css('cursor', 'pointer');
        }
        else if($(this).hasClass('reminder')) {
            $(this).css('cursor', 'pointer');
        }
        else {
            $(this).css('background', '#FB642B').css('cursor', 'pointer');
            $(this).find('a').css('color', '#FFF');
        }
    },
    function() {
        if($(this).hasClass('today') ) {
            $(this).css('cursor', 'pointer');
        }
        else if($(this).hasClass('reminder')) {
            $(this).css('cursor', 'pointer');
        }
        else {
            $(this).css('background', '#FFF').css('cursor', 'normal');
            $(this).find('a').css('color', '#444');
        }
    });

    $('.calendar td').click(function(){
        var url = $(this).find('a').attr('href');
        window.open(url, "_self");
    });

});
