var grafica = 0;
let myChart1;
let boto = "OFF";
let FlagReserva;
var carrega = 0;

function actualitzaEstat(){
    var request;
    var aforament;
    var msg;

    aforament = document.getElementById("aforament");
    request = new XMLHttpRequest();
    request.onreadystatechange = function() {
      if (request.readyState==4 && request.status==200) {
	      msg = JSON.parse(request.responseText);
          aforament.value = msg["Missatge"]+"%";
      }
    }
    request.open("GET","/api/aforament",true);
    request.send();
}

function consultaValor(maquina){
  var request;
  var msg;
  var url = "/api/hist/maquina/" + maquina + "/last/15";

  request=new XMLHttpRequest();
  request.onreadystatechange=function() {
    if (request.readyState==4 && request.status==200) {
	     msg = JSON.parse(request.responseText);
	     consumMaquina(msg);
    }
  }
  request.open("GET", url, true);
  request.send();
}

function consumMaquina(msg){
  //console.log(msg);

  var testData = {
      "type": "line",
      "data": {
          "labels": msg["hores"],
          "datasets": [{
                                   "label": "Potència (W)",
              "data": msg["valors"],
                                   "fill": false, //color de fons
                                   "borderColor": "#8fc04e",
                                   "lineTension": 0.1 // perque es noti una mica la corba
          }]
      },
      "options": {
          scales: {
              yAxes: [{
                  ticks: {
                      min: 0
                  }
              }]
          }
      }
  };

var ctx = $("#consum-maquina1").get(0).getContext("2d");

if (myChart1) {
    myChart1.destroy();
}

myChart1 = new Chart(ctx, {
        type: 'line',
        data: testData.data,
        options: testData.options
    });
}


let estat ="off";

function canviaBoto(maquina){
  if (estat =="off"){
    document.getElementById("boto-off").style.display = 'none';
    document.getElementById("boto-on").style.display='block';
    estat = "on";
    canviaValorActuador("on", maquina);
    document.getElementById("colorMaquina").style.color = 'green';
  } else if (estat == "on") {
    document.getElementById("boto-off").style.display = 'block';
    document.getElementById("boto-on").style.display='none';
    estat = "off";
    canviaValorActuador("off", maquina);
    document.getElementById("colorMaquina").style.color = 'red';
  } else {
    console.log("Emergencia");
  }
}

function actualitzaEstat(maquina) {
  var request;
  var msg;
  var url = "/api/maquina/" + maquina + "/estat"

  request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (request.readyState==4 && request.status==200) {
      msg = JSON.parse(request.responseText);
      update_estat(msg);
    }
  }
  request.open("GET", url, true);
  request.send();
}


function update_estat(msg){

  if (msg["estat"] == "ON") {
    estat = "on";
    document.getElementById("colorMaquina").style.color = 'green';
    document.getElementById("boto-off").style.display = 'none';
    document.getElementById("boto-on").style.display='block';
    document.getElementById("botoEmergencia").style.color = '#808080';
    document.getElementById("botoEmergencia").style.opacity = '0.7';
  }
  else if (msg["estat"] == "OFF") {
    document.getElementById("colorMaquina").style.color = 'red';
    document.getElementById("boto-off").style.display = 'block';
    document.getElementById("boto-on").style.display='none';
    document.getElementById("botoEmergencia").style.color = '#808080';
    document.getElementById("botoEmergencia").style.opacity = '0.7';
    estat = "off";
  }
  else {
    estat = "emergencia";
    document.getElementById("boto-on").style.display='none';
    document.getElementById("botoEmergencia").style.color = 'orange';
    document.getElementById("botoEmergencia").style.opacity = '1';
  }
}


function canviaValorActuador(value, maquina){
    var request;
    var msg;
    var url = "/api/maquina/" + maquina + "/estat/" + value;

    request = new XMLHttpRequest();
    request.onreadystatechange = function() {
      if (request.readyState==4 && request.status==200) {
	      msg = JSON.parse(request.responseText);
        if (msg["msg"] == "ok") {
        }
      }
    }
    request.open("PUT", url, true);
    request.send();
}


function finalitzaReserva(id){
  var request;
    var msg;
    var url = "/nfc-out/maquina/" + id;

    request = new XMLHttpRequest();
    request.onreadystatechange = function() {
      if (request.readyState==4 && request.status==200) {
	      msg = JSON.parse(request.responseText);
      }
    }
    request.open("PUT", url, true);
    request.send();
}


function checkReserva(maquina){
    var request;
    var msg;
    var url = "/api/reserves/maquina/" + maquina;

    request = new XMLHttpRequest();
    request.onreadystatechange = function() {
      if (request.readyState==4 && request.status==200) {
	      msg = JSON.parse(request.responseText);

        if (msg["msg"] == "nextReserva") {
          document.getElementById("usuari-reserva").innerHTML = " " + msg["usr"];
          FlagReserva = "ON";
        } else {
          document.getElementById("usuari-reserva").innerHTML = " No hi ha reserva";
          FlagReserva = "OFF";
        }

      }
    }
    request.open("GET", url, true);
    request.send();
}

function checkWifi(maquina){
  var request;
  var msg;
  var url = "/api/wifi/maquina/" + maquina;

  request = new XMLHttpRequest();
    request.onreadystatechange = function() {
      if (request.readyState==4 && request.status==200) {
	      msg = JSON.parse(request.responseText);

        document.getElementById("ssid-wifi").innerHTML = " " + msg["msg"];

      }
    }
    request.open("GET", url, true);
    request.send();
}

function changeWifiParam(maquina){
  var request;
  var msg;
  var ssid;
  var pswd;

  ssid = document.getElementById("nouSsidWifi").value;
  pswd = document.getElementById("nouPswdWifi").value;
  var url = "/api/maquina/" + maquina + "/" + ssid + "/" + pswd;

  request = new XMLHttpRequest();
    request.onreadystatechange = function() {
      if (request.readyState==4 && request.status==200) {
	      msg = JSON.parse(request.responseText);

        document.getElementById("nouSsidWifi").value=" ";
        document.getElementById("nouPswdWifi").value=" ";

      }
    }
    request.open("PUT", url, true);
    request.send();
}
