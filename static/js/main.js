// Tab Switching
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');

            // Remove active class from all buttons and content
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');

            // Trigger initialization for certain tabs
            if (targetTab === 'weekly-summary') {
                initializeWeeklySummary();
            }
        });
    });

    // Set today's date in the date input
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
    }

    // Set this week type based on the last entry
    const weekTypeSelect = document.getElementById('week-type');
    if (weekTypeSelect) {
        fetchDailyLog().then(entries => {
            if (entries.length > 0) {
                const lastEntry = entries[entries.length - 1];
                weekTypeSelect.value = lastEntry.week_type;
            }
        });
    }
});

// API Helper Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(endpoint, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'API call failed');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        showMessage(error.message, 'error');
        throw error;
    }
}

async function fetchDailyLog() {
    try {
        const result = await apiCall('/api/daily-log', 'GET');
        return result.data || [];
    } catch (error) {
        return [];
    }
}

async function saveDailyEntry(data) {
    return apiCall('/api/daily-log', 'POST', data);
}

async function fetchWeeklySummaries() {
    try {
        const result = await apiCall('/api/weekly-summary', 'GET');
        return result.data || [];
    } catch (error) {
        return [];
    }
}

async function getWeeklyAverages(date) {
    try {
        const result = await apiCall(`/api/weekly-averages/${date}`, 'GET');
        return result.data;
    } catch (error) {
        return null;
    }
}

// Message Display
function showMessage(message, type = 'success') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;

    // Find where to insert the message
    const container = document.querySelector('.container');
    const header = document.querySelector('header');
    if (header) {
        header.insertAdjacentElement('afterend', messageDiv);
    } else {
        container.insertBefore(messageDiv, container.firstChild);
    }

    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Date Utilities
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function parseDate(dateString) {
    const [year, month, day] = dateString.split('-');
    return new Date(year, month - 1, day);
}

function getWeekEnding(date) {
    if (typeof date === 'string') {
        date = parseDate(date);
    }
    const dayOfWeek = date.getDay();
    const diff = date.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
    const monday = new Date(date.setDate(diff));
    const sunday = new Date(monday);
    sunday.setDate(sunday.getDate() + 6);
    return formatDate(sunday);
}

// Initialize Weekly Summary (placeholder, called from chart.js)
function initializeWeeklySummary() {
    // This is called from daily_log.js to load weekly data
}

// Stub for chart-related functions
let radarChart = null;
