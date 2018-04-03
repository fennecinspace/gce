$(document).ready(function() {
    user_input = $('form div')
    $('form').submit(function() {
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(),
            type: 'POST',
            url: '/',
            success: function(response) {
                if (JSON.parse(response).success) {
                    $('#login_area').css({opacity:'0',transform:'scale(0)',transition:'0.7s'})
                    setTimeout(() => {window.location.replace('')},700)   
                }
                else 
                    shake(user_input)
            }
        });
        return false;
    });
});


function shake(obj_to_shake) {
    var interval = 100;
    var distance = 10;
    var times = 4;

    obj_to_shake.css('position', 'relative');

    for (var iter = 0; iter < (times + 1) ; iter++) {
        obj_to_shake.animate({
            left: ((iter % 2 == 0 ? distance : distance * -1))
        }, interval);
    }                                                                                                          
    obj_to_shake.animate({ left: 0 }, interval);
}