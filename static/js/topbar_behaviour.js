//get cookie using cookie name
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

//////////////// NOTIFICATION & OPTIONS TOGGLERS ////////////////
notification_is_toggled = false;
options_is_toggled = false;
slide_animation_duration = 200;

function notification_toggler(){
    document.getElementById('notification_button').addEventListener('click',e => {
        e.stopPropagation();
        if (!notification_is_toggled){
            notification_is_toggled = true;
            $("#notification_box").slideDown(slide_animation_duration);
            if (options_is_toggled){ // closing options if toggled
                options_is_toggled = false;
                $("#options_box").slideUp(slide_animation_duration);
            }
            if (search_is_toggled)
                hideSearch();
        }
        else {
            notification_is_toggled = false;
            $("#notification_box").slideUp(slide_animation_duration);
        }
    })
}

function options_toggler(){
    document.getElementById('profile_pic').addEventListener('click',e => {
        e.stopPropagation();
        if (!options_is_toggled){
            options_is_toggled = true;
            $("#options_box").slideDown(slide_animation_duration);
            if (notification_is_toggled){ // closing notification if toggled
                notification_is_toggled = false;
                $("#notification_box").slideUp(slide_animation_duration);
            }
            if (search_is_toggled)
                hideSearch();
        }
        else {
            options_is_toggled = false;
            $("#options_box").slideUp(slide_animation_duration);
        }
    })
}

function toggled_areas_closer(){ // closes the toggled windows when clicking elsewhere
    window.addEventListener('click', function(e){
        if (!document.getElementById('notification_box').contains(e.target)){
            if (notification_is_toggled){
                notification_is_toggled = false;
                $("#notification_box").slideUp(slide_animation_duration);
            }
        }
        if (!document.getElementById('options_box').contains(e.target)){
            if (options_is_toggled){
                options_is_toggled = false;
                $("#options_box").slideUp(slide_animation_duration);
            }
        }
        if (!document.getElementById('search_area').contains(e.target))
            if (search_is_toggled)
                hideSearch();
        // use else for clicks inside the box
    });
}

//////////////// NOTIFICATIONS STATE CHANGER ////////////////
function mark_notification_as_read(){
    document.querySelectorAll('.notification_id').forEach(elem => elem.addEventListener('click', function(e) {
        $.ajax({
            url:'/notification_state_changer_VIEW',
            type: "POST",
            data: {
                'notif_id': this.querySelector('div').innerHTML,
                'csrfmiddlewaretoken': getCookie('csrftoken'),
            },
            success:function(response){
                a = elem.parentElement;
                elem.parentElement.remove();
                if (!(document.querySelector('#notification_box div').children).length){ //if there are no more notification items
                    document.querySelector('#notification_box').innerHTML = '<span>Pas de Notification</span>';
                }   
            },
            complete:function(){},
            error:function (xhr, textStatus, thrownError){}
        });
    }))
}

//////////////// SEARCH BAR MANAGERS ////////////////
search_is_toggled = false;
suggestions_is_toggled = false;
search_animation_duration = 400;
show_leave_duration = 200;

function hideSearch(){
    search_is_toggled = false;
    $('#search_input')[0].value = ''; // emptying the search bar
    if (suggestions_is_toggled){
        suggestions_is_toggled = false;
        $("#search_suggestions").hide()
    }
    $('#leave_search_area').fadeOut(show_leave_duration);
    $('#search_area').animate({width:'2.6em','margin-left':'0'},search_animation_duration,'linear');
    $('#menu_entries').animate({'opacity':'1'},1000) //show menu entries
    $('#search_overlay').fadeOut(search_animation_duration);
}

function showSearch (){
    search_is_toggled = true;
    $('#search_area').animate({width:'95%','margin-left':'5%'},search_animation_duration,'swing');
    $('#leave_search_area').show(show_leave_duration);
    $('#search_input').focus();
    $('#menu_entries').animate({'opacity':'0'},100) //hide menu entries
    $('#search_overlay').fadeIn(search_animation_duration);
}

function search_bar_toggler() {
    // open search_area and search
    document.getElementById('search_button').addEventListener('click', e => {
        if (search_is_toggled){
            console.log("search this " + document.getElementById('search_input').value);
        }
        else
            showSearch();
            if (options_is_toggled){ // closing options if toggled
                options_is_toggled = false;
                $("#options_box").slideUp(slide_animation_duration);
            }
            if (notification_is_toggled){ // closing notification if toggled
                notification_is_toggled = false;
                $("#notification_box").slideUp(slide_animation_duration);
            }
    })

    // close search_area
    document.getElementById('leave_search_area').addEventListener('click', e => {
        if (search_is_toggled)
            hideSearch();
    })
    
}

function suggestions_filler(returned_data){
    var html_to_inject = ''
    if (returned_data.success){
        returned_data.users_data.forEach(user => {
            full_name = user.last_name
            html_to_inject +=`
            <div class='suggestion_item'>
                <div class='suggestion_item_id'>${user.id}</div>
                <img class='suggestion_item_img' src='${user.avatar}' >
                <div class='suggestion_item_info'>
                    <div class='suggestion_item_name'>${user.last_name.toLowerCase()} ${user.first_name.toLowerCase()}</div>
                    <div class='suggestion_item_filiere'>${user.level.toUpperCase()} - ${user.branch.toUpperCase()}</div>
                </div>
            </div>`
        })
        $('#search_suggestions').html(html_to_inject);
    }
    else {
        console.log('FAILURE')
        $('#search_suggestions').html("Hleoo");
    }
}

function search_bar_suggestions() {
    var typingTimer;  
    document.getElementById('search_input').addEventListener('input', function(e) {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(function(){
            if (search_is_toggled && $('#search_input')[0].value != ''){
                $.ajax({
                    url:'/search_suggestions_VIEW',
                    type: "POST",
                    data: {
                        'search_entry': this.value,
                        'csrfmiddlewaretoken': getCookie('csrftoken'),
                    },
                    success:function(response){
                        returned_data = JSON.parse(response)
                        suggestions_filler(returned_data)
                    },
                    complete:function(){},
                    error:function (xhr, textStatus, thrownError){}
                });
                suggestions_is_toggled = true;
                $("#search_suggestions").slideDown(slide_animation_duration)
            }
            else {
                suggestions_is_toggled = false;
                $("#search_suggestions").slideUp(slide_animation_duration)
            }
        }, 500);
    })
}

$( document ).ready(() => {
    /* notification and options toggling */
    notification_toggler();
    options_toggler();

    /* notification state changing */
    mark_notification_as_read();

    /* search bar management */
    search_bar_toggler();
    search_bar_suggestions();

    /* closing toggled area when clicking elsewhere */
    toggled_areas_closer();
})
