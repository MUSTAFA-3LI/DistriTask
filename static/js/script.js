let tasks = [];

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('taskForm').style.display = 'none';
});

// Show Task Form
function showTaskForm() {
    document.getElementById('taskForm').style.display = 'block';
}

// Hide Task Form
function hideTaskForm() {
    document.getElementById('taskForm').style.display = 'none';
}

// Add Task
function addTask() {
    const employeeInput = document.getElementById('taskEmployee');
    const nameInput = document.getElementById('taskName');
    const descriptionInput = document.getElementById('taskDescription');
    const deadlineInput = document.getElementById('taskDeadline');
    const priorityInput = document.getElementById('taskPriority');
    const statusInput = document.getElementById('taskStatus');

    if (!employeeInput || !nameInput || !descriptionInput || !deadlineInput || !priorityInput || !statusInput) {
        console.error('One or more input elements not found');
        return;
    }

    const employee = employeeInput.value.trim();
    const name = nameInput.value.trim();
    const description = descriptionInput.value.trim();
    const deadline = deadlineInput.value.trim();
    const priority = priorityInput.value;
    const status = statusInput.value;

    if (!name || !deadline) {
        alert('Please enter task name and deadline');
        return;
    }

    const task = { employee, name, description, deadline, priority, status };
    tasks.push(task);
    displayTasks('all');
    hideTaskForm();
    
    // Clear form inputs after adding task
    employeeInput.value = '';
    nameInput.value = '';
    descriptionInput.value = '';
    deadlineInput.value = '';
    priorityInput.value = 'low';
    statusInput.value = 'pending';
}

// Display Tasks
function displayTasks(filter) {
    const taskList = document.getElementById('taskList');
    if (!taskList) {
        console.error('Task list element not found');
        return;
    }
    
    taskList.innerHTML = '';
    
    const filteredTasks = filter === 'all' ? tasks : tasks.filter(task => task.status === filter);
    
    if (filteredTasks.length === 0) {
        taskList.innerHTML = '📋 No tasks available';
        return;
    }
    
    filteredTasks.forEach(task => {
        let div = document.createElement('div');
        div.className = `task ${task.priority}`;
        div.innerHTML = `
            <h3>📌 ${task.name}</h3>
            <p>👤 Employee: ${task.employee}</p>
            <p>📝 ${task.description}</p>
            <p>🕒 ${new Date(task.deadline).toLocaleString()}</p>
            <p>Status: ${task.status}</p>
        `;
        taskList.appendChild(div);
    });
}

// Filter Tasks
function filterTasks(status) {
    if (status === 'in-progress') {
        const inProgressTasks = tasks.filter(task => task.status === 'in-progress');

        if (inProgressTasks.length === 0) {
            document.getElementById('taskList').innerHTML = '⚙️ No In-Progress Tasks';
            return;
        }

        displayTasks('in-progress');
    } else {
        displayTasks(status);
    }
}

// Logout Function with Confirmation
function logout() {
    // Show confirmation message
    const confirmLogout = confirm("Are you sure you want to logout?");
    
    // If user confirms, redirect to homepage
    if (confirmLogout) {
        window.location.href = "../index.html"; // Replace with your homepage URL
    }
    // If user cancels, do nothing
}

function toggleDropdown() {
    const dropdown = document.getElementById('userDropdown');
    dropdown.classList.toggle('show');
}

// Close the dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('userDropdown');
    const profile = document.querySelector('.profile');
    
    if (!profile.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.classList.remove('show');
    }
});


















