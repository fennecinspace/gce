// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

csrftoken = getCookie('csrftoken')

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});


////////////////// PROFILE PAGE AVATAR CHANGER /////////////////////////////
function avatar_selector() {
    $('#avatar_upload').trigger('click');
}

function avatar_uploader(e) {
    var formData = new FormData($('#avatar_form')[0]);
    $.ajax({
        url: `${location.origin}/users/${document.getElementById('logged_in_user_id').innerHTML}/`,
        type: 'POST',
        data: formData,
        async: false,
        success: function (response) {
            data = JSON.parse(response)
            if (data['success']){
                document.querySelector('#profile_pic').src = data['new_avatar'];
                document.querySelector('.change_avatar').src = data['new_avatar'];
            }
            else
                alert('Erreur !')
        },
        complete: function (){
        },
        error: function (xhr, textStatus, thrownError){
        },
        cache: false,
        contentType: false,
        processData: false
    });
    console('Hello')
}