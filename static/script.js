const labels = categoryData.map(item => item[0]);
const values = categoryData.map(item => item[1]);

const ctx = document.getElementById("expenseChart");

new Chart(ctx, {
    type: "doughnut",
    data: {
        labels: labels,
        datasets: [{
            data: values,
            backgroundColor: [
                "#4e54c8",
                "#8f94fb",
                "#ff6b6b",
                "#feca57",
                "#1dd1a1"
            ]
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: "bottom"
            }
        }
    }
});