// Daily Log Functions
document.addEventListener('DOMContentLoaded', function() {
    loadDailyLog();

    // Form submission
    const form = document.getElementById('daily-form');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            await submitDailyEntry();
        });
    }

    // Load daily log when daily-log tab is clicked
    const dailyLogTab = document.querySelector('[data-tab="daily-log"]');
    if (dailyLogTab) {
        dailyLogTab.addEventListener('click', loadDailyLog);
    }
});

async function loadDailyLog() {
    try {
        const entries = await fetchDailyLog();
        displayDailyLog(entries);
    } catch (error) {
        console.error('Error loading daily log:', error);
    }
}

function displayDailyLog(entries) {
    const tbody = document.getElementById('daily-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (entries.length === 0) {
        tbody.innerHTML = '<tr><td colspan="12" style="text-align: center; padding: 20px; color: #b0b0b0;">No entries yet. Add your first entry above!</td></tr>';
        return;
    }

    // Sort entries by date (newest first)
    entries.sort((a, b) => new Date(b.date) - new Date(a.date));

    entries.forEach(entry => {
        const row = document.createElement('tr');

        // Determine if this is today
        const isToday = entry.date === formatDate(new Date());
        if (isToday) {
            row.style.backgroundColor = 'rgba(0, 212, 255, 0.1)';
        }

        row.innerHTML = `
            <td>${formatDateDisplay(entry.date)}</td>
            <td>${entry.week_type}</td>
            <td class="score-col">${getHeatmapCell(entry.mental_resilience, 'mental_resilience')}</td>
            <td class="score-col">${getHeatmapCell(entry.physical_energy, 'physical_energy')}</td>
            <td class="score-col">${getHeatmapCell(entry.emotional_balance, 'emotional_balance')}</td>
            <td class="score-col">${getHeatmapCell(entry.stress_level, 'stress_level')}</td>
            <td class="score-col">${getHeatmapCell(entry.productivity, 'productivity')}</td>
            <td>${entry.running_avg_mental ? entry.running_avg_mental.toFixed(1) : '-'}</td>
            <td>${entry.running_avg_physical ? entry.running_avg_physical.toFixed(1) : '-'}</td>
            <td>${entry.running_avg_emotional ? entry.running_avg_emotional.toFixed(1) : '-'}</td>
            <td>${entry.running_avg_stress ? entry.running_avg_stress.toFixed(1) : '-'}</td>
            <td>${entry.running_avg_productivity ? entry.running_avg_productivity.toFixed(1) : '-'}</td>
        `;

        tbody.appendChild(row);
    });
}

function getHeatmapCell(score, attribute) {
    let color = 'red';
    if (score >= 7) {
        color = 'green';
    } else if (score >= 4) {
        color = 'amber';
    }

    return `<span class="heatmap-cell ${color}">${score}</span>`;
}

function formatDateDisplay(dateString) {
    const date = new Date(dateString + 'T00:00:00');
    const options = { month: 'short', day: 'numeric', year: '2-digit' };
    return date.toLocaleDateString('en-US', options);
}

async function submitDailyEntry() {
    try {
        const date = document.getElementById('date').value;
        const weekType = document.getElementById('week-type').value;
        const mentalResilience = parseInt(document.getElementById('mental').value);
        const physicalEnergy = parseInt(document.getElementById('physical').value);
        const emotionalBalance = parseInt(document.getElementById('emotional').value);
        const stressLevel = parseInt(document.getElementById('stress').value);
        const productivity = parseInt(document.getElementById('productivity').value);

        // Validate
        if (!date) {
            showMessage('Please select a date', 'error');
            return;
        }

        if (mentalResilience < 1 || mentalResilience > 10 ||
            physicalEnergy < 1 || physicalEnergy > 10 ||
            emotionalBalance < 1 || emotionalBalance > 10 ||
            stressLevel < 1 || stressLevel > 10 ||
            productivity < 1 || productivity > 10) {
            showMessage('All scores must be between 1 and 10', 'error');
            return;
        }

        const data = {
            date: date,
            week_type: weekType,
            mental_resilience: mentalResilience,
            physical_energy: physicalEnergy,
            emotional_balance: emotionalBalance,
            stress_level: stressLevel,
            productivity: productivity
        };

        const result = await apiCall('/api/daily-log', 'POST', data);

        if (result.success) {
            showMessage('Entry saved successfully!', 'success');

            // Reset form
            document.getElementById('daily-form').reset();
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('date').value = today;

            // Reload the table
            loadDailyLog();

            // Update weekly summary if it's Sunday
            const entryDate = new Date(date);
            if (entryDate.getDay() === 0) { // Sunday
                initializeWeeklySummary();
            }
        }
    } catch (error) {
        console.error('Error saving entry:', error);
        showMessage('Failed to save entry', 'error');
    }
}
