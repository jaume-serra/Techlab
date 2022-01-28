var ctx = document.getElementById("grafic-consum").getContext("2d");
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["10:00", "10:10", "10:20", "10:30", "10:40", "10:50", "11:00"],
    datasets: [{
      type: 'line',
      label: 'Màquina 1',
      data: [33,25,32,21,35,26,27],
      borderColor: "rgb(230, 44, 38)",
      backgroundColor:"rgb(230,44,38)",
      borderWidth: 2,
      fill: false,
    }, {
      type: 'line',
      label: 'Màquina 2',
      borderColor: "rgb(19, 43, 170)",
      backgroundColor: "rgb(19, 43, 170)",
      borderWidth: 2,
      fill: false,
      xAxisID: 'x-axis-2',
      data: [42,26,34,22,16,7,58]
    }]
  },

  options: {
      responsive: true,
      title: {
        display: true,
        text: 'Consum màquines actives'
      },
      tooltips: {
        mode: 'nearest',
        intersect: true,
      },
      scales: {
        xAxes: [{
          gridLines: {
            offsetGridLines: false,
          }
        }, {
          id: 'x-axis-2',
          type: 'linear',
          position: 'bottom',
          display: false,
          ticks: {
            min: 0,
            /*max: 958
            /*stepSize: 24*/
          }
        }],
        yAxes: [{
          ticks: {
            min: 0
            /*max: 950*/
          }
        }]
      }
    }
  });
