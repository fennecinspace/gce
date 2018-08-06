//////////////// NOTIFICATION & OPTIONS TOGGLERS ////////////////
var notification_is_toggled = false;
var options_is_toggled = false;
var slide_animation_duration = 200;

function options_hider(){
    if (options_is_toggled){ // closing options if toggled
        options_is_toggled = false;
        $("#options_box").slideUp(slide_animation_duration);
    }
}

function notifications_box_hider() {
    if (notification_is_toggled){ // closing notification if toggled
        notification_is_toggled = false;
        $("#notification_box").slideUp(slide_animation_duration);
    }
}

function notification_toggler(){
    document.getElementById('notification_button').addEventListener('click',function(e) {
        e.stopPropagation();
        if (!notification_is_toggled){
            notification_is_toggled = true;
            $("#notification_box").slideDown(slide_animation_duration);
            options_hider();
            responsive_menu_hider();
            if (search_is_toggled)
                hideSearch();
        }
        else {
            notification_is_toggled = false;
            $("#notification_box").slideUp(slide_animation_duration);
        }
    });
}

function profile_option_handler() {
    var profile_options_item = document.getElementById('profile_options_item');
    if (profile_options_item){
        profile_options_item.addEventListener('click', function(e) {
            e.preventDefault();
            var user_id = document.getElementById('logged_in_user_id').innerHTML;
            $('#main_loader_overlay').fadeIn();
            if (profile_options_item.dataset.userType == "etud")
                $('#content_container').load(`${location.origin}/etuds/${user_id} #content_container > *`,()=> {
                    $('#main_loader_overlay').fadeOut();
                });
            else if (profile_options_item.dataset.userType == "ensg")
                $('#content_container').load(`${location.origin}/ensgs/${user_id} #content_container > *`,()=> {
                    $('#main_loader_overlay').fadeOut();
                });
            else if (profile_options_item.dataset.userType == "chef")
                $('#content_container').load(`${location.origin}/chefs/${user_id} #content_container > *`,()=> {
                    $('#main_loader_overlay').fadeOut();
                });
            else if (profile_options_item.dataset.userType == "tech")
                $('#content_container').load(`${location.origin}/techs/${user_id} #content_container > *`,()=> {
                    $('#main_loader_overlay').fadeOut();
                });
            options_hider();
        });
    }
}

function options_toggler(){
    document.getElementById('profile_pic').addEventListener('click',function(e) {
        e.stopPropagation();
        if (!options_is_toggled){
            options_is_toggled = true;
            $("#options_box").slideDown(slide_animation_duration);
            notifications_box_hider();
            responsive_menu_hider();
            if (search_is_toggled)
                hideSearch();
        }
        else {
            options_is_toggled = false;
            $("#options_box").slideUp(slide_animation_duration);
        }
    });
}

function toggled_areas_closer(){ // closes the toggled windows when clicking elsewhere
    window.addEventListener('click', function(e){
        if (!document.getElementById('notification_box').contains(e.target))
            notifications_box_hider();
        if (!document.getElementById('options_box').contains(e.target))
            options_hider();
        if (!document.getElementById('menu_entries').contains(e.target))
            responsive_menu_hider();
        if (!document.getElementById('search_area').contains(e.target))
            if(!document.getElementById('search_result').contains(e.target))
                if (search_is_toggled){
                    hideSearch();
                    if (search_result_is_toggled) {
                        search_result_is_toggled = false;
                        $('#search_result').fadeOut(show_leave_duration);
                        $('#search_result_list').html('');
                    }
                }
        // use else for clicks inside the box
    });
}

//////////////// NOTIFICATIONS STATE CHANGER ////////////////
function mark_notification_as_read(){
    var allNotifications = document.querySelectorAll('.notification_id');
    for (var i = 0; i < allNotifications.length; i++)
        allNotifications[i].addEventListener('click', function(e) {
            var notification = this;
            $.ajax({
                url:`${location.origin}/notification_state_changer_VIEW/`,
                type: "POST",
                data: {
                    'notif_id': notification.querySelector('div').innerHTML
                },
                success: function(response){
                    notification.parentElement.remove();
                    if (!(document.querySelector('#notification_box div').children).length){
                        document.querySelector('#notification_box').innerHTML = '<span id="no_notification">Pas de Notification</span>';
                        document.querySelector('#notification_numbers').remove();
                    } //if there are no more notification items
                    else {
                        var notification_list = document.querySelectorAll('.notification_item');
                        document.querySelector('#notification_numbers').innerHTML = notification_list.length;
                    }
                },
                complete:function(){},
                error:function (xhr, textStatus, thrownError){}
            });
        });
}

//////////////// SEARCH MANAGERS ////////////////
var search_is_toggled = false;
var suggestions_is_toggled = false;
var search_result_is_toggled = false;
var suggestions_is_allowed = true; // added to solve suggetsions and results overlapping
var search_animation_duration = 300;
var show_leave_duration = 200;
var search_input_timeout = 500;
var search_ajax_request;
var search_in_progress = false;

function hideSearch(){
    if (search_in_progress){
        search_ajax_request.abort();    // aborting ajax request in case leaving before it's done
        search_in_progress = false;
    }
        
    search_is_toggled = false;
    $('#search_input')[0].value = ''; // emptying the search bar
    if (suggestions_is_toggled){
        suggestions_is_toggled = false;
        $('#search_suggestions').html('');
        $("#search_suggestions").hide();
    }
    if (search_result_is_toggled) {
        search_result_is_toggled = false;
        $('#search_result').fadeOut(show_leave_duration);
        $('#search_result_list').html('');
    }
    $('#search_results_loader').fadeOut(show_leave_duration);
    $('#leave_search_area').fadeOut(show_leave_duration);
    $('#search_area').animate({width:'2.6em','margin-left':'0'},search_animation_duration);
    $('#menu_entries').animate({'opacity':'1'},800); //show menu entries
    $('#menu_button').animate({'opacity':'1'},800); //show menu button 
    $('#search_overlay').fadeOut(search_animation_duration);
}

function showSearch (){
    search_is_toggled = true;
    $('#search_area').animate({width:'95%','margin-left':'5%'},search_animation_duration);
    $('#leave_search_area').show(show_leave_duration);
    $('#search_input').focus();
    $('#menu_entries').animate({'opacity':'0'},50); //hide menu entries
    $('#menu_button').animate({'opacity':'0'},50); //hide menu button 
    $('#search_overlay').fadeIn(search_animation_duration);
}

function search_result_click_handler(){
    var all_search_results = document.querySelectorAll('.search_result_item');
    for (var i = 0; i < all_search_results.length; i++) {
        all_search_results[i].addEventListener('click', function(e) {
            e.stopPropagation();
            user_id = this.querySelector('.search_result_item_id').innerHTML;
            $('#main_loader_overlay').fadeIn();
            $('#content_container').load(`${location.origin}/etuds/${user_id} #content_container > *`,()=> {
                $('#main_loader_overlay').fadeOut();
            });
            hideSearch();
        });
    }
}

function search_result_filler(returned_data){
    var html_to_inject = '';
    if (returned_data.success){
        for (var i = 0; i < returned_data.users_data.length; i++){
            user = returned_data.users_data[i];
            full_name = user.last_name;
            html_to_inject+=`
                <div class='search_result_item'>
                    <div class='search_result_item_id'>${user.id}</div>
                    <img class='search_result_item_img' src='${user.avatar}'>
                    <div class='search_result_item_info'>
                        <div class='search_result_item_name'>${user.last_name.toLowerCase()} ${user.first_name.toLowerCase()}</div>
                        <span>
                            <div class='search_result_item_group'>GROUPE ${user.group_num} - SECTION ${user.section_num} - ${user.speciality.toLowerCase()}</div>
                        </span>
                        <div class='search_result_item_filiere'>${user.level.toUpperCase()} - ${user.branch.toUpperCase()}</div>
                    </div>
                </div>`;
        }
        $('#search_result_list').html(html_to_inject);
        search_result_click_handler();
    }
    else {
        html_to_inject = "<span>Pas de Resultats</span>";
        $('#search_result_list').html(html_to_inject);
    }
    $('#search_results_loader').fadeOut(show_leave_duration);
    $('#search_result').fadeIn(show_leave_duration);
    search_result_is_toggled = true; // toggle search results
    suggestions_is_allowed = true;
    search_in_progress = false;
}

function search_query(search_entry){
    search_ajax_request = $.ajax({
        url:`${location.origin}/search_result_VIEW/`,
        type: "POST",
        data: {
            'search_entry': search_entry,
        },
        success:function(response){
            returned_data = JSON.parse(response);
            search_result_filler(returned_data);
        },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
    });
}

function start_search(e) {
    e.stopPropagation();
    if (search_is_toggled) { // get search result
        if (!search_in_progress) {
            suggestions_is_allowed = false;
            search_in_progress = true;
            setTimeout(function () {
                if (search_result_is_toggled) { // in case new search started
                    search_result_is_toggled = false;
                    $('#search_result').fadeOut(show_leave_duration);
                    $('#search_result_list').html('');
                } 
                if (suggestions_is_toggled) {
                    suggestions_is_toggled = false;
                    $('#search_suggestions').html('');
                    $("#search_suggestions").slideUp(slide_animation_duration);
                }
                $('#search_results_loader').fadeIn(show_leave_duration); // show loading
                search_query(document.getElementById('search_input').value);
            },search_input_timeout + 100);
        }
    }
    else {
        showSearch();
        options_hider();
        notifications_box_hider();
        responsive_menu_hider();
    }
}

function search_bar_manager() {
    // open search_area and search
    document.getElementById('search_button').addEventListener('click', function(e) {
        start_search(e);
    }); // search when clicking in search button
    document.getElementById('search_input').addEventListener('keyup', function(e) { // search when pressing enter
        if (e.which == 13 && !search_in_progress)
            start_search(e);
    });
    
    // close search_area
    document.getElementById('leave_search_area').addEventListener('click', function(e) {
        if (search_is_toggled)
            hideSearch();
    });
}

function search_result_manager(){
    document.getElementById('search_result_exit').addEventListener('click', function () {
        hideSearch();
    });
}

//////////////// SUGGESTIONS MANAGERS ////////////////
function suggestions_click_handler(){
    var all_suggestions = document.getElementsByClassName('suggestion_item');
    for (var i = 0; i < all_suggestions.length; i++) {
        all_suggestions[i].addEventListener('click', function(e) {
            e.stopPropagation();
            var user_id = this.querySelector('.suggestion_item_id').innerHTML;
            $('#main_loader_overlay').fadeIn();
            $('#content_container').load(`${location.origin}/etuds/${user_id} #content_container > *`,()=> {
                $('#main_loader_overlay').fadeOut();
            });
            hideSearch();
        });
    }
}

function suggestions_filler(returned_data){
    var html_to_inject = '';
    if (returned_data.success){
        for (var i = 0; i < returned_data.users_data.length; i++){
            if (i >= 5) // allow only 5 suggestions
                break;
            user = returned_data.users_data[i];
            full_name = user.last_name;
            html_to_inject +=`
            <div class='suggestion_item'>
                <div class='suggestion_item_id'>${user.id}</div>
                <img class='suggestion_item_img' src='${user.avatar}'>
                <div class='suggestion_item_info'>
                    <div class='suggestion_item_name'>${user.last_name.toLowerCase()} ${user.first_name.toLowerCase()}</div>
                    <div class='suggestion_item_filiere'>${user.level.toUpperCase()} - ${user.branch.toUpperCase()}</div>
                </div>
            </div>`;
        }
        $('#search_suggestions').html(html_to_inject);
        suggestions_click_handler();
    }
    else {
        html_to_inject = "<span>Pas de Suggestions</span>";
        $('#search_suggestions').html(html_to_inject);
    }
}

function search_bar_suggestions() {
    var typingTimer;  
    document.getElementById('search_input').addEventListener('input', function(e) {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(function(){
            if (search_is_toggled && $('#search_input')[0].value != '' && suggestions_is_allowed){
                if (search_result_is_toggled) {
                    search_result_is_toggled = false;
                    $('#search_result').fadeOut(show_leave_duration);
                    $('#search_result_list').html('');
                }
                $.ajax({
                    url:`${location.origin}/search_suggestions_VIEW/`,
                    type: "POST",
                    data: {
                        'search_entry': e.target.value,
                    },
                    success:function(response){
                        returned_data = JSON.parse(response);
                        suggestions_filler(returned_data);
                    },
                    complete:function(){},
                    error:function (xhr, textStatus, thrownError){}
                });
                suggestions_is_toggled = true;
                $("#search_suggestions").slideDown(slide_animation_duration);
            }
            else {
                suggestions_is_toggled = false;
                $('#search_suggestions').html('');
                $("#search_suggestions").slideUp(slide_animation_duration);
            }
        }, search_input_timeout);
    });
}

//////////////// MAIN MENU TOGGELER FOR RESPONSIVE DESIGN////////////////
var menu_is_toggled = false;

// device type
function set_device_type(){
    if ($(window).width() <= 799 ){
        mobile_is_on = true;
        menu_is_toggled = false;
        $('#menu_entries').hide();
        $('#menu_button').show();
    }
    else {
        mobile_is_on = false;
        menu_is_toggled = true;
        $('#menu_entries').show();
        $('#menu_button').hide();
    }
}
set_device_type(); // first load device type

function menu_toggeler(){
    window.addEventListener('resize', function(e) {
        e.stopPropagation();
        set_device_type();
    });

    document.getElementById('menu_button').addEventListener('click', function(e) {
        e.stopPropagation();
        if (!menu_is_toggled){
            menu_is_toggled = true;
            $('#menu_entries').slideDown(slide_animation_duration);
            notifications_box_hider();
            options_hider();
        }
        else {
            menu_is_toggled = false;
            $('#menu_entries').slideUp(slide_animation_duration);

        }
    });
}

//////////////// PAGE CHANGING HANDLER ////////////////
function responsive_menu_hider() {
    if (menu_is_toggled && mobile_is_on){
        menu_is_toggled = false;
        $('#menu_entries').slideUp(slide_animation_duration);
    }
}

function pages_handler() {
    document.getElementById("home_entry").addEventListener('click', function () {
        $('#main_loader_overlay').fadeIn();
        $('#content_container').load(`${location.origin} #content_container > *`,()=> {
            $('#main_loader_overlay').fadeOut();
        });
        responsive_menu_hider();
    });
    user_type = $("#logged_in_user_id").html().substring(0, 4);
    
    if (user_type == 'tech') {
        document.getElementById("upload_entry").addEventListener('click', function () {
            $('#main_loader_overlay').fadeIn();
            $('#content_container').load(`${location.origin}/rectifications #content_container > *`,()=> {
                $('#main_loader_overlay').fadeOut();
            });
            responsive_menu_hider();
        });

        document.getElementById("marks_entry").addEventListener('click', function () {
            $('#main_loader_overlay').fadeIn();
            $('#content_container').load(`${location.origin}/saisir #content_container > *`,()=> {
                $('#main_loader_overlay').fadeOut();
            });
            responsive_menu_hider();
        });
    }
    else {
        document.getElementById("news_entry").addEventListener('click', function () {
            $('#main_loader_overlay').fadeIn();
            $('#content_container').load(`${location.origin}/annonces #content_container > *`,()=> {
                $('#main_loader_overlay').fadeOut();
            });
            responsive_menu_hider();
        });

        // document.getElementById("messenger_entry").addEventListener('click', function () {
        //     show_pop_up('messenger');
        //     responsive_menu_hider();
        // });
    }

    if (user_type == 'ensg' || user_type == 'etud') {
        document.getElementById("results_entry").addEventListener('click', function () {
            $('#main_loader_overlay').fadeIn();
            $('#content_container').load(`${location.origin}/notes #content_container > *`,()=> {
                $('#main_loader_overlay').fadeOut();
            });
            responsive_menu_hider();
        });
    }

    if (user_type == 'ensg') {
        document.getElementById("error_entry").addEventListener('click', function () {
            $('#main_loader_overlay').fadeIn();
            $('#content_container').load(`${location.origin}/reclamations #content_container > *`,()=> {
                $('#main_loader_overlay').fadeOut();
            });
            responsive_menu_hider();
        });
    }

    // if (user_type == 'ensg' || user_type == 'chef') {
    //     document.getElementById("consult_entry").addEventListener('click', function () {
    //         show_pop_up('consult');
    //         responsive_menu_hider();
    //     });
    // }

    if (user_type == 'chef') {
        document.getElementById("users_entry").addEventListener('click', function () {
            $('#main_loader_overlay').fadeIn();
            $('#content_container').load(`${location.origin}/personnels #content_container > *`,()=> {
                $('#main_loader_overlay').fadeOut();
            });
            responsive_menu_hider();
        });

        document.getElementById("billboard_entry").addEventListener('click', function () {
            $('#main_loader_overlay').fadeIn();
            $('#content_container').load(`${location.origin}/affichages #content_container > *`,()=> {
                $('#main_loader_overlay').fadeOut();
            });
            responsive_menu_hider();
        });
    }
}

//////////////// FUNCTIONS CALLING ////////////////

$(document).ready(function () {
    /* notification and options */
    notification_toggler();
    options_toggler();
    mark_notification_as_read();
    profile_option_handler();

    /* search manager */
    search_bar_manager();
    search_result_manager();
    search_bar_suggestions();

    /* closing toggled area when clicking elsewhere */
    toggled_areas_closer();

    /* Menu Handler */
    menu_toggeler();
    pages_handler();

    /* socket connection */
    socket_connection();

});


/////////////////////////////// SOCKETS /////////////////////////////////////////
var socket;
function socket_connection(){
    var endpoint;

    if (location.protocol == "https:")
        endpoint = 'wss://' + location.host;
    else 
        endpoint = 'ws://' + location.host;

    socket = new WebSocket(endpoint);

    socket.onmessage = e => {
        console.log('Message', e);
    }
    socket.onopen = e => {
        console.log('Open', e);
    }
    socket.onerror = e => {
        console.log('Error', e);
    }
    socket.onclose = e => {
        console.log('Close', e);
    }
}