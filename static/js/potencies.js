let grafica;
var colors = [];
let time = 0;

function getRandomColor() {
  var letters = '0123456789ABCDEF'.split('');
  var color = '#';
  for (var i = 0; i < 6; i++ ) {
      color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}


function actualitzaGrafica(msg){

  var ctx = document.getElementById("potencies-maquines");

  if (grafica) {
    grafica.destroy();
  }

  var length_maq = msg["noms"].length;
  var length_color = colors.length;
  var substract = length_maq - length_color;


  if (length_color < length_maq){
    for (var j=0; j< substract; j++){
      colors.push(getRandomColor());
    }
  }


  var datasets_prova = [];
  for (var i=0; i<msg["noms"].length; i++){
    var maquina = msg["noms"][i];
    datasets_prova.push({
      label: msg["noms"][i],
      fill: false,
      backgroundColor: colors[i],
      borderColor: colors[i],
      lineTension: 0.1,
      pointHoverBorderWidth: 2,
      pointRadius: 4,
      pointHitRadius: 10,
      data: msg[maquina],
    });
  }  



  var data = {
    labels: msg["hores"],
    datasets: datasets_prova
  };

  var options = {
    scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]            
          }  
  };
  
  grafica = new Chart(ctx, {
    type: 'line',
    data: data,
    options: options
  });
}


function updatePotencies(){

    var request,msg;

    if (time == 0){
      request = new XMLHttpRequest();
      request.onreadystatechange = function() {
        if (request.readyState==4 && request.status==200) {
          msg = JSON.parse(request.responseText);
          actualitzaGrafica(msg);
        }
      }
      request.open("GET","/api/potencies/maquines",true);
      request.send();
      time +=1;
    }
    else if (time==5){
      time = 0;
    }
    else{
      time +=1;
    }
   
}
