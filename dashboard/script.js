Chart.defaults.color = '#a1a1aa';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.08)';

document.addEventListener('DOMContentLoaded', () => {
    if (typeof dssData !== 'undefined') {
        initDashboard(dssData);
        initScrollSpy();
    } else {
        document.body.innerHTML = `<h2 style="color:red; text-align:center; padding: 2rem; margin-top:100px;">Error: dssData is undefined. Run dss_exporter.py first.</h2>`;
    }
});

function initScrollSpy() {
    const sections = document.querySelectorAll('.scroll-section');
    const navLinks = document.querySelectorAll('.nav-links a');

    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            // Adjustment for sticky navbar height
            if (scrollY >= (sectionTop - 150)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

function initDashboard(data) {
    document.getElementById('yearDisplay').textContent = data.metadata.latest_year;
    
    // KPIs
    document.getElementById('kpiRegions').textContent = data.metadata.total_regions;
    
    const bestModel = data.model_performance[0];
    document.getElementById('kpiModelR2').textContent = (bestModel.R2 * 100).toFixed(2) + '%';
    
    const highRiskCount = data.top_vulnerable.filter(r => r.rvi_score > 0.6).length;
    document.getElementById('kpiHighRisk').textContent = highRiskCount;
    
    renderLists(data.top_vulnerable, 'vulnerableList', 'high-risk');
    renderLists(data.safest, 'safestList', 'safe');
    
    renderRecommendations(data.recommendations);
    
    renderModelChart(data.model_performance);
    renderRadarChart(data.top_vulnerable, data.safest);
    renderDoughnutChart(data.top_vulnerable, data.safest, data.metadata.total_regions);
}

function renderLists(regions, elementId, cssClass) {
    const list = document.getElementById(elementId);
    list.innerHTML = '';
    
    regions.forEach((region, index) => {
        const li = document.createElement('li');
        li.className = cssClass;
        li.innerHTML = `
            <span class="list-rank">#${index + 1}</span>
            <span class="list-name">${region.kabupaten}</span>
            <span class="score-badge">${region.rvi_score.toFixed(3)}</span>
        `;
        list.appendChild(li);
    });
}

function renderRecommendations(recs) {
    const tbody = document.getElementById('recTableBody');
    tbody.innerHTML = '';
    
    recs.forEach(rec => {
        const tr = document.createElement('tr');
        const badgeColor = rec.risk_level === 'High' ? 'var(--danger)' : 'var(--warning)';
        
        tr.innerHTML = `
            <td><strong>${rec.kabupaten}</strong></td>
            <td>${rec.rvi_score}</td>
            <td><span style="color: ${badgeColor}; font-weight: bold;">${rec.risk_level}</span></td>
            <td>${rec.recommendation}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderModelChart(models) {
    const ctx = document.getElementById('modelChart').getContext('2d');
    
    const labels = models.map(m => m.Model);
    const r2Data = models.map(m => m.R2);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Skor R² (Semakin tinggi semakin baik)',
                data: r2Data,
                backgroundColor: 'rgba(59, 130, 246, 0.7)',
                borderColor: '#3b82f6',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { min: 0, max: 1 }
            }
        }
    });
}

function calcAvg(arr, prop) {
    const sum = arr.reduce((a, b) => a + (b[prop] || 0), 0);
    return sum / arr.length;
}

function renderRadarChart(topVuln, topSafe) {
    const ctx = document.getElementById('radarChart').getContext('2d');
    
    // Averages for vulnerable
    const vulnAvg = [
        calcAvg(topVuln, 'env_risk_index'),
        calcAvg(topVuln, 'socio_vuln_index'),
        calcAvg(topVuln, 'health_risk_score')
    ];
    
    // Averages for safe
    const safeAvg = [
        calcAvg(topSafe, 'env_risk_index'),
        calcAvg(topSafe, 'socio_vuln_index'),
        calcAvg(topSafe, 'health_risk_score')
    ];

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Risiko Lingkungan', 'Kerentanan Sosio-Ekonomi', 'Risiko Kesehatan & Sanitasi'],
            datasets: [
                {
                    label: 'Top 10 Paling Rentan',
                    data: vulnAvg,
                    backgroundColor: 'rgba(239, 68, 68, 0.2)',
                    borderColor: '#ef4444',
                    pointBackgroundColor: '#ef4444',
                    borderWidth: 2
                },
                {
                    label: 'Top 10 Paling Tangguh',
                    data: safeAvg,
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    borderColor: '#10b981',
                    pointBackgroundColor: '#10b981',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    angleLines: { color: 'rgba(255,255,255,0.1)' },
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    pointLabels: { font: { size: 12 }, color: '#f8fafc' },
                    ticks: { display: false, min: 0, max: 1 }
                }
            }
        }
    });
}

function renderDoughnutChart(topVuln, topSafe, totalRegions) {
    const ctx = document.getElementById('doughnutChart').getContext('2d');
    
    const highRisk = topVuln.filter(r => r.rvi_score > 0.6).length;
    const lowRisk = topSafe.filter(r => r.rvi_score < 0.4).length;
    const medRisk = totalRegions - highRisk - lowRisk;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Risiko Tinggi (>0.6)', 'Risiko Menengah (0.4-0.6)', 'Risiko Rendah (<0.4)'],
            datasets: [{
                data: [highRisk, medRisk, lowRisk],
                backgroundColor: [
                    '#ef4444', 
                    '#f59e0b', 
                    '#10b981'
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            cutout: '70%',
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}
