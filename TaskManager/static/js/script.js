// Function to hide the form
function hideTaskForm() {
    document.getElementById("taskForm").style.display = "none";
}

// Function to parse deadline (used for both add and update)
function parseDeadline(deadline) {
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

    // Convert to 24-hour format
    if (period === "p.m." && hour !== 12) {
        hour += 12;
    } else if (period === "a.m." && hour === 12) {
        hour = 0;
    }

    return new Date(year, month, day, hour, minute);
}

function filterTasks(status) {
    document.querySelectorAll('.task-card').forEach(task => {
        task.style.display = (status === "all" || task.dataset.status === status) ? "block" : "none";
    });
}

// Function to calculate time remaining
function updateCountdown(taskId, deadline) {
    const countdownElement = document.getElementById(`countdown-${taskId}`);
    if (!countdownElement) return;

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

// Function to initialize countdowns
function initializeCountdowns() {
    document.querySelectorAll('.task-card').forEach(task => {
        const taskId = task.querySelector('span[id^="countdown-"]').id.split('-')[1];
        const deadline = task.querySelector('span[id^="deadline-"]').textContent.trim(); // Ensure no extra spaces
        updateCountdown(taskId, deadline);
        setInterval(() => updateCountdown(taskId, deadline), 1000);
    });
}

// Function to hide messages after 5 seconds
function hideMessages() {
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 1000); // Fade out duration
        }, 5000); // 5 seconds delay
    });
}




;