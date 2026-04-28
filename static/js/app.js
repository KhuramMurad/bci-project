const socket = io();

// UI Elements
const statusDot = document.getElementById('connection-status-dot');
const statusText = document.getElementById('connection-status-text');
const focusVal = document.getElementById('focus-val');
const focusBar = document.getElementById('focus-bar');
const relaxVal = document.getElementById('relax-val');
const relaxBar = document.getElementById('relax-bar');

// Chart Setup
const ctx = document.getElementById('eegChart').getContext('2d');

const NUM_CHANNELS = 8;
const MAX_DATA_POINTS = 100;

// Initialize datasets for 8 channels
const datasets = [];
const colors = [
    '#00f0ff', '#7000ff', '#ff3366', '#00e676', 
    '#ffaa00', '#ff00aa', '#00aaff', '#aaff00'
];

for (let i = 0; i < NUM_CHANNELS; i++) {
    datasets.push({
        label: `Channel ${i+1}`,
        data: Array(MAX_DATA_POINTS).fill(0),
        borderColor: colors[i],
        borderWidth: 1.5,
        tension: 0.4, // Smooth curves
        pointRadius: 0, // Hide points for performance and aesthetics
    });
}

const chartConfig = {
    type: 'line',
    data: {
        labels: Array(MAX_DATA_POINTS).fill(''),
        datasets: datasets
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false, // Turn off chart.js animation for real-time performance
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#9ba1a6',
                    font: { family: 'Inter', size: 12 }
                }
            },
            tooltip: { enabled: false } // Disable tooltips for performance
        },
        scales: {
            x: {
                display: false, // Hide X axis
                grid: { display: false }
            },
            y: {
                display: true,
                min: -60,
                max: 60,
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)',
                },
                ticks: {
                    color: '#9ba1a6',
                    font: { family: 'Inter' }
                }
            }
        }
    }
};

const eegChart = new Chart(ctx, chartConfig);

// Socket Events
socket.on('connect', () => {
    statusDot.style.background = '#00e676'; // Green
    statusText.innerText = 'Connected';
    console.log('Connected to backend');
});

socket.on('disconnect', () => {
    statusDot.style.background = '#ff3366'; // Red
    statusText.innerText = 'Disconnected';
    console.log('Disconnected from backend');
});

// Mock metric generation for the UI dashboard panels
let focus = 50;
let relax = 50;

socket.on('eeg_data', (payload) => {
    // payload.channels is an array of 8 values
    const channels = payload.channels;
    
    // Update chart
    for (let i = 0; i < NUM_CHANNELS; i++) {
        // Remove first element, add new element
        chartConfig.data.datasets[i].data.shift();
        chartConfig.data.datasets[i].data.push(channels[i]);
    }
    
    eegChart.update();
    
    // Update Mock Metrics smoothly
    focus += (Math.random() * 4 - 2);
    relax += (Math.random() * 4 - 2);
    
    // Clamp between 0 and 100
    focus = Math.max(0, Math.min(100, focus));
    relax = Math.max(0, Math.min(100, relax));
    
    focusVal.innerText = Math.round(focus);
    focusBar.style.width = `${focus}%`;
    
    relaxVal.innerText = Math.round(relax);
    relaxBar.style.width = `${relax}%`;
});
