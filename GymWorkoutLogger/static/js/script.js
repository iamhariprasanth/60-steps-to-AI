let currentSlideIndex = 1;
let donutChart = null;
let repsChart = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    showSlide(currentSlideIndex);
    loadDashboard();
    setupFormListener();
    autoSlide();
    setupMusicControls();
});

// ==================== SLIDER FUNCTIONALITY ====================
function changeSlide(n) {
    showSlide(currentSlideIndex += n);
}

function currentSlide(n) {
    showSlide(currentSlideIndex = n);
}

function showSlide(n) {
    const slides = document.getElementsByClassName("slide");
    const dots = document.getElementsByClassName("dot");
    
    if (n > slides.length) {
        currentSlideIndex = 1;
    }
    if (n < 1) {
        currentSlideIndex = slides.length;
    }
    
    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active");
    }
    for (let i = 0; i < dots.length; i++) {
        dots[i].classList.remove("active");
    }
    
    slides[currentSlideIndex - 1].classList.add("active");
    dots[currentSlideIndex - 1].classList.add("active");
}

function autoSlide() {
    currentSlideIndex++;
    showSlide(currentSlideIndex);
    setTimeout(autoSlide, 8000); // Change slide every 8 seconds
}

// ==================== MUSIC CONTROLS ====================
function setupMusicControls() {
    const music = document.getElementById('gymMusic');
    const musicToggle = document.getElementById('musicToggle');
    const volumeControl = document.getElementById('volumeControl');
    
    // Set initial volume
    music.volume = 0.3;
    
    // Auto-play with user interaction
    musicToggle.addEventListener('click', function() {
        if (music.paused) {
            music.play().catch(err => console.log('Autoplay prevented:', err));
            musicToggle.classList.add('playing');
            musicToggle.textContent = '🔊 Playing';
        } else {
            music.pause();
            musicToggle.classList.remove('playing');
            musicToggle.textContent = '🔇 Paused';
        }
    });
    
    // Volume control
    volumeControl.addEventListener('input', function() {
        music.volume = this.value / 100;
    });
    
    // Attempt auto-play on page load
    setTimeout(() => {
        music.play().catch(err => {
            console.log('Autoplay prevented by browser. Click music button to play.');
        });
        musicToggle.classList.add('playing');
        musicToggle.textContent = '🔊 Playing';
    }, 1000);
}
function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active');
    });
    
    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.add('active');
    }
    
    // Add active class to clicked nav link
    event.target.classList.add('active');
    
    // Load data when section changes
    if (sectionId === 'dashboard') {
        setTimeout(() => loadDashboard(), 100);
    } else if (sectionId === 'analytics') {
        setTimeout(() => loadAnalytics(), 100);
    }
}

// ==================== FORM HANDLING ====================
function setupFormListener() {
    const form = document.getElementById('workout-form');
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            exercise: document.getElementById('exercise').value,
            sets: document.getElementById('sets').value,
            reps: document.getElementById('reps').value,
            weight: document.getElementById('weight').value,
            notes: document.getElementById('notes').value
        };
        
        try {
            const response = await fetch('/add-workout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            const messageDiv = document.getElementById('form-message');
            if (data.success) {
                messageDiv.className = 'message success';
                messageDiv.textContent = '✅ ' + data.message;
                form.reset();
                setTimeout(() => {
                    messageDiv.textContent = '';
                }, 3000);
                // Refresh dashboard
                loadDashboard();
            } else {
                messageDiv.className = 'message error';
                messageDiv.textContent = '❌ Error: ' + data.message;
            }
        } catch (error) {
            const messageDiv = document.getElementById('form-message');
            messageDiv.className = 'message error';
            messageDiv.textContent = '❌ Error: ' + error.message;
        }
    });
}

// ==================== DASHBOARD LOADING ====================
async function loadDashboard() {
    try {
        const [workouts, weeklyStats, exerciseStats] = await Promise.all([
            fetch('/get-workouts').then(r => r.json()),
            fetch('/get-weekly-stats').then(r => r.json()),
            fetch('/get-exercise-stats').then(r => r.json())
        ]);
        
        // Update stats
        updateStats(workouts, weeklyStats, exerciseStats);
        
        // Update table
        updateWorkoutsTable(workouts);
        
        // Update weekly chart
        updateWeeklyChart(weeklyStats);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function updateStats(workouts, weeklyStats, exerciseStats) {
    // Total workouts
    document.getElementById('total-workouts').textContent = workouts.length;
    
    // This week workouts
    const weekWorkouts = Object.values(weeklyStats).reduce((sum, day) => sum + day.exercises, 0);
    document.getElementById('week-workouts').textContent = weekWorkouts;
    
    // Total weight
    let totalWeight = 0;
    workouts.forEach(workout => {
        totalWeight += workout.weight * workout.sets;
    });
    document.getElementById('total-weight').textContent = totalWeight.toFixed(0) + ' kg';
    
    // Favorite exercise
    if (Object.keys(exerciseStats).length > 0) {
        const favorite = Object.entries(exerciseStats).reduce((max, [exercise, stats]) => 
            stats.count > max.count ? {exercise, count: stats.count} : max, 
            {exercise: 'N/A', count: 0}
        );
        document.getElementById('fav-exercise').textContent = favorite.exercise;
    }
}

function updateWorkoutsTable(workouts) {
    const tbody = document.getElementById('workouts-tbody');
    
    if (workouts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-message">No workouts logged yet. Start by logging your first workout!</td></tr>';
        return;
    }
    
    // Show last 10 workouts
    const recentWorkouts = workouts.slice(-10).reverse();
    tbody.innerHTML = recentWorkouts.map(workout => `
        <tr>
            <td>${new Date(workout.date).toLocaleString()}</td>
            <td><strong>${workout.exercise}</strong></td>
            <td>${workout.sets}</td>
            <td>${workout.reps}</td>
            <td>${workout.weight}</td>
            <td>${workout.notes || '-'}</td>
            <td>
                <button class="btn-delete" onclick="deleteWorkout(${workout.id})">🗑️</button>
            </td>
        </tr>
    `).join('');
}

function updateWeeklyChart(weeklyStats) {
    const ctx = document.getElementById('weeklyChart').getContext('2d');
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const exerciseCounts = days.map(day => weeklyStats[day]?.exercises || 0);
    const repsData = days.map(day => weeklyStats[day]?.total_reps || 0);
    
    if (weeklyChart) {
        weeklyChart.destroy();
    }
    
    weeklyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: days,
            datasets: [
                {
                    label: 'Exercises Completed',
                    data: exerciseCounts,
                    backgroundColor: '#FF6B6B',
                    borderColor: '#C92A2A',
                    borderWidth: 2
                },
                {
                    label: 'Total Reps',
                    data: repsData,
                    backgroundColor: '#4ECDC4',
                    borderColor: '#0F8B8D',
                    borderWidth: 2,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#333',
                        font: { size: 12 }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#666' },
                    grid: { color: '#e0e0e0' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    ticks: { color: '#666' },
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });
}

// ==================== ANALYTICS LOADING ====================
async function loadAnalytics() {
    try {
        const [trends, exerciseStats] = await Promise.all([
            fetch('/get-trends').then(r => r.json()),
            fetch('/get-exercise-stats').then(r => r.json())
        ]);
        
        updateTrendPivotTable(trends);
        updateDonutChart(exerciseStats);
        updateRepsChart(trends);
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

function updateTrendPivotTable(trends) {
    const tbody = document.getElementById('trendTableBody');
    
    if (Object.keys(trends).length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-message">No workout data available</td></tr>';
        return;
    }
    
    tbody.innerHTML = Object.entries(trends).map(([exercise, data]) => {
        if (data.length === 0) return '';
        
        const latestWeight = data[data.length - 1].weight;
        const maxWeight = Math.max(...data.map(d => d.weight));
        const avgWeight = (data.reduce((sum, d) => sum + d.weight, 0) / data.length).toFixed(1);
        const totalReps = data.reduce((sum, d) => sum + (d.reps * d.sets), 0);
        const timesDone = data.length;
        
        // Calculate progress
        const firstWeight = data[0].weight;
        const progress = ((latestWeight - firstWeight) / firstWeight * 100).toFixed(1);
        const progressColor = progress >= 0 ? '#00E676' : '#FF1744';
        const progressArrow = progress >= 0 ? '📈' : '📉';
        
        return `
            <tr>
                <td><strong>${exercise}</strong></td>
                <td>${latestWeight} kg</td>
                <td>${maxWeight} kg</td>
                <td>${avgWeight} kg</td>
                <td>${totalReps}</td>
                <td>${timesDone}</td>
                <td style="color: ${progressColor}; font-weight: 700;">
                    ${progressArrow} ${progress}%
                </td>
            </tr>
        `;
    }).join('');
}

function updateDonutChart(exerciseStats) {
    const ctx = document.getElementById('donutChart').getContext('2d');
    
    const exercises = Object.keys(exerciseStats);
    const counts = Object.values(exerciseStats).map(stat => stat.count);
    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#FF8B94', '#A8E6CF', '#FFD3B6'];
    
    if (donutChart) {
        donutChart.destroy();
    }
    
    donutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: exercises,
            datasets: [{
                data: counts,
                backgroundColor: colors.slice(0, exercises.length),
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#333',
                        font: { size: 12 },
                        padding: 15
                    }
                }
            }
        }
    });
}

function updateRepsChart(trends) {
    const ctx = document.getElementById('repsChart').getContext('2d');
    
    const exercises = [];
    const reps = [];
    const colors = [];
    const colorPalette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#FF8B94'];
    let colorIndex = 0;
    
    for (const [exercise, data] of Object.entries(trends)) {
        if (data.length > 0) {
            exercises.push(exercise);
            const totalReps = data.reduce((sum, d) => sum + (d.reps * d.sets), 0);
            reps.push(totalReps);
            colors.push(colorPalette[colorIndex % colorPalette.length]);
            colorIndex++;
        }
    }
    
    if (repsChart) {
        repsChart.destroy();
    }
    
    repsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: exercises,
            datasets: [{
                label: 'Total Reps',
                data: reps,
                backgroundColor: colors,
                borderColor: colors.map(c => c + 'CC'),
                borderWidth: 2
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    ticks: { color: '#666' },
                    grid: { color: '#e0e0e0' }
                },
                y: {
                    ticks: { color: '#666' }
                }
            }
        }
    });
}

// ==================== DELETE WORKOUT ====================
async function deleteWorkout(workoutId) {
    if (!confirm('Are you sure you want to delete this workout?')) return;
    
    try {
        const response = await fetch(`/delete-workout/${workoutId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        if (data.success) {
            loadDashboard();
        } else {
            alert('Error deleting workout: ' + data.message);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}
