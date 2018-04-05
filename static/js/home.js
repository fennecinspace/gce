/////////////////// HOME MENU /////////////////////
function home_menu_manager() {
    ///// later replace alerts with load (' view url ') for each view 
    user_type = $("#logged_in_user_id").html().substring(0, 4);
    
    if (user_type == 'tech') {
        document.getElementById("televerser_icon").addEventListener('click', () => {
            alert('upload')
        })

        document.getElementById("saisir_icon").addEventListener('click', () => {
            alert('marks')
        })
    }
    else {
        document.getElementById("annonces_icon").addEventListener('click', () => {
            alert('news')
        })

        document.getElementById("messenger_icon").addEventListener('click', () => {
            alert('messenger')
        })
    }

    if (user_type == 'ensg' || user_type == 'etud') {
        document.getElementById("resultats_icon").addEventListener('click', () => {
            alert('results')
        })
    }

    if (user_type == 'ensg') {
        document.getElementById("reclamations_icon").addEventListener('click', () => {
            alert('error')
        })
    }

    if (user_type == 'ensg' || user_type == 'chef') {
        document.getElementById("consultations_icon").addEventListener('click', () => {
            alert('consult')
        })
    }

    if (user_type == 'chef') {
        document.getElementById("utilisateur_icon").addEventListener('click', () => {
            alert('users')
        })

        document.getElementById("affichages_icon").addEventListener('click', () => {
            alert('billboard')
        })
    }
}



//////////////// FUNCTIONS CALLING ////////////////

$(document).ready(() => {
    home_menu_manager();
})