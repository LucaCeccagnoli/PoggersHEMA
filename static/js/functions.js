//aggiunge automaticamente jquery
function get_jQuery(){
    var jQueryScript = document.createElement('script');
    jQueryScript.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js');
    document.head.appendChild(jQueryScript)
}

// ottiene articoli con chiamata rest
// params specifica parametri da appendere all'url della richiesta, per filtrare gli articoli
// element specifica l'elemento dopo cui stampare i risultati
function get_articles(params, element){
    var xhr = new XMLHttpRequest();

    xhr.open("GET", "http://127.0.0.1:8000/api/articles/" + params);
    xhr.onreadystatechange = function(){
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            response = xhr.responseText;
            response = JSON.parse(response)
            console.log(response)

            //sostituire con il codice per disegnare le carte
            for(var article in response){
                var li = document.createElement('li');

                //elementi del json
                for(var key in response[article]){
                    console.log(response[article]);
                    var textNode = document.createTextNode(response[article][key]);
                    
                    li.appendChild(textNode);
                }
                element.appendChild(li)
            }
        }
    }
    xhr.send();
}

//richiesta http per ottenere dati di un singolo articolo data la chiave primaria
//esegue la funzione callback una volta ricevuta la risposta
function get_article_detail(key, callback){
    var xhr = new XMLHttpRequest();

    xhr.open("GET", "http://127.0.0.1:8000/api/articles/" + key);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();

    xhr.onreadystatechange = function(){
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            var response = xhr.responseText;
            response = JSON.parse(response);
            callback(response);
        }
    }
}

// richiesta http all'api che controlla l'utente loggato
// ritorna l'username dell'utente loggato, o una stringa vuota se il login non è stato effettuato
function get_logged_user(callback){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", 'http://127.0.0.1:8000/api/get-logged-user/');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();

    xhr.onreadystatechange = function(){
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            var response = xhr.responseText;
            response = JSON.parse(response);

            callback(response);
        }
    }
}

// funzioni per i cookie
function set_cookie(key, value, minutes){
    //cerca il cookie
    var d = new Date();
    d.setTime(d.getTime() + minutes * 60 * 1000);   // 1000 millisecondi * 60 secondi = 1 minuto
    var expires = "expires="+d.toUTCString();
    document.cookie = key + "=" + value + ";" + expires + ";path=/" ;
}

function get_cookie(key){
    cookie = ""
    name = key + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length ; i++){
        var c = ca[i];
        while( c.charAt(0) == ' '){
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0){
            cookie = c.substring(name.length, c.length);
        }
    }
    return cookie;
}
