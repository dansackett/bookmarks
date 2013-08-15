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

    $('.calendar td').click(function(){
        var url = $(this).find('a').attr('href');
        window.open(url, "_self");
    });

});
