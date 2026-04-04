const form = document.getElementById('climbForm');
const messageBox = document.getElementById('message');
const logbook = document.getElementById('logbook');

async function fetchClimbs(endpoint = 'climbs/') {
    try {
		const response = await fetch(`/${endpoint}`, {
    		headers: {
        	"ngrok-skip-browser-warning": "69420"
    		}
		});
        const climbs = await response.json();

        logbook.innerHTML = '';

        climbs.forEach(climb => {
            const statusClass = climb.is_sent ? 'sent' : 'project';
            const statusText = climb.is_sent ? 'Sent ✅' : 'Project ⏳';
            const statusBadge = climb.is_sent ? 'status-sent' : 'status-project';

            const climbCard = `
                <div class="climb-card ${statusClass}">
                    <div class="climb-info">
                        <span class="climb-name">${climb.name}</span>
                        <span>Grade: ${climb.grade}</span>
                        <span style="font-size: 13px; color: #666;">
                            Attempts: <strong>${climb.attempts}</strong>
                        </span>
                    </div>
                    <div class="climb-status ${statusBadge}">
                        ${statusText}
                    </div>
                </div>
            `;
            logbook.innerHTML += climbCard;
        });

        if (climbs.length === 0) {
            logbook.innerHTML = '<p style="text-align:center; color:#777;">Nothing found here!</p>';
        }

    } catch (error) {
        logbook.innerHTML = '<p style="color:red; text-align:center;">Could not load climbs.</p>';
    }
}

// Button Events
const btnAll = document.getElementById('btnAll');
const btnSent = document.getElementById('btnSent');

btnAll.addEventListener('click', () => {
    btnAll.classList.add('active');
    btnSent.classList.remove('active');
    fetchClimbs('climbs/');
});

btnSent.addEventListener('click', () => {
    btnSent.classList.add('active');
    btnAll.classList.remove('active');
    fetchClimbs('climbs/sent/');
});

// Form Submit
form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const climbData = {
        name: document.getElementById('name').value,
        grade: document.getElementById('grade').value,
        is_sent: document.getElementById('is_sent').checked
    };

    try {
        const response = await fetch(`/climbs/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "ngrok-skip-browser-warning": "69420" // Add this here too!
            },
            body: JSON.stringify(climbData)
		});

        const responseData = await response.json();

        if (response.ok) {
            showMessage(`Success! Logged: ${responseData.name}`, 'success');
            form.reset();
            fetchClimbs();
        } else {
            showMessage(`Error: ${responseData.detail}`, 'error');
        }
    } catch (error) {
        showMessage("Error: Could not connect to the server.", 'error');
    }
});

function showMessage(text, type) {
    messageBox.textContent = text;
    messageBox.className = type;
    messageBox.style.display = 'block';
    setTimeout(() => { messageBox.style.display = 'none'; }, 4000);
}

// Initial load
fetchClimbs();
