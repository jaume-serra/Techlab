let myChart;
var aforament = 0;

function graficaCircular(msg){
  var max_aforament = msg[0];
  var aforament = msg[1]
  var ctx = document.getElementById("aforament-nou");
  //ctx.fillText("30" + "%", width/2 - 20, width/2, 200);

  if (myChart) {
    myChart.destroy();
}

  myChart = new Chart(ctx, {
    type: 'doughnut',
    data:{
	    datasets: [{
		    data: [aforament,max_aforament-aforament],
		    backgroundColor: ['#8fc04e',"#e9e9e9"],
		    label: ''}],
		    labels: ['Ocupats',"Disponibles"]},
        options: {responsive: true}
});
}

function consultaAforament(){
    var request;
    var aforament;
    var msg;

    aforament = document.getElementById("aforament");
    request = new XMLHttpRequest();
    request.onreadystatechange = function() {
      if (request.readyState==4 && request.status==200) {
	      msg = JSON.parse(request.responseText);
        graficaCircular(msg["Missatge"]);
        //aforament.value = msg["Missatge"]+"%";
      }
    }
    request.open("GET","/api/aforament",true);
    request.send();
}


function consultaEstatMaquines(){
  var request;
  var msg;
  var url = "/api/maquines/estat";

  request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (request.readyState==4 && request.status==200) {
      msg = JSON.parse(request.responseText);

      for (var i = 0; i <= msg["maquines"].lenght(); i++) {
        canviaEstat(msg,msg[i],msg[i][1]);
      }

    }
  }
  request.open("GET", url, true);
  request.send();
  if (aforament == 5){
    consultaAforament();
    aforament = 0;
  }
  aforament +=1;
  
}

function canviaEstat(msg, key,i) {
  if (msg[key][0] == "ON"){
    document.getElementById(i).style.color = 'green';
  } 
  else if (msg[key][0] == "OFF") {
    document.getElementById(i).style.color = 'red';
  } 
  else {
    document.getElementById(i).style.color = 'orange';
  }
}
