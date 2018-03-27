

# Pour utiliser livereload (browser-sync alternative)


## Installation :
installer des modules dans la machine host

    pip install --upgrade pip
    pip install django-livereload-server
    pip install psycopg2

clonner le repo

    git clone git@gitlab.com:pfe-l3/gce.git

faire un build  

    cd ToGceProjectFolder/
    docker-compose build

## Utilisation:
utilisé 2 Console(Terminal) pour lancé 2 serveurs au meme temps:<br>
- 1er :

        cd ToGceProjectFolder/
        python manage.py livereload

- 2eme :  (apres que le 1er server se lance) (dans un autre teminal)

        cd ToGceProjectFolder/
        docker-compose up

laisse les 2 serveurs en marche, et chaque fois que tu sauvgarde un docment css, js, ou html, la page recharge automatiquement