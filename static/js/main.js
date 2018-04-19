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

csrftoken = getCookie('csrftoken');

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
    if (document.getElementById('avatar_upload').value != ''){
        var formData = new FormData(document.getElementById('avatar_form'));
        $.ajax({
            url: `${location.origin}/users/${document.getElementById('logged_in_user_id').innerHTML}/`,
            type: 'POST',
            data: formData,
            async: false,
            success: function (response) {
                data = JSON.parse(response);
                if (data.success){
                    document.querySelector('#profile_pic').src = data.new_avatar;
                    document.querySelector('.change_avatar').src = data.new_avatar;
                }
                else
                    alert('Erreur !');
            },
            complete: function (){
            },
            error: function (xhr, textStatus, thrownError){
            },
            cache: false,
            contentType: false,
            processData: false,
        });
    }
}


/////////////////// HOME MENU /////////////////////
function load_televerser(e) {
    alert('no yet');
}
function load_saisir(e) {
    $('#content_container').load(`${location.origin}/saisir #content_container > *`);
}
function load_annonces(e) {
    $('#content_container').load(`${location.origin}/annonces #content_container > *`);
}
function load_resultats(e) {
    alert('no yet');
}
function load_reclamations(e) {
    alert('no yet');
}
function load_affichages(e) {
    alert('no yet');
}
function load_consultations(e) {
    alert('no yet');
}
function load_utilisateur(e) {
    alert('no yet');
}
function load_messenger(e) {
    alert('no yet');
}

/////////////////// ANNONCE PAGE /////////////////////
var create_annonce_show = false;

function annonceVisibility(element,e) {
    e.stopPropagation();
    $.ajax({
        url: `${location.origin}/annonces/`,
        type: 'POST',
        data: {
            'type' : 'show_hide',
            'annonce_id' : element.parentElement.querySelector(".annonce_item_id").innerHTML,
        },
        async: false,
        success: function (response) {
            data = JSON.parse(response);
            if (data.success){
                if (data.hideCross){
                    element.querySelector('div').className = "hide";
                }
                else
                    element.querySelector('div').className = "";
            }
            else {
                alert('Echec !');
            }
        },
        complete: function (){},
        error: function (xhr, textStatus, thrownError){},
    });
}

function deleteAnnonce(element,e) {
    e.stopPropagation();
    $.ajax({
        url: `${location.origin}/annonces/`,
        type: 'POST',
        data: {
            'type' : 'delete',
            'annonce_id' : element.parentElement.querySelector(".annonce_item_id").innerHTML,
        },
        async: false,
        success: function (response) {
            data = JSON.parse(response);
            if (data.success){
                element.parentElement.remove();
                if (document.getElementsByClassName('annonce_item').length == 0)
                    document.getElementById('annonce_items_container').innerHTML = "<span id='no_annonce'>Pas de nouvelles annonces </span>";
            }
            else {
                alert('Echec !');
            }
        },
        complete: function (){},
        error: function (xhr, textStatus, thrownError){},
    });
}

function toggleCreateAnnonce(e) {
    e.stopPropagation();
    $('#annonce_add_button').slideUp();
    $('#annonce_create').slideDown();
}

function leaveCreateAnnonce(e) {
    e.stopPropagation();
    $('#annonce_create').slideUp();
    $('#annonce_add_button').slideDown();
}

function createAnnonceShow(element,e) {
    e.stopPropagation();
    if (create_annonce_show){
        element.querySelector('div').className = "";
        create_annonce_show = false;
    }
    else {
        element.querySelector('div').className = "hide";
        create_annonce_show = true;
    }
}

function createAnnonce(e) {
    e.stopPropagation();
    var title_annonce = document.getElementById('annonce_create_title');
    var content_annonce = document.getElementById('annonce_create_content');
    var module_annonce = document.getElementById('annonce_create_module');
    
    var chosen_module =  module_annonce.options[module_annonce.selectedIndex];
    if (title_annonce.value.trim().length > 5 && content_annonce.value.trim().length > 5){
        $.ajax({
            url: `${location.origin}/annonces/`,
            type: 'POST',
            data: {
                'type' : 'create',
                'title' : title_annonce.value.trim(),
                'content' : content_annonce.value.trim(),
                'module': chosen_module.value,
                'show' : create_annonce_show,
            },
            async: false,
            success: function (response) {
                data = JSON.parse(response);
                if (data.success){
                    $.get(`${location.origin}/annonces/`, function(new_annonce_page) {
                        new_annonce = $('#first_annonce_item',new_annonce_page).hide();
                        new_annonce.removeClass('left_item');
                        $('#annonce_items_container').prepend(new_annonce);
                        new_annonce.slideDown();
                        if (document.getElementById('no_annonce'))
                            $('#no_annonce').slideUp();

                    },'html');
                }
                else {
                    alert('Echec !');
                }
            },
            complete: function (){},
            error: function (xhr, textStatus, thrownError){},
        });
    }
    else {
        shake($('#annonce_create'));
    }

    //^[a-zA-Z0-9é'èçà& ?!]+$/.test(title_annonce.value)
}


/////////////////// SAISIR PAGE /////////////////////
var module_to_upload_to = null;

function filter_modules(e) {
    e.stopPropagation();
    var filter_value = e.target.value.trim().toLowerCase();
    var all_modules = $('.saisir_module_item');

    if (filter_value.length == 0)
        for (var i = 0; i < all_modules.length; i++)
            all_modules.eq(i).removeClass('hide');
    else
        for (var x = 0; x < all_modules.length; x++)
            if (all_modules[x].querySelector('.saisir_module_title').innerHTML.toLowerCase().includes(filter_value) || all_modules[x].querySelector('.saisir_module_level').innerHTML.toLowerCase().includes(filter_value))
                all_modules.eq(x).removeClass('hide'); 
            else
                all_modules.eq(x).addClass('hide');   
}

function choose_module(element,e) {
    e.stopPropagation();
    module_to_upload_to = element.querySelector('.saisir_module_title').innerHTML;
    $(element.parentElement).slideUp();
    $('#copies_notes_area').slideDown();

    $.ajax({
        url: `${location.origin}/get_unsaved_entries/`,
        type: 'POST',
        data: {
            'module_name' : module_to_upload_to,
        },
        async: false,
        success: function (response) {
            $('#saisir_area').html(response);
        },
        complete: function (){},
        error: function (xhr, textStatus, thrownError){},
    });    
}

function leave_upload_area(e) {
    e.stopPropagation();
    module_to_upload_to = null;
    $('#copies_notes_area').slideUp();
    $('#saisir_chose_module').slideDown();
}

function trigger_upload(e){
    e.stopPropagation();
    $('#upload_copies_input').trigger('click');
}

function upload_copies(element,e){
    e.stopPropagation();
}

// function drag_n_drop(e) {
//     e.stopPropagation();
//     e.preventDefault();
//     var files = e.dataTransfer.files; // Array of all files

//     for (var i=0, file; file=files[i]; i++) {
//         if (file.type.match(/image.*/)) {
//             var reader = new FileReader();

//             reader.onload = function(e2) {
//                 // finished reading file data.
//                 var img = document.createElement('img');
//                 img.src= e2.target.result;
//                 document.body.appendChild(img);
//             }

//             reader.readAsDataURL(file); // start reading the file data.
//         }
//     }
// }

/////////////////// SHAKE EFFECT /////////////////////
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