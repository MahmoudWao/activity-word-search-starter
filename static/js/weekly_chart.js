// Weekly Summary Chart Functions
let radarChart = null;

async function initializeWeeklySummary() {
    try {
        const summaries = await fetchWeeklySummaries();
        const selector = document.getElementById('week-selector');

        if (!selector) return;

        selector.innerHTML = '';

        if (summaries.length === 0) {
            selector.innerHTML = '<option>No weeks available yet</option>';
            clearChartAndStats();
            return;
        }

        // Add summaries to selector (newest first)
        summaries.forEach((summary, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `Week of ${formatWeekEndDate(summary.week_ending)}`;
            selector.appendChild(option);
        });

        // Display the first (most recent) summary
        selector.addEventListener('change', function() {
            const index = parseInt(this.value);
            displayWeeklySummary(summaries[index]);
        });

        // Display initial summary
        displayWeeklySummary(summaries[0]);
    } catch (error) {
        console.error('Error initializing weekly summary:', error);
    }
}

function formatWeekEndDate(dateString) {
    const date = new Date(dateString + 'T00:00:00');
    const options = { weekday: 'long', month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

function displayWeeklySummary(summary) {
    if (!summary) return;

    // Display stats
    displayWeeklyStats(summary);

    // Create/update radar chart
    updateRadarChart(summary);
}

function displayWeeklyStats(summary) {
    const statsDiv = document.getElementById('weekly-stats');
    if (!statsDiv) return;

    statsDiv.innerHTML = `
        <div class="stat-row">
            <div class="stat-item">
                <div class="stat-label">Mental Resilience</div>
                <div class="stat-value">${summary.mental_resilience_avg.toFixed(1)}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Physical Energy</div>
                <div class="stat-value">${summary.physical_energy_avg.toFixed(1)}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Emotional Balance</div>
                <div class="stat-value">${summary.emotional_balance_avg.toFixed(1)}</div>
            </div>
        </div>
        <div class="stat-row">
            <div class="stat-item">
                <div class="stat-label">Low Stress</div>
                <div class="stat-value">${summary.stress_level_avg.toFixed(1)}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Productivity</div>
                <div class="stat-value">${summary.productivity_avg.toFixed(1)}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Week Type</div>
                <div class="stat-value">${summary.week_type}</div>
            </div>
        </div>
    `;
}

function updateRadarChart(summary) {
    const ctx = document.getElementById('radarChart');
    if (!ctx) return;

    const data = {
        labels: [
            'Mental Resilience',
            'Physical Energy',
            'Emotional Balance',
            'Low Stress',
            'Productivity'
        ],
        datasets: [
            {
                label: `Week of ${formatWeekEndDate(summary.week_ending)}`,
                data: [
                    summary.mental_resilience_avg,
                    summary.physical_energy_avg,
                    summary.emotional_balance_avg,
                    summary.stress_level_avg,
                    summary.productivity_avg
                ],
                borderColor: '#00d4ff',
                backgroundColor: 'rgba(0, 212, 255, 0.15)',
                pointBackgroundColor: '#00d4ff',
                pointBorderColor: '#e0e0e0',
                pointRadius: 5,
                pointHoverRadius: 7,
                borderWidth: 2,
                tension: 0.1
            }
        ]
    };

    const options = {
        scales: {
            r: {
                beginAtZero: true,
                min: 1,
                max: 10,
                ticks: {
                    stepSize: 1,
                    callback: function(value) {
                        return value;
                    }
                },
                grid: {
                    color: '#404040',
                    drawBorder: true
                },
                angleLines: {
                    color: '#404040'
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    color: '#e0e0e0',
                    font: {
                        size: 12
                    }
                }
            },
            filler: {
                propagate: true
            }
        },
        responsive: true,
        maintainAspectRatio: true,
        animation: {
            duration: 300
        }
    };

    // Destroy existing chart if it exists
    if (radarChart) {
        radarChart.destroy();
    }

    // Create new chart
    radarChart = new Chart(ctx, {
        type: 'radar',
        data: data,
        options: options
    });
}

function clearChartAndStats() {
    const statsDiv = document.getElementById('weekly-stats');
    if (statsDiv) {
        statsDiv.innerHTML = '<p style="text-align: center; color: #b0b0b0;">No data available yet. Add daily entries to see weekly summaries.</p>';
    }

    const ctx = document.getElementById('radarChart');
    if (ctx && radarChart) {
        radarChart.destroy();
        radarChart = null;
    }
}

// Initialize on page load if weekly summary tab is active
document.addEventListener('DOMContentLoaded', function() {
    const weeklySummaryTab = document.getElementById('weekly-summary');
    if (weeklySummaryTab && weeklySummaryTab.classList.contains('active')) {
        initializeWeeklySummary();
    }
});
