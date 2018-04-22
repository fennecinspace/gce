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
                alert('Echec !');
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
        error: function (xhr, textStatus, thrownError){
            alert('Echec !');
        },
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
        error: function (xhr, textStatus, thrownError){
            alert('Echec !');
        },
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
            error: function (xhr, textStatus, thrownError){
                alert('Echec !');
            },
        });
    }
    else {
        shake($('#annonce_create'));
    }

    //^[a-zA-Z0-9é'èçà& ?!]+$/.test(title_annonce.value)
}


/////////////////// SAISIR PAGE /////////////////////
var upload_in_progress = false;
var module_to_upload_to = null;
var droppedFiles = null;
var upload_file_req = null;
var mouse_is_down = false;
var offset = [0,0];

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
            async: false,
            success: function (response) {
                data = JSON.parse(response);
                if (data.success){
                    $('#saisir_area').html(data.html);
                    $(element.parentElement).slideUp(500);
                    $('#copies_notes_area').slideDown(500);
                }
                else
                    alert('Echec !');
            },
            complete: function (){
                element.querySelector('.saisir_module_item_loader').style.display = "none";
            },
            error: function (xhr, textStatus, thrownError){
                alert('Echec !');
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
}

function trigger_upload(e){
    if(!upload_in_progress)
        $('#upload_copies_input').trigger('click');
}

function upload_copies(element,e){
    if (document.getElementById('upload_copies_input').value != '')
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
                }
                else
                    alert('Echec !');
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
                alert('Echec !');
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
        alert('un autre upload est en cours');
    }
}

function copie_click(elem, e) {
    e.preventDefault();
    mouse_is_down = true;
    offset = [elem.offsetLeft - e.clientX, elem.offsetTop - e.clientY];
}

function copie_unclick(elem, e) {
    e.preventDefault();
    mouse_is_down = false;
}

function copie_move(elem, e) {
    e.preventDefault(); // if this is removed mouse will unclick on move
    if (mouse_is_down) {
        if ((e.movementX > 0 && e.target.offsetLeft < 0 ) || (e.movementX < 0 && -e.target.offsetLeft < (e.target.offsetWidth - e.target.parentElement.offsetWidth)))
            elem.style.left = (e.clientX + offset[0]) + 'px';
        if ((e.movementY > 0 && e.target.offsetTop < 0 )|| (e.movementY < 0 && e.target.offsetTop > -(e.target.offsetHeight - e.target.parentElement.offsetHeight) ) )
            elem.style.top  = (e.clientY + offset[1]) + 'px';
    }
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

function go_to_top(e) {
    $('#site_container').animate({ scrollTop: 0 }, 500);
}

function go_to_bottom(e) {
    $('#site_container').animate({ scrollTop: $('#saisir_area').height() }, 500);
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
                    'file_id': data.uncompleted[i].querySelector('.mark_version_id').innerHTML,
                    'student_id': getStudentId(data.uncompleted[i]),
                }
            ];
        }

    if (data.completed) 
        for(let i = 0; i < data.completed.length; i++) {
            cmp = [
                ...cmp, 
                {
                    'version_id': data.completed[i].querySelector('.mark_version_id').innerHTML,
                    'version_note' : data.completed[i].querySelector('.saisir_student_mark').value,
                    'student_id': getStudentId(data.completed[i]),
                }
            ];
        }

        console.log(data);
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

    if (final)
        data = format_data_to_send(data, "submit");
    else
        data = format_data_to_send(data, "save");

    $.ajax({
        url: `${location.origin}/saisir/`,
        type: 'POST',
        data: data,
        async: false,
        success: function (response) {
            data = JSON.parse(response);
            if (data.success){
                $('#saisir_area').html(data.html);
            }
            else
                alert('Echec !');
        },
        complete: function (){},
        error: function (xhr, textStatus, thrownError){
            alert('Echec !');
        },
    });
}

function send_delete_request(data_to_send, type) {
    data_to_send = JSON.stringify(data_to_send);
    $.ajax({
        url: `${location.origin}/saisir/`,
        type: 'POST',
        data: {
            'type': 'delete',
            'delete_type': type,
            'data_to_delete': data_to_send,
            'module_name': module_to_upload_to,
        },
        async: false,
        success: function (response) {
            data = JSON.parse(response);
            if (data.success){
                $('#saisir_area').html(data.html);
            }
            else
                alert('Echec !');
        },
        complete: function (){},
        error: function (xhr, textStatus, thrownError){
            alert('Echec !');
        },
    });
}

function delete_entry(elem, e, type) {
    if (confirm('Confirmer la Suppression')){
        var data_to_send = [elem.parentElement.parentElement.querySelector('.mark_version_id').innerHTML];
        send_delete_request(data_to_send, type);
    }
}

function delete_multiple_entry(e) {
    e.stopPropagation();
    var data_to_send = {};
    var files, copies, ids;

    if (confirm('Confirmer la Suppression de Plusieurs Entrées')){
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

        if(Object.keys(data_to_send).length > 0){
            data_to_send = JSON.stringify(data_to_send);
            send_delete_request(data_to_send, 'both');
        }
    }
}

var files_selection_status = false;
var copies_selection_status = false;

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
        elem.parentElement.parentElement.querySelector('.select_all').innerHTML = "";
    }   
    else {
        for (let i = 0; i < all_check_boxes.length; i++)
            all_check_boxes[i].checked = true;
        elem.parentElement.parentElement.querySelector('.select_all').innerHTML = "&#10006;";
    }
        

}
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