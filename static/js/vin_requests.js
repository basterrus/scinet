$('.right_frame').on('click', 'button[type=button]', function () { // catch the form submit event
    event.preventDefault();
    $.ajax({ // create an AJAX call...
        data: $(this).serialize(), // get the form data
        type: $(this).attr('method'), // GET or POST
        url: $(this).attr('action'), // the file to call
        success: function (response) { // on success..
            $('#modalchangepw').html(response); // update the DIV
        }
    });
    return false;
});