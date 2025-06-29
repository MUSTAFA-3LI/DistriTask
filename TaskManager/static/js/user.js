let tasks = [];

document.addEventListener("DOMContentLoaded", () => {
    loadTasks();
});

// Load Tasks from LocalStorage
function loadTasks() {
    const savedTasks = localStorage.getItem('tasks');
    if (savedTasks) {
        tasks = JSON.parse(savedTasks);
        displayTasks('all');
    }
}

// Display Tasks
function displayTasks(filter) {
    const tasksGrid = document.querySelector(".tasks-grid");
    tasksGrid.innerHTML = '';
    
    let filteredTasks = tasks;

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    switch (filter) {
        case 'all':
            filteredTasks = tasks;
            break;
        case 'upcoming':
            filteredTasks = tasks.filter(task => new Date(task.deadline) > new Date());
            break;
        case 'current':
            filteredTasks = tasks.filter(task => {
                const taskDate = new Date(task.deadline);
                taskDate.setHours(0, 0, 0, 0);
                return taskDate.getTime() === today.getTime();
            });
            break;
        case 'delayed':
            filteredTasks = tasks.filter(task => new Date(task.deadline) < new Date() && task.status !== 'completed');
            break;
        default:
            filteredTasks = tasks;
    }

    // Sort tasks by priority
    filteredTasks.sort((a, b) => {
        const priorityOrder = { high: 1, medium: 2, low: 3 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
    });

    if (filteredTasks.length === 0) {
        tasksGrid.innerHTML = '📋 <span class="lang-no-tasks">No tasks available</span>';
        return;
    }
    
    filteredTasks.forEach((task, index) => {
        let div = document.createElement('div');
        div.className = `task-item ${task.priority}`;

        const isDelayed = new Date(task.deadline) < new Date() && task.status !== 'completed';
        if (isDelayed) {
            div.classList.add('delayed');
        }

        div.innerHTML = `
            <h3>📌 ${task.name}</h3>
            <p>👤 Employee: ${task.employee}</p>
            <p>📝 ${task.description}</p>
            <p>🕒 ${new Date(task.deadline).toLocaleString()}</p>
            <p>Status: ${task.status}</p>
            ${isDelayed ? '<p class="warning">⚠️ This task is delayed!</p>' : ''}
        `;
        tasksGrid.appendChild(div);
    });
}

// Filter Tasks
function filterTasks(status) {
    displayTasks(status);
}

// Function to handle task completion
function completeTask(taskId, event = null) {
    // Prevent default form submission if event is provided
    if (event && typeof event.preventDefault === 'function') {
        event.preventDefault();
    }
    
    // Update task status to completed
    const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
    if (taskElement) {
        taskElement.classList.add('completed');
        taskElement.setAttribute('data-status', 'completed');
        
        // Stop countdown and show completed message
        const countdownElement = document.getElementById(`countdown-${taskId}`);
        if (countdownElement) {
            countdownElement.textContent = "✅ Task completed";
            countdownElement.style.color = "#28a745";
            countdownElement.style.fontWeight = "600";
        }
        
        // Call stopCountdown function if it exists
        if (typeof stopCountdown === 'function') {
            stopCountdown(taskId);
        }
        
        // Hide the complete button
        const completeBtn = taskElement.querySelector('.complete-btn');
        if (completeBtn) {
            completeBtn.style.display = 'none';
        }
    }
}

// Update countdown function to check task status
function updateCountdown(taskId, deadline) {
    const countdownElement = document.getElementById(`countdown-${taskId}`);
    if (!countdownElement) return;

    // Check if task is completed
    const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
    if (taskElement && taskElement.getAttribute('data-status') === 'completed') {
        countdownElement.textContent = "✅ Task completed";
        countdownElement.style.color = "#28a745";
        countdownElement.style.fontWeight = "600";
        return; // Stop updating countdown for completed tasks
    }

    const deadlineDate = parseDeadline(deadline);
    if (isNaN(deadlineDate.getTime())) {
        countdownElement.textContent = "Invalid deadline!";
        return;
    }

    const now = new Date().getTime();
    const timeRemaining = deadlineDate.getTime() - now;

    if (timeRemaining <= 0) {
        countdownElement.textContent = "Deadline passed!";
        return;
    }

    const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

    countdownElement.textContent = `${days}d ${hours}h ${minutes}m ${seconds}s`;
}

// Function to parse deadline (keep existing function)
function parseDeadline(deadline) {
    if (deadline.includes("T")) {
        return new Date(deadline);
    }
    const months = {
        "January": 0, "February": 1, "March": 2, "April": 3, "May": 4, "June": 5,
        "July": 6, "August": 7, "September": 8, "October": 9, "November": 10, "December": 11
    };
    const parts = deadline.split(/[\s,]+/);
    const month = months[parts[0]];
    const day = parseInt(parts[1], 10);
    const year = parseInt(parts[2], 10);
    const timeParts = parts[3].split(":");
    let hour = parseInt(timeParts[0], 10);
    const minute = parseInt(timeParts[1], 10);
    const period = parts[4];
    if (period === "p.m." && hour !== 12) {
        hour += 12;
    } else if (period === "a.m." && hour === 12) {
        hour = 0;
    }
    return new Date(year, month, day, hour, minute);
}

// Update the existing completeTask function to call the new one
function completeTaskWithConfirmation(event, taskId) {
    event.preventDefault();
    
    // Show confirmation dialog
    if (confirm('Are you sure you want to mark this task as completed?')) {
        // Call the new completeTask function without event parameter
        completeTask(taskId);
        
        // You can also add AJAX call here to update the backend
        // For now, we'll just update the frontend
        console.log(`Task ${taskId} marked as completed`);
    }
}