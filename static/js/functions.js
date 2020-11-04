//aggiunge automaticamente jquery
function get_jQuery(){
    var jQueryScript = document.createElement('script');
    jQueryScript.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js');
    document.head.appendChild(jQueryScript)
}

// ottiene articoli con chiamata rest
function getArticles(url){
    xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.send();
    xhr.onreadystatechange = function(){
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            response = JSON.parse(xhr.responseText);
            console.log(response);
            $.each(response, function(i){addCard(response[i])});
        }
    }
}

// mostra la carta di un articolo
function addCard(item){
    var src = "https://images-na.ssl-images-amazon.com/images/I/61dO6Tn1bKL._AC_SL1500_.jpg";
    var textNome = item["name"];
    var textMateriale = item["material"];
    var textDesc = item["description"];
    var textPrezzo = item["price"];
    var textStock = item["stock"];


    var myCard = $(`<div class=" card card-size"> 
                        <img class="card-img-top" src=${src}> 
                        <div class="card-body"> 
                            <h5 class="card-title">${textNome} - ${textMateriale}</h5> 
                            <p class="card-text">${textDesc}</p>
                            <p> Prezzo: ${textPrezzo} €</p>
                            <small>In Stock: ${textStock}</small> 
                            <button
                                style = "float: right;"
                                class="btn btn-primary" 
                                onclick = "addToCart(${parseInt(item['pk'])})">
                                Add To Cart 
                            </button>
                        </div>
                    </div>`);
    myCard.appendTo('#container-carte');
}

//mostra la carta di un OrderItem
function addItemCard(item, article){
    var src = "https://images-na.ssl-images-amazon.com/images/I/61dO6Tn1bKL._AC_SL1500_.jpg";
    var textNome = article['name'];
    var textPrezzo = article['price'];
    var amount = item['amount'];
    var item_id = item['id'];

    var myCard = $(`<div class=" card card-size"> 
                        <img class="card-img-top" src=${src}> 
                            <div class="card-body"> 
                                <h5 class="card-title">${textNome}</h5> 
                                <p class="card-text">
                                    <input class = "form-control-sm" type="number" style = "float:left;" 
                                    value="${amount}" min="1" max="9" step="1"
                                    onchange="amountChanged(${item_id},this.value)"/>
                                </p> 
                                <button class = "btn btn-danger" style = "float:right; margin:3px 0px;"
                                        onclick = 'removeItem(${item_id})'>Remove</button>
                                Single Price: ${textPrezzo} €
                            </div>
                        </div>`);
    myCard.appendTo('#container-carte');
}

//richiesta http per ottenere dati di un singolo articolo data la chiave primaria
//esegue la funzione callback una volta ricevuta la risposta
function get_article_detail(key, callback){
    var xhr = new XMLHttpRequest();

    xhr.open("GET", "http://127.0.0.1:8000/api/article-detail/" + key);
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



