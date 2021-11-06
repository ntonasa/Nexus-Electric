function loadXMLDoc(xmlfile, xslfile, renderdivid, eventually=null, data=null) {
    Promise.all([getXMLresponse(xmlfile), getXMLresponse(xslfile)])
    .then(values => {
        if (window.ActiveXObject || xhttp.responseType == "msxml-document") {
            ex = values[0].transformNode(values[1]);
            document.getElementById(renderdivid).innerHTML = ex;
        }
        else if (document.implementation && document.implementation.createDocument) {
            xsltProcessor = new XSLTProcessor();
            xsltProcessor.importStylesheet(values[1]);
            resultDocument = xsltProcessor.transformToFragment(values[0], document);
            document.getElementById(renderdivid).appendChild(resultDocument);
        }
        if (eventually) {
            eventually(data);
        }
    })
    .catch(err => {
        return;
    })
}

function getXMLresponse(filename) {
    if (window.ActiveXObject) {
        xhttp = new ActiveXObject("Msxml2.XMLHTTP");
    }
    else {
        xhttp = new XMLHttpRequest();
    }
    xhttp.open("GET", filename, true);
    xhttp.send();

    return new Promise((resolve, reject) => {
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200 && this.responseXML != null) {
                    resolve(this.responseXML);
                }
                else {
                    reject("Unsuccessful Request Status");
                }
            }
        }
    })
}

function _async_http_request(method, url) {
    try {
        if (window.ActiveXObject) {
            xhttp = new ActiveXObject("Msxml2.XMLHTTP");
        }
        else {
            xhttp = new XMLHttpRequest();
        }
        xhttp.open(method, url, true);
        xhttp.send();

        return new Promise((resolve, reject) => {
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4) {
                    resolve(this);
                }
            }
        })
    } catch (err) {
        return new Promise((resolve, reject) => {
            reject(err);
        })
    }
}

function check_window_status(trigger, event) {
    event.preventDefault();
    var win = window.open('', trigger.attributes.target.nodeValue);
    if (win.closed) {
        win = window.open(trigger.attributes.href.nodeValue, trigger.attributes.target.nodeValue);
    }
    else if (win.location.href == 'about:blank') {
        win.location.href = trigger.attributes.href.nodeValue;
    }
    win.focus();
}

function parse_cookies() {
    var cookiestr = decodeURIComponent(document.cookie);
    var cookiearr = cookiestr.split(';');
    var cookiedict = {};
    for (keyval in cookiearr) {
        key_val_arr = cookiearr[keyval].split('=');
        cookiedict[key_val_arr[0]] = key_val_arr[1];
    }
    return cookiedict
}

String.prototype.format = function() {
    the_string = this;
    for (k in arguments) {
        the_string = the_string.replace("{" + k + "}", arguments[k])
    }
    return the_string
}

BASE_URL = 'http://127.0.0.1:8888/energy/api/{0}?format=json';

// function get_access_token() {
//     xhttp = new XMLHttpRequest();
//     xhttp.open('POST', BASE_URL.format("Login"), true);
//     xhttp.send({
//         'username' : $('#username').val(),
//         'password' : $('#password').val()
//     })

//     promise = new Promise((resolve, reject) => {
//         xhttp.onreadystatechange = function() {
//             if (this.readyState == 4) {
//                 alert(this.response)
//                 resolve()
//             }
//         }
//     })
// }

function get_access_token() {
    $.ajax({
        url: BASE_URL.format("Login"),
        method: 'POST',
        data: {
            'username' : $('#username').val(),
            'password' : $('#password').val()
        }
    }).done(function(data) {
        alert(data)
        alert(JSON.parse(data))
    })
}