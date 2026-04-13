const form = document.getElementById('climbForm');
const messageBox = document.getElementById('message');
const logbook = document.getElementById('logbook');

// --- 1. AUTHORIZATION GUARD ---
function checkAuth() {
    const token = localStorage.getItem('climbToken');
    const authSection = document.getElementById('auth-links');
    const userSection = document.getElementById('user-profile');

    if (token) {
        if (authSection) authSection.style.display = 'none';
        if (userSection) userSection.style.display = 'block';
    } else {
        if (authSection) authSection.style.display = 'block';
        if (userSection) userSection.style.display = 'none';
        // Optional: Redirect if on a protected page
        if (window.location.pathname.includes('dashboard')) {
            window.location.href = '/static/login.html';
        }
    }
}

function logout() {
    localStorage.removeItem('climbToken');
    localStorage.removeItem('userId');
    window.location.href = '/static/index.html';
}

// --- 2. FETCH & RENDER LOGBOOK ---
async function fetchClimbs(filterSent = false) {
    const userId = localStorage.getItem('userId');
    const token = localStorage.getItem('climbToken');

    if (!token || !userId) return;

    try {
        const response = await fetch(`/users/${userId}/logbook`, {
            headers: {
                "Authorization": `Bearer ${token}`,
                "ngrok-skip-browser-warning": "69420"
            }
        });

        if (response.status === 401) logout();

        let climbs = await response.json();

        // Frontend filtering for the "Sent Only" button
        if (filterSent) {
            climbs = climbs.filter(c => c.is_sent === true);
        }

        renderLogbook(climbs);
    } catch (error) {
        logbook.innerHTML = '<p style="color:red; text-align:center;">Could not load logbook.</p>';
    }
}

function renderLogbook(climbs) {
    logbook.innerHTML = '';

    if (climbs.length === 0) {
        logbook.innerHTML = '<p style="text-align:center; color:#777;">No climbs found!</p>';
        return;
    }

    climbs.forEach(climb => {
        const statusClass = climb.is_sent ? 'sent' : 'project';
        const statusText = climb.is_sent ? 'Sent ✅' : 'Project ⏳';

        // Note: We access climb.route.name because of the nested Pydantic schema
        const climbCard = `
            <div class="climb-card ${statusClass}">
                <div class="climb-info">
                    <span class="climb-name">${climb.route.name}</span>
                    <span>Grade: ${climb.route.grade}</span>
                    <span style="font-size: 12px; color: #666;">
                        Attempts: <strong>${climb.attempts}</strong>
                    </span>
                </div>
                <div class="climb-status">
                    ${statusText}
                </div>
            </div>
        `;
        logbook.innerHTML += climbCard;
    });
}

// --- 3. THE TWO-STEP LOGGING PROCESS ---
form.addEventListener('submit', async function(event) {
    event.preventDefault();

    const token = localStorage.getItem('climbToken');
    const userId = localStorage.getItem('userId');

    if (!token) {
        showMessage("Please login first", "error");
        return;
    }

    const routeData = {
        name: document.getElementById('name').value,
        grade: document.getElementById('grade').value
    };

    try {
        // STEP 1: Create or Get the Route
        const routeResponse = await fetch('/routes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(routeData)
        });
        const route = await routeResponse.json();

        // STEP 2: Create the Climb Log using the new route ID
        const climbData = {
            user_id: userId,
            route_id: route.id,
            is_sent: document.getElementById('is_sent').checked,
            attempts: 1 // Default to 1 for a new log
        };

        const response = await fetch('/climbs/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(climbData)
        });

        if (response.ok) {
            showMessage("Climb logged successfully!", 'success');
            form.reset();
            fetchClimbs();
        } else {
            const err = await response.json();
            showMessage(`Error: ${err.detail}`, 'error');
        }
    } catch (error) {
        showMessage("Connection error", 'error');
    }
});

// --- 4. HELPERS & EVENTS ---
function showMessage(text, type) {
    messageBox.textContent = text;
    messageBox.className = type;
    messageBox.style.display = 'block';
    setTimeout(() => { messageBox.style.display = 'none'; }, 4000);
}

document.getElementById('btnAll').addEventListener('click', (e) => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    fetchClimbs(false);
});

document.getElementById('btnSent').addEventListener('click', (e) => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    fetchClimbs(true);
});

// Initial Setup
checkAuth();
fetchClimbs();
