// GETTING CSRF TOKEN
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


/////////////////// OTHER /////////////////////

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

function ltrim(str) {
    if(str == null) return str;
    return str.replace(/^\s+/g, '');
}

function rtrim(str) {
    if(str == null) return str;
    return str.replace(/\s+$/g, '');
}

function show_pop_up(content, type = 'alert', ok_callback = function(){}, cancel_callback = function(){}, last = true, second = false, general = true) {
    var overlay = document.getElementById('pop_up_message_overlay');
    overlay.innerHTML = `<div id="pop_up_message_container">
    <div id="pop_up_message">
        <div class="pop_up_message_content">${content}</div>
        <div id="pop_up_message_cancel" class="default_button_small">Annuler</div>
        <div id="pop_up_message_ok" class="default_button_small">OK</div>
    </div>`;

    overlay.querySelector('#pop_up_message_ok').addEventListener('click',function ok_fct() {
        overlay.querySelector('#pop_up_message_cancel').style.display = 'none';
        if (last) {
            $(overlay).fadeOut();
            $('#content_container').removeClass('blur_elem');
        }
        ok_callback();
    }, false);

    if (type == 'confirm') {
        overlay.querySelector('#pop_up_message_cancel').style.display = 'block';
        overlay.querySelector('#pop_up_message_cancel').addEventListener('click',function cancel_fct() {
            setTimeout(() => {
                overlay.querySelector('#pop_up_message_cancel').style.display = 'none';
            }, 400);
            $(overlay).fadeOut();
            $('#content_container').removeClass('blur_elem');
            cancel_callback();
        });
    }
    if (general)
        $('#content_container').addClass('blur_elem');
    $(overlay).fadeIn(500);
    if (second)
        shake($('#pop_up_message'));
}


/////////////////// HOME MENU /////////////////////
function load_televerser(e) {
    $('#main_loader_overlay').fadeIn();
    $('#content_container').load(`${location.origin}/rectifications #content_container > *`,()=> {
        $('#main_loader_overlay').fadeOut();
    });
}
function load_saisir(e) {
    $('#main_loader_overlay').fadeIn();
    $('#content_container').load(`${location.origin}/saisir #content_container > *`,()=> {
        $('#main_loader_overlay').fadeOut();
    });
}
function load_annonces(e) {
    $('#main_loader_overlay').fadeIn();
    $('#content_container').load(`${location.origin}/annonces #content_container > *`,()=> {
        $('#main_loader_overlay').fadeOut();
    });
}
function load_resultats(e) {
    $('#main_loader_overlay').fadeIn();
    $('#content_container').load(`${location.origin}/notes #content_container > *`,()=> {
        $('#main_loader_overlay').fadeOut();
    });
}
function load_reclamations(e) {
    $('#main_loader_overlay').fadeIn();
    $('#content_container').load(`${location.origin}/reclamations #content_container > *`,()=> {
        $('#main_loader_overlay').fadeOut();
    });
}
function load_affichages(e) {
    $('#main_loader_overlay').fadeIn();
    $('#content_container').load(`${location.origin}/affichages #content_container > *`,()=> {
        $('#main_loader_overlay').fadeOut();
    });
}
function load_consultations(e) {
    show_pop_up('not yet !');
}
function load_utilisateur(e) {
    $('#main_loader_overlay').fadeIn();
    $('#content_container').load(`${location.origin}/personnels #content_container > *`,()=> {
        $('#main_loader_overlay').fadeOut();
    });
}
function load_messenger(e) {
    show_pop_up('not yet !');
}


////////////////////// ETUDIANT /////////////////////////
/////////////////// AVATAR CHANGER //////////////////////
function avatar_selector() {
    $('#avatar_upload').trigger('click');
}

function avatar_uploader(e) {
    if (document.getElementById('avatar_upload').value != ''){
        var formData = new FormData(document.getElementById('avatar_form'));
        $('#main_loader_overlay').fadeIn();
        $.ajax({
            url: `${location.origin}/etuds/${document.getElementById('logged_in_user_id').innerHTML}/`,
            type: 'POST',
            data: formData,
            success: function (response) {
                data = JSON.parse(response);
                if (data.success){
                    document.querySelector('#profile_pic').src = data.new_avatar;
                    document.querySelector('.change_avatar').src = data.new_avatar;
                }
                else
                    setTimeout(()=>{show_pop_up('Echec !');},400);
            },
            complete: function (){
                $('#main_loader_overlay').fadeOut();
            },
            error: function (xhr, textStatus, thrownError){
                setTimeout(()=>{show_pop_up('Echec !');},400);
            },
            cache: false,
            contentType: false,
            processData: false,
        });
    }
}


////////////////// CHEF DEPARTEMENT //////////////////
/////////////////// ANNONCE PAGE /////////////////////
var create_annonce_show = false;

function annonceVisibility(element,e) {
    e.stopPropagation();
    show_pop_up('Confirmer le Changement d\'Etat d\'Affichage','confirm',() => {
        $('#main_loader_overlay').fadeIn();
        $.ajax({
            url: `${location.origin}/annonces/`,
            type: 'POST',
            data: {
                'type' : 'show_hide',
                'annonce_id' : element.parentElement.querySelector(".annonce_item_id").innerHTML,
            },
    
            success: function (response) {
                data = JSON.parse(response);
                if (data.success)
                    if (data.hideCross)
                        element.querySelector('div').className = "hide";
                    else
                        element.querySelector('div').className = "";
                else 
                    setTimeout(()=>{show_pop_up('Echec !');},400);
            },
            complete: function (){
                $('#main_loader_overlay').fadeOut();
            },
            error: function (xhr, textStatus, thrownError){
                setTimeout(()=>{show_pop_up('Echec !');},400);
            },
        });
    });
}

function deleteAnnonce(element,e) {
    e.stopPropagation();
    show_pop_up('Confirmer la Suppression','confirm',() => {
        $('#main_loader_overlay').fadeIn();
        $.ajax({
            url: `${location.origin}/annonces/`,
            type: 'POST',
            data: {
                'type' : 'delete',
                'annonce_id' : element.parentElement.querySelector(".annonce_item_id").innerHTML,
            },
            success: function (response) {
                data = JSON.parse(response);
                if (data.success){
                    element.parentElement.remove();
                    if (document.getElementsByClassName('annonce_item').length == 0)
                        document.getElementById('annonce_items_container').innerHTML = "<span id='no_annonce'>Pas de nouvelles annonces </span>";
                }
                else {
                    setTimeout(()=>{show_pop_up('Echec !');},400);
                }
            },
            complete: function (){
                $('#main_loader_overlay').fadeOut();
            },
            error: function (xhr, textStatus, thrownError){
                setTimeout(()=>{show_pop_up('Echec !');},400);
            },
        });
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

// function trigger_select(elem,e) {
//     var selections = Array.from(elem.parentElement.querySelectorAll('select'));
//     selections = selections.filter(x => x != elem);
//     if (elem.options[elem.selectedIndex].value == '')
//         for (let i = 0; i < selections.length; i++) {
//             selections[i].removeAttribute('disabled');
//             selections[i].options[0].innerHTML = selections[i].dataset.fillerText;
//         }
//     else 
//         for (let i = 0; i < selections.length; i++) {
//             selections[i].setAttribute('disabled',true);
//             selections[i].options[0].innerHTML = "Desactiver";
//         }
        
// }

function createAnnonce(e) {
    e.stopPropagation();
    var title_annonce = document.getElementById('annonce_create_title');
    var content_annonce = document.getElementById('annonce_create_content');
    var chosen_category = document.querySelector('select:not([disabled])').parentElement;
    var type;
    if (chosen_category.id == 'annonce_create_filiere')
        type = 'filiere';
    else if (chosen_category.id == 'annonce_create_parcours')
        type = 'parcours';
    else if (chosen_category.id == 'annonce_create_module')
        type = 'module' ;

    var chosen_items =  get_selected_items(chosen_category.id, 'value');
    if (title_annonce.value.trim().length > 5 && content_annonce.value.trim().length > 5 && chosen_items != null){
        var data_to_send = {
            'type': type,
            'data': chosen_items,
        };
        send_create_annonce(data_to_send, title_annonce.value, content_annonce.value);
    }
    else {
        shake($('#annonce_create'));
    }

    // ^[a-zA-Z0-9é'èçà& ?!]+$/.test(title_annonce.value)
}


function send_create_annonce(data_to_send, title, content){
    data_to_send = JSON.stringify (data_to_send);
    $('#main_loader_overlay').fadeIn();
    $.ajax({
        url: `${location.origin}/annonces/`,
        type: 'POST',
        data: {
            'type' : 'create',
            'title' : title.trim(),
            'content' : content.trim(),
            'create_group': data_to_send,
            'show' : create_annonce_show,
        },
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
                setTimeout(()=>{show_pop_up('Echec !');},400);
            }
        },
        complete: function (){
            $('#main_loader_overlay').fadeOut();
        },
        error: function (xhr, textStatus, thrownError){
            setTimeout(()=>{show_pop_up('Echec !');},400);
        },
    });
}


//////////////////// TECHNICIEN /////////////////////
/////////////////// SAISIR PAGE /////////////////////
var upload_in_progress = false;
var module_to_upload_to = null;
var droppedFiles = null;
var upload_file_req = null;
var mouse_is_down = false;
var offset = [0,0];
var files_selection_status = false;
var copies_selection_status = false;
var disable_click = false;

function filter_modules(e) {
    e.stopPropagation();
    var filter_value = e.target.value.trim().toLowerCase();
    var all_modules = $('.saisir_module_item');

    if (filter_value.length == 0)
        for (var i = 0; i < all_modules.length; i++)
            all_modules.eq(i).slideDown();
    else
        for (var x = 0; x < all_modules.length; x++)
            if (all_modules[x].querySelector('.saisir_module_title').innerHTML.toLowerCase().includes(filter_value) || all_modules[x].querySelector('.saisir_module_level').innerHTML.toLowerCase().includes(filter_value))
                all_modules.eq(x).slideDown();
            else
                all_modules.eq(x).slideUp(); 
}


function choose_module(element,e) {
    e.stopPropagation();
    e.preventDefault();
    module_to_upload_to = element.querySelector('.saisir_module_title').innerHTML;
    element.querySelector('.saisir_module_item_loader').style.display = "block";
    setTimeout(function() {
        $.ajax({
            url: `${location.origin}/saisir/`,
            type: 'POST',
            data: {
                'module_name' : module_to_upload_to,
            },
            success: function (response) {
                data = JSON.parse(response);
                if (data.success){
                    $('#saisir_area').html(data.html);
                    $(element.parentElement).slideUp(500);
                    $('#copies_notes_area').slideDown(500);
                    files_selection_status = false;
                    copies_selection_status = false;
                }
                else
                    show_pop_up('Echec !');
            },
            complete: function (){
                element.querySelector('.saisir_module_item_loader').style.display = "none";
            },
            error: function (xhr, textStatus, thrownError){
                show_pop_up('Echec !');
            },
        }); 
    },100);
 

    document.querySelector('#retour > div:last-child').innerHTML = module_to_upload_to;
   
    /// used for file dragging upload
    $('#upload_area').on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
    });
    $('#upload_area').on('dragover dragenter', function(e) {
        if(!upload_in_progress)
            $('#upload_area').addClass('upload_active_drag');
    });
    $('#upload_area').on('dragleave dragend drop', function(e) {
        if(!upload_in_progress)
            $('#upload_area').removeClass('upload_active_drag');
    });

    $('#upload_area').on('drop', function(e) {
        if(!upload_in_progress) {
            droppedFiles = e.originalEvent.dataTransfer.files;
            start_copies_upload();
        }
    });
}


function leave_upload_area(e) {
    e.stopPropagation();
    module_to_upload_to = null;
    $('#copies_notes_area').slideUp(500);
    $('#saisir_chose_module').slideDown(500);
    if (upload_file_req) {
        upload_file_req.abort();
        upload_file_req = null;
    }
    files_selection_status = false;
    copies_selection_status = false;
}


function trigger_upload(e){
    if(!upload_in_progress)
        $('#upload_input').trigger('click');
}

function upload_copies(element,e){
    if (document.getElementById('upload_input').value != '')
        start_copies_upload();
}


function start_copies_upload(){
    if (!upload_file_req) {
        ajax_data = new FormData(document.getElementById('upload_form'));
        ajax_data.append("type",'upload');
        ajax_data.append("module_name",module_to_upload_to);
        if (droppedFiles)
            for (var i = 0; i < droppedFiles.length; i++)
                ajax_data.append( 'emplacement_fichier', droppedFiles[i] );

        upload_file_req = $.ajax({
            url: `${location.origin}/saisir/`,
            type: 'POST',
            data: ajax_data,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            success: function (response) {
                data = JSON.parse(response);
                if (data.success){
                    $('#saisir_area').html(data.html);
                    files_selection_status = false;
                    copies_selection_status = false;
                }
                else
                    show_pop_up('Echec !');
                droppedFiles = null;
                upload_file_req = null;
            },
            complete: function (){
                document.getElementById('progress_percent').className = "hide";
                document.getElementById('progress_bar').className = "hide";
                document.getElementById('glisser-fichier').className = "";
                document.getElementById('selectioner-fichier').className = "";
                document.getElementById('upload_area').className = "upload_unactive_drag upload_is_allowed";
                document.getElementById('progress_percent').innerHTML = "0%";
                document.getElementById('progress_bar_status').style.width = '0%';
                upload_in_progress = false;
            },
            error: function (xhr, textStatus, thrownError){
                show_pop_up('Echec !');
            },
            xhr: function () {
                var jqXHR = new window.XMLHttpRequest();
                jqXHR.upload.addEventListener( "progress", function ( e ) {
                    if (e.lengthComputable) {
                        var percentComplete = Math.round( (e.loaded * 100) / e.total );
                        document.getElementById('progress_percent').innerHTML = percentComplete + "%";
                        document.getElementById('progress_bar_status').style.width = percentComplete + '%';
                    }
                });
                return jqXHR;
            },
            beforeSend: function() {
                document.getElementById('progress_percent').className = "";
                document.getElementById('progress_bar').className = "";
                document.getElementById('glisser-fichier').className = "hide";
                document.getElementById('selectioner-fichier').className = "hide";
                document.getElementById('upload_area').className = "upload_unactive_drag";
                upload_in_progress = true;
            }
        });
    }
    else {
        show_pop_up('un autre upload est en cours');
    }
}

function leave_image_overlay(elem, e) {
    if (document.getElementById('image_show_large'))
        $('#image_show_large').hide();
    if (document.getElementById('note_image_overlay'))
        $('#note_image_overlay').hide();
    if (document.getElementById('student_consult_center'))
        $('#student_consult_center').hide();

}

function copie_click(img, e) {
    e.preventDefault();
    if(!disable_click){
        overlay = document.getElementById('image_show_large');
        overlay.innerHTML = `<img src='${ img.src }'>` + '<div onclick="leave_image_overlay(this,event);">&#10006;</div>';
        // if (overlay.querySelector('img').clientWidth > overlay.querySelector('img').clientHeight){
        //     overlay.querySelector('img').style.width = '100%';
        //     overlay.querySelector('img').style.height = 'auto';
        // }
        // else {
        //     overlay.querySelector('img').style.width = 'auto';
        //     overlay.querySelector('img').style.height = '100%';
        // }
        $(overlay).show();
    }
}

function copie_mouse_down(elem, e) {
    e.preventDefault();
    mouse_is_down = true;
    offset = [elem.offsetLeft - e.clientX, elem.offsetTop - e.clientY];
    disable_click = false;
}


function copie_mouse_up(elem, e) {
    e.preventDefault();
    mouse_is_down = false;
}


function copie_move(elem, e) {
    e.stopPropagation();
    e.preventDefault(); // if this is removed mouse will unclick on move
    if (mouse_is_down) {
        if ((e.movementX > 0 && e.target.offsetLeft < 0 ) || (e.movementX < 0 && -e.target.offsetLeft < (e.target.offsetWidth - e.target.parentElement.offsetWidth)))
            elem.style.left = (e.clientX + offset[0]) + 'px';
        if ((e.movementY > 0 && e.target.offsetTop < 0 )|| (e.movementY < 0 && e.target.offsetTop > -(e.target.offsetHeight - e.target.parentElement.offsetHeight) ) )
            elem.style.top  = (e.clientY + offset[1]) + 'px';
    }
    disable_click = true;
}


function get_current_image(elem) {
    var all_images = elem.parentElement.querySelectorAll('img');
    for (var i = 0; i < all_images.length; i++)
        if (all_images[i].className == "")
            current_img = all_images[i];
    return current_img;
}


function next_image(elem, e){
    e.stopPropagation();
    var current_img = get_current_image(elem);
    var list_length = elem.parentElement.dataset.listLength;
    var current_index = current_img.dataset.indexNumber;

    if (current_index == list_length-1)
        elem.parentElement.querySelector('[data-index-number="0"]').className = "";
    else 
        elem.parentElement.querySelector(`[data-index-number="${ parseInt(current_index)+1 }"]`).className = "";
    current_img.className = "hide";
}


function previous_image(elem, e){
    e.stopPropagation();
    var current_img = get_current_image(elem);
    var list_length = elem.parentElement.dataset.listLength;
    var current_index = current_img.dataset.indexNumber;

    if (current_index == 0)
        elem.parentElement.querySelector(`[data-index-number="${ list_length-1 }"]`).className = "";
    else 
        elem.parentElement.querySelector(`[data-index-number="${ parseInt(current_index)-1 }"]`).className = "";
    current_img.className = "hide";
}


function change_zoom(elem, e) {
    var current_img =  get_current_image(elem);
    var zoom_level = elem.innerHTML;
    switch (zoom_level) {
        case 'x1':  elem.innerHTML = "x2";
                    current_img.style.width = "200%";
                    break;
        case 'x2':  elem.innerHTML = "x3";
                    current_img.style.width = "300%";
                    break;
        case 'x3':  elem.innerHTML = "x1";
                    current_img.style.width = "100%";
                    break;
    }
    current_img.style.top = "0";
    current_img.style.left = current_img.parentElement.clientWidth - current_img.clientWidth + "px";
}

function change_zoom_scroll(elem,e){
    if (e.shiftKey){
        e.stopPropagation();
        e.preventDefault();
        img_width_percent = elem.clientWidth / elem.parentElement.clientWidth * 100;
        if (e.deltaY < 0 && img_width_percent < 300)
            elem.style.width = img_width_percent + 4 + '%';
        if (e.deltaY > 0 && img_width_percent > 100)
            elem.style.width = img_width_percent - 4 + '%';
        
        elem.style.top = "0";
        elem.style.left = elem.parentElement.clientWidth - elem.clientWidth + "px";
    }
}


function go_to_top(e) {
    $('#site_container').animate({ scrollTop: 0 }, 500);
}

function go_to_bottom(e) {
    if(document.querySelector('#saisir_area'))
        $('#site_container').animate({ scrollTop: $('#saisir_area').height() }, 500);
    if(document.querySelector('#notes_area'))
        $('#site_container').animate({ scrollTop: $('#notes_area').height() }, 500);
}

function go_to_copies(e) {
    $('#site_container').animate({ scrollTop: document.getElementById('completed_entries_title').offsetTop - 50 }, 500);
}

function go_to_files(e) {
    $('#site_container').animate({ scrollTop: document.getElementById('uncompleted_entries_title').offsetTop - 50 }, 500);
}


function get_all_entries(parentTag) {
    var elements = document.getElementById(parentTag).querySelectorAll('.mark_item_large');
    if (elements.length == 0)
        return null;
    return elements;
}


function check_valid_entries(elements, type){ //  returns only valid entries (no empty / no false info)
    var allowed_options = document.getElementById(elements[0].querySelector('.saisir_student_name').getAttribute('list')).options;
    var valid_elements = [];

    for (var i = 0; i < elements.length; i++){
        var std_name = ltrim(elements[i].querySelector(".saisir_student_name").value);
        std_name = rtrim(std_name);
        // if (std_name == ""){ // accept empty entries
        //     valid_elements.push(elements[i]) ;
        //     continue;
        // }
        for (var j = 0; j < allowed_options.length; j++)
            if (std_name == allowed_options[j].value){
                valid_elements.push(elements[i]) ;
                break;
            }
    }
    return valid_elements;
}


function getStudentId(elem) {
    var allowed_options = document.getElementById(elem.querySelector('.saisir_student_name').getAttribute('list')).options;
    var std_name = elem.querySelector('.saisir_student_name').value;
    for (var j = 0; j < allowed_options.length; j++)
        if (std_name == allowed_options[j].value){
            return allowed_options[j].dataset.userId;
        }
    throw "Erreur: Entrée Invalid";
}


function format_data_to_send(data, type) {
    var data_to_send = { 'type': type, 'module_name': module_to_upload_to };
    var cmp = [];
    var uncmp = [];

    if (data.uncompleted) 
        for(let i = 0; i < data.uncompleted.length; i++) {
            uncmp = [
                ...uncmp, 
                {
                    'student_id': getStudentId(data.uncompleted[i]),
                    'file_id': data.uncompleted[i].querySelector('.mark_version_id').innerHTML,
                }
            ];
        }

    if (data.completed) 
        for(let i = 0; i < data.completed.length; i++) {
            cmp = [
                ...cmp, 
                {
                    'student_id': getStudentId(data.completed[i]),
                    'version_id': data.completed[i].querySelector('.mark_version_id').innerHTML,
                    'version_note' : data.completed[i].querySelector('.saisir_student_mark').value,
                }
            ];
        }

    data_to_send.data = JSON.stringify({
        'uncompleted': uncmp,
        'completed': cmp,
    });

    return data_to_send;
}


function send_copies_data(elem, e, final) {
    e.stopPropagation();
    var cmp = get_all_entries('completed_entries');
    var uncmp = get_all_entries('uncompleted_entries');
    var data = {'completed':[], 'uncompleted':[]};

    if (cmp) 
        data.completed = [...check_valid_entries(cmp)];
    if (uncmp) 
        data.uncompleted = [...check_valid_entries(uncmp)];

    if (final && data.completed) {  //submit
        for (let i = 0; i < data.completed.length; i++)
            if (data.completed[i].querySelector(".saisir_student_mark").value == ""){
                show_pop_up('Erreur : Pas tous les copies ont une note !');
                return;
            }
        
        var files = document.querySelectorAll('#uncompleted_entries .mark_item_large');
        if (files.length == 0)
            data = format_data_to_send(data, "submit"); 
        else {
            show_pop_up('Erreur : Il existe des fichiers qui n\'appartiennent à aucune copie, il faut les attribuer a un étudiant ou les supprimer !');
            return; 
        }
    }
    else  //save
        data = format_data_to_send(data, "save");
    

    if (final)
        show_pop_up('Confirmer la fin de la saisie','confirm',() => {
            show_pop_up('Êtes-vous sûr ? Vous ne pourrez plus modifier les notes et les copies !','confirm',() => {
                send_copies_data_request (data);
            },() => {}, last = true, second = true);
        },() => {}, last = false);
    else
        send_copies_data_request (data);
}

function send_copies_data_request (data){ 
    $('#main_loader_overlay').fadeIn();
    $.ajax({
        url: `${location.origin}/saisir/`,
        type: 'POST',
        data: data,
        success: function (response) {
            data = JSON.parse(response);
            if (data.success){
                if (data.type == 'submit') {
                    $('#content_container').load(`${location.origin}/saisir #content_container > *`);
                }
                else {
                    $('#saisir_area').html(data.html);
                }
                files_selection_status = false;
                copies_selection_status = false;
            }
            else
                if (data.error)
                    setTimeout(()=>{show_pop_up(data.error);},400);
                    
                else
                    setTimeout(()=>{show_pop_up('Echec !');},400);
                
        },
        complete: function (){
            $('#main_loader_overlay').fadeOut();
        },
        error: function (xhr, textStatus, thrownError){
            setTimeout(()=>{show_pop_up('Echec !');},400);
        },
    });
}


function send_delete_request(data_to_send, type) {
    data_to_send = JSON.stringify(data_to_send);
    $('#main_loader_overlay').fadeIn();
    $.ajax({
        url: `${location.origin}/saisir/`,
        type: 'POST',
        data: {
            'type': 'delete',
            'delete_type': type,
            'data_to_delete': data_to_send,
            'module_name': module_to_upload_to,
        },
        success: function (response) {
            data = JSON.parse(response);
            if (data.success){
                $('#saisir_area').html(data.html);
                files_selection_status = false;
                copies_selection_status = false;
            }
            else
                setTimeout(()=>{show_pop_up('Echec !');},400);
        },
        complete: function (){
            $('#main_loader_overlay').fadeOut();
        },
        error: function (xhr, textStatus, thrownError){
            setTimeout(()=>{show_pop_up('Echec !');},400);
        },
    });
}


function delete_entry(elem, e, type) {
    var message_confirmation;
    if (type == 'file')
        message_confirmation = 'Confirmer la Suppression';
    else if (type == 'copy')
        message_confirmation = 'Confirmer le Dégroupage';

    show_pop_up(message_confirmation, 'confirm', () => {
        var data_to_send = [elem.parentElement.parentElement.querySelector('.mark_version_id').innerHTML];
        send_delete_request(data_to_send, type);
    });
}


function delete_multiple_entry(e) {
    e.stopPropagation();
    var data_to_send = {};
    var files, copies, ids;

    files = document.querySelector('#uncompleted_entries').querySelectorAll('.check_item_checkbox:checked');
    copies = document.querySelector('#completed_entries').querySelectorAll('.check_item_checkbox:checked');

    if (files.length > 0){
        ids = [];
        for (let i = 0; i < files.length; i++)
            ids.push(files[i].parentElement.parentElement.parentElement.querySelector('.mark_version_id').innerHTML);
        data_to_send.files = ids;
    }

    if (copies.length > 0){
        ids = [];
        for (let i = 0; i < copies.length; i++)
            ids.push(copies[i].parentElement.parentElement.parentElement.querySelector('.mark_version_id').innerHTML);
        data_to_send.copies = ids;
    }


    if(Object.keys(data_to_send).length > 0)
        show_pop_up('Confirmer la Suppression de Plusieurs Entrées', 'confirm', () => {
            data_to_send = JSON.stringify(data_to_send);
            send_delete_request(data_to_send, 'both');
        });
}


function select_all_entries(elem ,e) {
    e.stopPropagation();
    var check_boxes_type = elem.parentElement.parentElement.id;
    var all_check_boxes = elem.parentElement.parentElement.querySelectorAll('.check_item_checkbox');

    var current_status;
    if (check_boxes_type == 'uncompleted_entries') {
        current_status = files_selection_status;
        files_selection_status = !files_selection_status;
    }
    else if (check_boxes_type == 'completed_entries') {
        current_status = copies_selection_status;
        copies_selection_status = !copies_selection_status;
    }

    if (current_status){
        for (let i = 0; i < all_check_boxes.length; i++)
            all_check_boxes[i].checked = false;
        elem.parentElement.parentElement.querySelector('.select_all > span').innerHTML = "";
    }
    else {
        for (let i = 0; i < all_check_boxes.length; i++)
            all_check_boxes[i].checked = true;
        elem.parentElement.parentElement.querySelector('.select_all > span').innerHTML = "&#10006;";
    }
}

function show_more(elem,e) {
    var hidden_elems = elem.parentElement.querySelectorAll('.mark_item_large.hide');
    var x; //nb of elems to show

    if (hidden_elems.length > 8)
        x = 8;
    else {
        x = hidden_elems.length;
        $(elem).hide();
    }

    for (let i = 0; i < x; i++) {
        $(hidden_elems[i]).slideDown();
        $(hidden_elems[i]).removeClass('hide');
    }
}

////////////////// ENSEIGNANT ////////////////////
//////////////////// NOTES ///////////////////////
var upload_correction_req;

function get_module_notes(element,e) {
    e.stopPropagation();
    e.preventDefault();
    module_to_upload_to = element.querySelector('.saisir_module_title').innerHTML;
    element.querySelector('.saisir_module_item_loader').style.display = "block";
    setTimeout(function() {
        $.ajax({
            url: `${location.origin}/notes/`,
            type: 'POST',
            data: {
                'module_name' : module_to_upload_to,
            },
            success: function (response) {
                data = JSON.parse(response);
                if (data.success){
                    $('#notes_area').html(data.html);
                    $(element.parentElement).slideUp(500);
                    $('#notes_editing_area').slideDown(500);
                }
                else
                    show_pop_up('Echec !');
            },
            complete: function (){
                element.querySelector('.saisir_module_item_loader').style.display = "none";
            },
            error: function (xhr, textStatus, thrownError){
                show_pop_up('Echec !');
            },
        }); 
    },100);
    document.querySelector('#retour > div:last-child').innerHTML = module_to_upload_to;
}


function leave_notes_area(e) {
    e.stopPropagation();
    module_to_upload_to = null;
    $('#notes_editing_area').slideUp(500);
    $('#saisir_chose_module').slideDown(500);
    $('#upload_area').slideUp();
}


function mark_image_viewer(elem, e , container_name = '.notes_item_image') {
    $('#note_image_overlay').html('<div onclick="leave_image_overlay(this,event);">&#10006;</div>');
    item = elem.parentElement.parentElement.querySelector(container_name + ' > div');
    $(item).clone().prependTo('#note_image_overlay');
    $('#note_image_overlay').show();
}


function send_notes_data(elem, e, final) {
    e.stopPropagation();
    var data = {
        'type' : final ? 'submit' : 'save',
        'module_name' : module_to_upload_to
    };

    data.data_to_send = [];
    var items = document.querySelectorAll('.notes_item_small');
    for (let i = 0; i < items.length; i++)
        data.data_to_send = [
            ...data.data_to_send, 
            {
                "version_id": items[i].querySelector('.notes_item_id').innerHTML,
                "mark": items[i].querySelector('.notes_item_mark_value').value,
            }];

    if (final) {
        if (document.getElementById('correction_entry'))
            data.correction = true;
        else {
            data.correction = false;
            show_pop_up('Téléverser une correction');
            return;
        }
    }

    if (final)
        show_pop_up('Confirmer la fin de la verification', 'confirm', () => {
            show_pop_up('Êtes-vous sûr ? Vous ne pourrez plus modifier les notes !', 'confirm', () => {
                send_notes_data_request (data);
            },() => {}, last = true , second = true);
        },() => {}, last = false);
    else 
        send_notes_data_request (data);
}

function send_notes_data_request (data) {
    data.data_to_send = JSON.stringify(data.data_to_send);
    $('#main_loader_overlay').fadeIn();
    $.ajax({
        url: `${location.origin}/notes/`,
        type: 'POST',
        data: data,
        success: function (response) {
            data = JSON.parse(response);
            setTimeout(() => {
                if (data.success)
                    if (data.type == 'submit') {
                        $('#notes_area').html(data.html);
                        show_pop_up('les notes ne sont plus modifiables');
                    }
                    else
                        $('#notes_area').html(data.html);
                else
                    show_pop_up('Echec !');
            }, 400);
        },
        complete: function (){
            $('#main_loader_overlay').fadeOut();
        },
        error: function (xhr, textStatus, thrownError){
            setTimeout(()=>{show_pop_up('Echec !');},400);
        },
    });
}


function toggle_upload_correction(elem, e) {
    if (elem.dataset.toggled == 'false'){
        $('#upload_area').slideDown();
        elem.dataset.toggled = 'true';
    }
    else {
        $('#upload_area').slideUp();
        elem.dataset.toggled = 'false';
    }
}

function upload_correction(element,e){
    if (document.getElementById('upload_input').value != '')
        start_correction_upload();
}

function start_correction_upload() {
    if (!upload_correction_req) {
        var ajax_data = new FormData(document.getElementById('upload_form'));
        ajax_data.append('type','upload');
        ajax_data.append('module_name',module_to_upload_to);
        if (droppedFiles)
            for (var i = 0; i < droppedFiles.length; i++)
                ajax_data.append( 'emplacement_fichier', droppedFiles[i] );

        upload_correction_req = $.ajax({
            url: `${location.origin}/notes/`,
            type: 'POST',
            data: ajax_data,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            success: function (response) {
                data = JSON.parse(response);
                if (data.success){
                    $('#notes_area').html(data.html);
                    $('#upload_area').slideUp();
                }
                else
                    show_pop_up('Echec !');
                droppedFiles = null;
                upload_correction_req = null;
            },
            complete: function (){
                document.getElementById('progress_percent').className = "hide";
                document.getElementById('progress_bar').className = "hide";
                document.getElementById('glisser-fichier').className = "";
                document.getElementById('selectioner-fichier').className = "";
                document.getElementById('upload_area').className = "upload_unactive_drag upload_is_allowed";
                document.getElementById('progress_percent').innerHTML = "0%";
                document.getElementById('progress_bar_status').style.width = '0%';
                upload_in_progress = false;
            },
            error: function (xhr, textStatus, thrownError){
                show_pop_up('Echec !');
            },
            xhr: function () {
                var jqXHR = new window.XMLHttpRequest();
                jqXHR.upload.addEventListener( "progress", function ( e ) {
                    if (e.lengthComputable) {
                        var percentComplete = Math.round( (e.loaded * 100) / e.total );
                        document.getElementById('progress_percent').innerHTML = percentComplete + "%";
                        document.getElementById('progress_bar_status').style.width = percentComplete + '%';
                    }
                });
                return jqXHR;
            },
            beforeSend: function() {
                document.getElementById('progress_percent').className = "";
                document.getElementById('progress_bar').className = "";
                document.getElementById('glisser-fichier').className = "hide";
                document.getElementById('selectioner-fichier').className = "hide";
                document.getElementById('upload_area').className = "upload_unactive_drag";
                upload_in_progress = true;
            }
        });
    }
    else {
        show_pop_up('un autre upload est en cours');
    }
}

function delete_correction(elem, e) {
    show_pop_up('Confirmer la Suppression','confirm',() => {
        var data_to_send = elem.parentElement.parentElement.querySelector('.mark_correction_id').innerHTML;
        $('#main_loader_overlay').fadeIn();
        $.ajax({
            url: `${location.origin}/notes/`,
            type: 'POST',
            data: {
                'type': 'delete',
                'data_to_delete': data_to_send,
                'module_name': module_to_upload_to,
            },
            success: function (response) {
                data = JSON.parse(response);
                if (data.success){
                    $('#notes_area').html(data.html);
                }
                else
                    setTimeout(()=>{show_pop_up('Echec !');},400);
            },
            complete: function (){
                $('#main_loader_overlay').fadeOut();
            },
            error: function (xhr, textStatus, thrownError){
                setTimeout(()=>{show_pop_up('Echec !');},400);
            },
        });
    });
}

function demande_modification_right(elem, e) {
    show_pop_up('Voulez-vous envoyer une demande au chef de departement ?','confirm', () => {
        $('#main_loader_overlay').fadeIn();
        $.ajax({
            url: `${location.origin}/notes/`,
            type: 'POST',
            data: {
                'type': 'access_right',
                'module_name': module_to_upload_to,
            },
            success: function (response) {
                data = JSON.parse(response);
                if (data.success)
                    setTimeout(()=>{show_pop_up('Une demande a été envoyée au responsable de la filière, vous recevrez une notification, si cette dernière est acceptée');},400);
                else
                    setTimeout(()=>{show_pop_up('Echec !');},400);
            },
            complete: function (){
                $('#main_loader_overlay').fadeOut();
            },
            error: function (xhr, textStatus, thrownError){
                setTimeout(()=>{show_pop_up('Echec !');},400);
            },
        });
    });
}


////////////////// CHEF ///////////////////
//////////////// AFFICHAGE ////////////////
function afficher_module(elem,e){
    e.stopPropagation();
    show_pop_up('Confirmer l\'affichage', 'confirm', () => {
        show_pop_up('Êtes-vous sûr ?', 'confirm', () => {
            var data_to_send = elem.parentElement.querySelector('.affichage_module_id').innerHTML;
            $('#main_loader_overlay').fadeIn();
            $.ajax({
                url: `${location.origin}/affichages/`,
                type: 'POST',
                data: {
                    'type': 'show',
                    'data': data_to_send,
                },
                success: function (response) {
                    data = JSON.parse(response);
                    setTimeout(()=>{
                        if (data.success){
                            show_pop_up(`les notes du module ${data.module} ont été affichées`);
                            $(elem.parentElement).slideUp().remove();
                            if (document.querySelectorAll('.affichage_item_large').length == 0)
                                document.getElementById('affichage_container').innerHTML = '<div class="saisir_item_small" id="fin_de_verification_note">Pas de Note a Afficher</div>';
                        }
                        else
                            show_pop_up('Echec !');
                    },400);
                },
                complete: function (){
                    $('#main_loader_overlay').fadeOut();
                },
                error: function (xhr, textStatus, thrownError){
                    setTimeout(()=>{show_pop_up('Echec !');},400);
                },
            });
        }, () => {}, last = true, second = true);
    }, () => {}, last = false);
}

function enable_module_modification(elem,e) {
    e.stopPropagation();
    show_pop_up('autoriser l\'enseignant a reverifié et remodifié les notes', 'confirm', () => {
        show_pop_up('Êtes-vous sûr ?', 'confirm', () => {
            var data_to_send = elem.parentElement.querySelector('.affichage_module_id').innerHTML;
            $('#main_loader_overlay').fadeIn();
            $.ajax({
                url: `${location.origin}/affichages/`,
                type: 'POST',
                data: {
                    'type': 'grant_access',
                    'data': data_to_send,
                },
                success: function (response) {
                    data = JSON.parse(response);
                    setTimeout(()=>{
                        if (data.success){
                            show_pop_up(`l'enseignant du module ${data.module} a le droit de modification, vous ne pourrez plus afficher jusqu'a qu'il renvoie les données une seconde fois`);
                            $(elem.parentElement).slideUp().remove();
                            if (document.querySelectorAll('.affichage_item_large').length == 0)
                                document.getElementById('affichage_container').innerHTML = '<div class="saisir_item_small" id="fin_de_verification_note">Pas de Note a Afficher</div>';
                        }
                        else
                            show_pop_up('Echec !');
                    },400);
                },
                complete: function (){
                    $('#main_loader_overlay').fadeOut();
                },
                error: function (xhr, textStatus, thrownError){
                    setTimeout(()=>{show_pop_up('Echec !');},400);
                },
            });
        },() => {}, last = true , second = true);
    }, () => {}, last = false);
}



function filter_affichage(e) {
    e.stopPropagation();
    var filter_value = e.target.value.trim().toLowerCase();
    var all_affichages = $('.affichage_item_large');

    if (filter_value.length == 0)
        for (var i = 0; i < all_affichages.length; i++)
        all_affichages.eq(i).slideDown();
    else
        for (var x = 0; x < all_affichages.length; x++)
            if (all_affichages[x].querySelector('.affichage_module_name').innerHTML.toLowerCase().includes(filter_value) || all_affichages[x].querySelector('.affichage_module_spec').innerHTML.toLowerCase().includes(filter_value) || all_affichages[x].querySelector('.affichage_module_parc').innerHTML.toLowerCase().includes(filter_value))
                all_affichages.eq(x).slideDown();
            else
                all_affichages.eq(x).slideUp();
}


function access_personnel_profile(elem, e){
    e.stopPropagation();
    var user_id = elem.querySelector('.personnel_user_id').innerHTML;
    var user_type = elem.querySelector('.personnel_user_type').innerHTML;
    $('#main_loader_overlay').fadeIn();
    $('#content_container').load(`${location.origin}/${user_type}/${user_id} #content_container > *`,()=> {
        $('#main_loader_overlay').fadeOut();
    });
}

function filter_users(e) {
    e.stopPropagation();
    var filter_value = e.target.value.trim().toLowerCase();
    var all_users = $('.personnel_user_item');
    
    if (filter_value.length == 0)
        for (var i = 0; i < all_users.length; i++)
            all_users.eq(i).slideDown();
    else
        for (var x = 0; x < all_users.length; x++){
            var last_name = all_users[x].querySelector('.personnel_user_lastname').innerHTML.trim().toLowerCase();
            var first_name = all_users[x].querySelector('.personnel_user_firstname').innerHTML.trim().toLowerCase();
            if (first_name.includes(filter_value) || last_name.includes(filter_value) || (last_name + " " + first_name).includes(filter_value) || (first_name + " " + last_name).includes(filter_value))
                all_users.eq(x).slideDown(); 
            else
                all_users.eq(x).slideUp(); 
        }
}


////////////////////// SAVING ENABLING ///////////////////
function enable_saving(e) {
    e.stopPropagation();
    $('.data_save_btn').removeClass('hide');
    $('.data_submit_btn').addClass('hide');
}

///////////////////// STUDENT NOTES ///////////////////////
function toggle_std_center(elem, e) {
    e.stopPropagation();
    // clearing old data
    var all_tabs = document.querySelectorAll('.std_center_content');
    for (let t = 0; t < all_tabs.length; t++)
        all_tabs[t].innerHTML = "";  
    // resetting general info
    document.getElementById('std_center_module_id').innerHTML = "";
    document.getElementById('std_center_item_year').innerHTML = "";
    document.getElementById('std_center_item_id').innerHTML = "";
    document.getElementById('std_center_version_id').innerHTML = "";

    //reseting to copy
    hide_center_element("std_center_correct");
    hide_center_element("std_center_reclam");
    show_center_element("std_center_copy");

    //getting general info
    document.getElementById('std_center_module_id').innerHTML = elem.parentElement.parentElement.querySelector('.notes_item_name_value').dataset.moduleId; 
    document.getElementById('std_center_item_year').innerHTML = elem.parentElement.parentElement.dataset.itemYear; 
    document.getElementById('std_center_item_id').innerHTML = elem.parentElement.parentElement.dataset.itemId;
    document.getElementById('std_center_version_id').innerHTML = elem.parentElement.parentElement.dataset.versionId;

    // getting copy data
    var copy_item = elem.parentElement.parentElement.querySelector('.notes_item_image > div');
    $(copy_item).clone().appendTo('#std_center_copy > .std_center_content');

    // getting correction data
    var correction_item = elem.parentElement.parentElement.querySelector('.notes_item_correction > div');
    if (correction_item != null) // if correction exists
        $(correction_item).clone().appendTo('#std_center_correct > .std_center_content');

    //reclamation tab filler
    var reclamation_item =  elem.parentElement.parentElement.querySelector('.notes_item_reclam > div');
    $(reclamation_item).clone().appendTo('#reclam_tab');

    // showing center
    document.getElementById("student_consult_center").style.display = "block";
}


function hide_center_element(elem_id) {
    document.getElementById(elem_id).style.display = "none"; //content
    document.getElementById(elem_id + "_btn").style.background = "transparent"; //button
}


function show_center_element(elem_id) {
    document.getElementById(elem_id).style.display = "block"; //content
    document.getElementById(elem_id + "_btn").style.background = "rgba(189, 189, 189, 0.5)"; //button
}


function change_student_center_tab (elem, e) {
    switch(elem.id) {
        case "std_center_copy_btn": 
            hide_center_element("std_center_correct");
            hide_center_element("std_center_reclam");
            show_center_element("std_center_copy");
            break;
        case "std_center_correct_btn": 
            hide_center_element("std_center_copy");
            hide_center_element("std_center_reclam");
            show_center_element("std_center_correct");
            break;
        case "std_center_reclam_btn": 
            hide_center_element("std_center_copy");
            hide_center_element("std_center_correct");
            show_center_element("std_center_reclam");
            break;
    }
}


function reclamation_manager(type, elem, e) {
    e.stopPropagation();
    var module_id = document.getElementById('std_center_module_id').innerHTML;
    var version_id = document.getElementById('std_center_version_id').innerHTML;

    if (module_id == "") {
        show_pop_up('Erreur !');
        return;
    }

    if (type == 'create')
        create_reclamation(module_id, version_id);
    else if (type == 'delete')
        delete_reclamation(elem);
}


function create_reclamation(module_id, version_id) {
    var reclam_title = document.getElementById('reclam_tab').querySelector('input[name="reclamation_title"]').value;
    var reclam_content = document.getElementById('reclam_tab').querySelector('textarea[name="reclamation_content"]').value;
    if (reclam_title.trim().length > 5 && reclam_content.trim().length > 5)
        show_pop_up('Voulez vous Créer une Réclamation ?',"confirm",() => {
            show_pop_up('Êtes-vous sûr ?',"confirm",() => {
                var student_id = document.getElementById('logged_in_user_id').innerHTML;
                $('#main_loader_overlay').fadeIn();
                $.ajax({
                    url: `${location.origin}/etud_reclamation_handler_VIEW/`,
                    type: 'POST',
                    data: {
                        'type': 'create',
                        'module_id': module_id,
                        'version_id': version_id,
                        'student_id': student_id,
                        'title': reclam_title,
                        'content': reclam_content,
                    },
                    success: function (response) {
                        data = JSON.parse(response);
                        setTimeout(()=> {
                            if (data.success){
                                if (data.error) {
                                    show_pop_up(`Il existe des réclamations pas encore réglées !`, 'alert', ()=>{}, ()=>{}, last= true, second = false, general = false);
                                }
                                else  {
                                    show_pop_up(`Une reclamation a été créé, elle sera réglée par l'enseignant du module`, 'alert', ()=>{}, ()=>{}, last= true, second = false, general = false);
                                    update_reclamation_tab(data.html,'create');
                                    $(document.querySelector('#reclam_tab .notes_item_reclam_new')).slideUp();
                                    $(document.querySelector('#reclam_tab .copie_is_archived')).slideDown();
                                }
                            }
                            else
                                show_pop_up('Echec !', 'alert', ()=>{}, ()=>{}, last= true, second = false, general = false);
                        }, 400);
                    },
                    complete: function (){
                        $('#main_loader_overlay').fadeOut();
                    },
                    error: function (xhr, textStatus, thrownError){
                        setTimeout(()=>{
                            show_pop_up('Echec !', 'alert', ()=>{}, ()=>{}, last= true, second = false, general = false);
                        },400); 
                    },
                });

            }, () => {},last = true, second = true, general = false);
        }, () => {},last = false, second = false, general = false);
    else 
        shake($('#reclam_tab'));
}


function delete_reclamation(elem) {
    show_pop_up('Voulez vous Supprimer cette Réclamation ?',"confirm",() => {
        show_pop_up('Êtes-vous sûr ?',"confirm",() => {
            var reclam_id = elem.parentElement.parentElement.querySelector('.reclam_id').innerHTML;
            
            $('#main_loader_overlay').fadeIn();
            $.ajax({
                url: `${location.origin}/etud_reclamation_handler_VIEW/`,
                type: 'POST',
                data: {
                    'type': 'delete',
                    'reclam_id': reclam_id,
                },
                success: function (response) {
                    data = JSON.parse(response);
                    setTimeout(() => {
                        if (data.success){
                            show_pop_up(`La réclamation a été supprimé !`, 'alert', ()=>{}, ()=>{}, last= true, second = false, general = false);
                            update_reclamation_tab(data.html,'delete', elem.parentElement.parentElement);
                            $(document.querySelector('#reclam_tab .notes_item_reclam_new')).slideDown();
                            $(document.querySelector('#reclam_tab .copie_is_archived')).slideUp();
                        }
                        else
                            show_pop_up('Echec !', 'alert', ()=>{}, ()=>{}, last= true, second = false, general = false);
                    }, 400);
                },
                complete: function (){
                    $('#main_loader_overlay').fadeOut();
                },
                error: function (xhr, textStatus, thrownError){
                    setTimeout(() => {
                        show_pop_up('Echec !', 'alert', ()=>{}, ()=>{}, last= true, second = false, general = false);
                    }, 400);
                },
            });

        }, () => {},last = true, second = true, general = false);
    }, () => {},last = false, second = false, general = false);
}

function update_reclamation_tab(data, type, elem = null){
    /*
        updating tab first
        then pasting tab on to main content
    */
    var old_reclams_section = document.querySelector('#reclam_tab > div .notes_item_reclam_old > div');

    if (type == 'create'){
        if (old_reclams_section.querySelectorAll('.old_reclam_item').length == 0){
            var parent = old_reclams_section.parentElement;
            $(parent).hide();
            parent.innerHTML = data;
            $(parent).slideDown();
        }
        else {
            var relcams_title = old_reclams_section.querySelector('.reclam_second_title');
            new_old_item = $(data).find('.old_reclam_item')[0];
            $(new_old_item).addClass('hide');
            relcams_title.insertAdjacentElement('afterend', new_old_item);
            $(new_old_item).slideDown();
        }
    }
    else if (type == 'delete'){
        $(elem).slideUp(400);
        setTimeout(() => {
            elem.remove();
            console.log(old_reclams_section.querySelector('.old_reclam_item'));
            if (old_reclams_section.querySelectorAll('.old_reclam_item').length == 0){
                $(old_reclams_section.querySelector('.reclam_second_title')).slideUp();
                setTimeout(()=> {
                    old_reclams_section.querySelector('.reclam_second_title').remove();
                },400);
            }
        }, 400);
    }

    // updating main content
    setTimeout(()=>{
        
        var current_item_id = document.getElementById('std_center_item_id').innerHTML;
        var current_item_year =  document.getElementById('std_center_item_year').innerHTML;
        var tmp_query = `.notes_item_small[data-item-year='${current_item_year}'][data-item-id='${current_item_id}'] .notes_item_reclam_old`;
        var main_reclamation_item =  document.querySelector(tmp_query);
        var tab_reclams_section = document.querySelector('#reclam_tab > div .notes_item_reclam_old');
        main_reclamation_item.innerHTML = tab_reclams_section.innerHTML;
    
    },1000);
}


/////////////////// ENSG RECLAM //////////////////////
function mark_as_corrected(elem) {
    elem.dataset.state = "corrected";
}


function reclam_image_viewer(elem, e , container_name) {
    $('#note_image_overlay').html('<div onclick="leave_image_overlay(this,event);">&#10006;</div>');
    item = elem.parentElement.parentElement.parentElement.parentElement.querySelector(container_name + ' > div');
    $(item).clone().prependTo('#note_image_overlay');
    $('#note_image_overlay').show();
}

function handle_reclamation(elem, e, type){
    e.stopPropagation();
    var value = validate_reclam_ensg(elem, type);
    if (value == 'invalid'){
        return;
    }

    var message;
    if (type == 'accept')
        message = 'Voulez vous corriger cette note ?';
    else if (type == 'refuse')
        message = 'Voulez vous rejeter cette réclamation ?';


    // if everything is valid send request on user permission 
    show_pop_up(message,"confirm",() => {
        show_pop_up('Êtes-vous sûr ?',"confirm",() => {
            var copie_id = elem.parentElement.parentElement.querySelector('.notes_item_id').innerHTML;
            var reclam_id = elem.parentElement.parentElement.querySelector('.reclam_item_id').innerHTML;

            $('#main_loader_overlay').fadeIn();
            $.ajax({
                url: `${location.origin}/ensg_reclamation_handler_VIEW/`,
                type: 'POST',
                data: {
                    'type': type,
                    'reclam_id': reclam_id,
                    'copie_id': copie_id,
                    'note': value,
                },
                success: function (response) {
                    data = JSON.parse(response);
                    setTimeout(() => {
                        if (data.success){
                            if (type == 'accept')
                                show_pop_up(`La réglamation a été approuvée, n'oblier pas de corrigé la copie, et de demander au technicien de la téléverser !`);
                            else 
                                show_pop_up(`La réglamation a été rejetée`);
                            update_ensg_reclamation_page(elem, value, type);
                        }
                        else
                            show_pop_up('Echec !');
                    }, 400);
                },
                complete: function (){
                    $('#main_loader_overlay').fadeOut();
                },
                error: function (xhr, textStatus, thrownError){
                    setTimeout(() => {
                        show_pop_up('Echec !');
                    }, 400);
                },
            });

        }, () => {},last = true, second = true);
    }, () => {},last = false, second = false);
}

function validate_reclam_ensg(elem, type) {
    var note_input = elem.parentElement.parentElement.querySelector('.notes_item_info_mark > input');
    if (type == 'accept'){
        if (note_input.dataset.state == "original") {
            show_pop_up("Corriger la note avant de l'envoyer au technicien pour qu'il téléverse la nouvelle copie");
            return 'invalid';
        }
        if (isNaN(parseFloat(note_input.value)) || parseFloat(note_input.value) > 20 || parseFloat(note_input.value) < 0) {
            show_pop_up("Note Invalide");
            return 'invalid';
        }
        return parseFloat(note_input.value);
    }
    else if (type == 'refuse'){
        if (isNaN(parseFloat(note_input.dataset.originalNote)) || parseFloat(note_input.dataset.originalNote) > 20 || parseFloat(note_input.dataset.originalNote) < 0)
            return 'invalid';
        return parseFloat(note_input.dataset.originalNote);
    }
}


// function update_ensg_reclamation_page(elem, note, type) {
//     var reclam_area = document.getElementById('reclam_area');
//     var reclam_item =  $(elem.parentElement.parentElement).clone()[0];

//     $(elem.parentElement.parentElement).slideUp();
//     setTimeout(() => {
//         // deleting waiting entry
//         elem.parentElement.parentElement.remove();
        
//         // setting updated note
//         reclam_item.querySelector('.notes_item_info_mark > input').value = note;

//         // deleting buttons 
//         reclam_item.querySelector('.reclam_buttons_area').remove();
        
//         var statut;
//         if (type == 'accept')
//             statut = 'Oui';
//         else if (type == 'refuse')
//             statut = 'Non';
//         var approved_status = $(`
//             <div class="reclam_ensg_info_item">
//                 <div class="reclam_ensg_info_label">Approuvée :</div>
//                 <div class="reclam_ensg_info_value">${statut}</div>
//             </div>
//             `)[0];
//         reclam_item.querySelector('.reclam_ensg_info').appendChild(approved_status);

//         if (reclam_area.querySelector('#reclamations_done') == null) {
//             // creating new done area
//             var new_reclamations_done_area = document.createElement('div');
//             new_reclamations_done_area.id = "reclamations_done";
//             new_reclamations_done_area.appendChild($('<div class="default_title annee_title">Réglées</div>')[0]);
//             new_reclamations_done_area.appendChild(reclam_item);
//             new_reclamations_done_area.className = "hide";
//             //inserting area after waiting section
//             document.getElementById('reclamations_waiting').insertAdjacentElement('afterend',new_reclamations_done_area);
//             $(new_reclamations_done_area).slideDown();
//         }
//         else  {
//             $(reclam_item).addClass('hide');
//             reclam_area.querySelector('#reclamations_done > .default_title').insertAdjacentElement('afterend',reclam_item);
//             $(reclam_item).slideDown();
//         }

//         if (reclam_waiting_container.querySelectorAll('.reclam_ensg_item').length == 0)
//             $(reclam_waiting_container.querySelector('.default_title.annee_title')).slideUp();
//     }, 400);
// }

function update_ensg_reclamation_page(elem, note, type) {
    var reclam_area = document.getElementById('reclam_area');
    var reclam_item =  elem.parentElement.parentElement;
    var relam_item_id = reclam_item.querySelector(".reclam_item_id").dataset.reclamId;

    $(reclam_item).slideUp();
    setTimeout(() => {
        reclam_item.remove();
        $.get(`${location.origin}/reclamations/`, function(new_reclam_page) {
            if (reclam_area.querySelector('#reclamations_done') == null) {
                var new_done_area = $(new_reclam_page).find('#reclamations_done')[0];
                $(new_done_area).addClass("hide");
                reclam_area.querySelector('#reclamations_waiting').insertAdjacentElement('afterend', new_done_area);
                $(new_done_area).slideDown();
            }
            else {
                var new_reclam_item = $(new_reclam_page).find(`[data-reclam-id="${relam_item_id}"]`)[0].parentElement.parentElement;
                $(new_reclam_item).addClass("hide");
                reclam_area.querySelector('#reclamations_done > .default_title').insertAdjacentElement('afterend',new_reclam_item);
                $(new_reclam_item).slideDown();
            }
        },'html');
        if (reclam_area.querySelectorAll('#reclamations_waiting .reclam_ensg_item').length == 0)
            $(reclam_area.querySelector('#reclamations_waiting .default_title.annee_title')).slideUp();
    }, 450);
}

//////////////// TECH RECTIFICATION /////////////
var upload_rect_req = null;

function rect_upload(elem, e) {
    e.stopPropagation();
    $('#upload_input').trigger('click');
}

function upload_rect(elem,e) {
    e.stopPropagation();
    show_pop_up('Téléverser ?','confirm',() => {
        var version_id = elem.parentElement.parentElement.querySelector(".version_id").innerHTML;
        var module_id = elem.parentElement.parentElement.querySelector(".rect_item_value[data-id-module]").dataset.idModule;
        
        if (!upload_rect_req) {
            ajax_data = new FormData(document.getElementById('upload_form'));
            ajax_data.append("version_id", version_id);
            ajax_data.append("module_id", module_id);
            ajax_data.append("type", "upload");

            upload_rect_req = $.ajax({
                url: `${location.origin}/rectifications/`,
                type: 'POST',
                data: ajax_data,
                dataType: 'json',
                cache: false,
                contentType: false,
                processData: false,
                success: function (response) {
                    data = JSON.parse(response);
                    if (data.success){
                        update_rect_item(elem ,"upload");
                    }
                    else
                        show_pop_up('Echec !');
                    upload_rect_req = null;
                },
                complete: function (){
                },
                error: function (xhr, textStatus, thrownError){
                    show_pop_up('Echec !');
                },
                xhr: function () {
                    var jqXHR = new window.XMLHttpRequest();
                    jqXHR.upload.addEventListener( "progress", function ( e ) {
                        if (e.lengthComputable) {
                            // var percentComplete = Math.round( (e.loaded * 100) / e.total );
                            // document.getElementById('progress_percent').innerHTML = percentComplete + "%";
                            // document.getElementById('progress_bar_status').style.width = percentComplete + '%';
                        }
                    });
                    return jqXHR;
                },
                beforeSend: function() {
                    upload_in_progress = true;
                }
            });
        }
        else {
            show_pop_up('un autre upload est en cours');
        }
    });
}


function rect_reset_accept(elem, e, type) {
    e.stopPropagation();
    var version_id = elem.parentElement.querySelector(".version_id").innerHTML;
    var module_id = elem.parentElement.querySelector(".rect_item_value[data-id-module]").dataset.idModule;
    var message;
    
    if (type == 'accept')
        message = 'Voulez vous confirmer cette réctification';
    else if (type == 'reset')
        message = 'Réinitialiser pour téléverser de nouveaux fichiers ?';
    
    show_pop_up(message ,'confirm',() => {
        show_pop_up("Êtes-vous sûr ?" ,'confirm',() => {
            $('#main_loader_overlay').fadeIn();
            $.ajax({
                url: `${location.origin}/rectifications/`,
                type: 'POST',
                data: {
                    'type': type,
                    'version_id': version_id,
                    'module_id': module_id,
                },
                success: function (response) {
                    data = JSON.parse(response);
                    setTimeout(() => {
                        if (data.success){
                            if (type == 'accept'){
                                show_pop_up(`Réctification réglée !`);
                                $(elem.parentElement).slideUp();
                                setTimeout(() => {
                                    elem.parentElement.remove();
                                    if (document.querySelectorAll('.rect_item').length == 0)
                                        document.getElementById('rect_container').innerHTML = '<div class="saisir_item_small" id="fin_de_verification_note">Pas de Copies à Réctifier</div>';
                                },450);
                            }

                            else if (type == 'reset') {
                                show_pop_up(`Vous pouvez téléverser une nouvelle copie !`);
                                update_rect_item(elem, "reset");
                            }
                        }
                        else
                            show_pop_up('Echec !');
                    }, 400);
                },
                complete: function (){
                    $('#main_loader_overlay').fadeOut();
                },
                error: function (xhr, textStatus, thrownError){
                    setTimeout(() => {
                        show_pop_up('Echec !');
                    }, 400);
                },
            });
        },() => {}, last = true, second = true);
    },() => {}, last = false, second = false);
}

function update_rect_item(elem, type) {
    if (type == 'upload')
        elem = elem.parentElement;
    var rect_item = elem.parentElement;
    $.get(`${location.origin}/rectifications/`, function(new_rect_page) {
        var updated_item = $(new_rect_page).find(`div[data-copie-id="${rect_item.querySelector('div[data-copie-id]').dataset.copieId}"]`)[0].parentElement.parentElement;
        $(rect_item).slideUp();
        setTimeout(() => {
            rect_item.innerHTML = "";
            rect_item.innerHTML = updated_item.innerHTML;
            $(rect_item).slideDown();
        }, 800);
    },'html');
}

function rect_image_viewer(elem, e) {
    $('#note_image_overlay').html('<div onclick="leave_image_overlay(this,event);">&#10006;</div>');
    item = elem.parentElement.querySelector('.notes_item_image > div');
    $(item).clone().prependTo('#note_image_overlay');
    $('#note_image_overlay').show();
}

function filter_reclamations(e, elem) {
    e.stopPropagation();
    var filter_value = elem.value.trim().toLowerCase();
    var all_reclams = $('.reclam_ensg_item');

    if (filter_value.length == 0)
        for (var i = 0; i < all_reclams.length; i++)
            all_reclams.eq(i).slideDown();
    else 
        for (var x = 0; x < all_reclams.length; x++){
            if (is_reclam_item_in(all_reclams[x] , filter_value))
                all_reclams.eq(x).slideDown(); 
            else
                all_reclams.eq(x).slideUp(); 
        }
}

function is_reclam_item_in(item, filter) {
    var student_name = item.querySelector('.reclam_ensg_info_student').innerHTML.trim().toLowerCase();
    var module_name = item.querySelector('.reclam_ensg_info_module').innerHTML.trim().toLowerCase();
    var sujet = item.querySelector('.reclam_ensg_info_sujet').innerHTML.trim().toLowerCase();
    var disc = item.querySelector('.reclam_ensg_info_disc').innerHTML.trim().toLowerCase();
    var new_note = -1, old_note = -1;
    if (item.querySelector('.reclam_new_note_entry') != null && item.querySelector('.reclam_new_note_entry') != null) {
        new_note = item.querySelector('.reclam_new_note_entry').innerHTML;
        old_note = item.querySelector('.reclam_old_note_entry').innerHTML;
    }
    else 
        old_note = item.querySelector('.reclam_old_note_entry').value;
    
    // matching by character
    if (student_name.includes(filter) || 
        module_name.includes(filter) ||
        sujet.includes(filter) ||
        disc.includes(filter) ||
        String(old_note).includes(filter) ||
        String(new_note).includes(filter))
        return true;
    
    var approv = "non";
    var affich = "non";
    if (item.querySelector('.reclam_ensg_info_approv') != null)
        approv = item.querySelector('.reclam_ensg_info_approv').innerHTML.toLowerCase();
    if (item.querySelector('.reclam_ensg_info_affich') != null)
        affich = item.querySelector('.reclam_ensg_info_affich').innerHTML.toLowerCase(); 

    // special search
    if ((filter == "ap:oui" && approv == "oui") || 
        (filter == "ap:non" && approv == "non") ||
        (filter == "re:oui" && affich == "oui") ||
        (filter == "re:non" && affich == "non"))
        return true;

    return false;
}
