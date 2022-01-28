const $grafica = document.querySelector("#consumMachine");
const etiquetes = ["Genere", "Febrer", "Març", "Abril"]

const consumMitja = {
    label: "Consum mitjà (mA)",
    data: [1, 4, 3, 0.5],
    backgroundColor: 'rgba(54, 162, 235, 0.2)',
    borderColor: 'rgba(54, 162, 235, 1)',
    borderWidth: 1,
};

const reserves = {
    label: "Reserves",
    data: [1, 30, 3, 5],
    backgroundColor: 'rgba(255, 159, 64, 0.2)',
    borderColor: 'rgba(255, 159, 64, 1)',
    borderWidth: 1,
};


new Chart($grafica, {
    type: 'bar',
    data: {
        labels: etiquetes,
        datasets: [
            consumMitja,
            reserves
        ]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }],
        },
    }
});
