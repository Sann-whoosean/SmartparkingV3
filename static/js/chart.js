// charts.js
function renderBarChart(canvasId, labels, data, title = 'Bar Chart') {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Jumlah Transaksi',
                data: data,
                backgroundColor: 'rgba(54, 162, 235, 0.7)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
                title: { display: true, text: title }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function renderPieChart(canvasId, labels, data, title = 'Pie Chart') {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56', '#8A2BE2', '#FFA500']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                title: { display: true, text: title }
            }
        }
    });
}
