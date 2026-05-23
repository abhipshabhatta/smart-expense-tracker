const labels = categoryData.map(item => item[0]);

const amounts = categoryData.map(item => item[1]);

const ctx = document.getElementById("expenseChart");

new Chart(ctx, {
    type: "pie",

    data: {
        labels: labels,

        datasets: [
            {
                label: "Expenses",

                data: amounts
            }
        ]
    },

    options: {
        responsive: true
    }
});