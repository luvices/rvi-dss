// Configuration for Chart.js text color
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Inter', sans-serif";

document.addEventListener('DOMContentLoaded', () => {
    if (typeof dashboardData !== 'undefined') {
        renderKPIs(dashboardData.metrics);
        renderTrendChart(dashboardData.trends);
        renderImportanceChart(dashboardData.feature_importance);
        renderTable(dashboardData.raw_data);
    } else {
        document.getElementById('kpi-container').innerHTML = `<p style="color:red">Error: dashboardData is undefined. Ensure process_data.py has been run.</p>`;
    }
});

function renderKPIs(metrics) {
    const container = document.getElementById('kpi-container');
    container.innerHTML = `
        <div class="glass-panel kpi-card">
            <h3>Wilayah Dianalisis</h3>
            <div class="value">${metrics.total_regions}</div>
        </div>
        <div class="glass-panel kpi-card">
            <h3>Total Data Points</h3>
            <div class="value">${metrics.total_records}</div>
        </div>
        <div class="glass-panel kpi-card">
            <h3>Akurasi Model (R²)</h3>
            <div class="value">${(metrics.model_r2 * 100).toFixed(1)}%</div>
        </div>
    `;
}

function renderTrendChart(trends) {
    const ctx = document.getElementById('trendChart').getContext('2d');
    
    // Create datasets dynamically based on regions
    const colors = ['#06b6d4', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444'];
    let idx = 0;
    
    const datasets = Object.keys(trends.data).map(region => {
        const color = colors[idx % colors.length];
        idx++;
        return {
            label: region,
            data: trends.data[region],
            borderColor: color,
            backgroundColor: color + '33', // 20% opacity
            borderWidth: 2,
            tension: 0.4,
            fill: true
        };
    });

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: trends.years,
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: 'rgba(255,255,255,0.05)' }
                },
                x: {
                    grid: { color: 'rgba(255,255,255,0.05)' }
                }
            }
        }
    });
}

function renderImportanceChart(importance) {
    const ctx = document.getElementById('importanceChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: importance.labels.map(l => l.toUpperCase().replace('_', ' ')),
            datasets: [{
                label: 'Importance Score',
                data: importance.values,
                backgroundColor: [
                    '#06b6d4', '#0ea5e9', '#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#d946ef'
                ],
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y', // Horizontal bar chart
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.05)' }
                },
                y: {
                    grid: { display: false }
                }
            }
        }
    });
}

function renderTable(rawData) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';
    
    rawData.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.kabupaten}</td>
            <td>${row.tahun}</td>
            <td>${row.produksi_padi.toLocaleString()}</td>
            <td>${row.curah_hujan ? row.curah_hujan.toLocaleString() : '-'}</td>
            <td>${row.suhu ? row.suhu : '-'}</td>
            <td>${row.ipm ? row.ipm : '-'}</td>
            <td>${row.kemiskinan ? row.kemiskinan : '-'}</td>
        `;
        tbody.appendChild(tr);
    });
}
