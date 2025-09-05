// src/static/js/main.js
let usersList = [];

async function fetchUsers() {
    try {
        console.log('Fetching users from /get-users');
        const response = await fetch('/get-users', {
            method: 'GET',
            headers: {'Content-Type': 'application/json'}
        });
        const data = await response.json();
        console.log('Fetched users:', data);
        if (data.error) {
            console.error('Error fetching users:', data.error);
            showNotification('Failed to load users: ' + data.error);
            return [];
        }
        const users = Array.isArray(data.users) ? data.users : [];
        if (users.length === 0) {
            console.log('No users returned from server');
            showNotification('No users found in the system');
        }
        return users;
    } catch (error) {
        console.error('Network error fetching users:', error);
        showNotification('Network error: Unable to fetch users');
        return [];
    }
}

async function refreshUserDropdown() {
    const userSelect = document.getElementById('user');
    console.log('Refreshing user dropdown');
    try {
        usersList = await fetchUsers();
        console.log('Populating dropdown with users:', usersList);
        userSelect.innerHTML = '<option value="" disabled selected>Select a user</option>';
        if (usersList.length === 0) {
            showNotification('No users found in the system');
            userSelect.innerHTML += '<option value="" disabled>No users available</option>';
        } else {
            usersList.sort();
            usersList.forEach(u => {
                const option = document.createElement('option');
                option.value = u;
                option.textContent = u.charAt(0).toUpperCase() + u.slice(1);
                userSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error refreshing dropdown:', error);
        showNotification('Error loading user dropdown');
    }
}

// Initialize dropdown
refreshUserDropdown();

function showNotification(message, isError = true) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.display = 'block';
    notification.className = isError ? 'error' : 'success';
    console.log(`Notification: ${message} (isError: ${isError})`);
    setTimeout(() => { notification.style.display = 'none'; }, 5000);
}

async function getRecommendations() {
    const user = document.getElementById('user').value;
    if (!user) return showNotification('Please select a user');
    console.log(`Fetching recommendations for user: ${user}`);
    try {
        const response = await fetch('/get-recommendations', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user})
        });
        const data = await response.json();
        console.log('Recommendations response:', data);
        if (data.error) {
            showNotification(data.error);
            return;
        }
        // Debug watched data
        console.log('Watched movies:', data.watched);
        const recommendationsDiv = document.getElementById('recommendations');
        recommendationsDiv.innerHTML = data.recommendations && data.recommendations.length
            ? data.recommendations.map(r => `<p>${(r.title || r.id || 'Unknown').charAt(0).toUpperCase() + (r.title || r.id || 'unknown').slice(1).replace(/-/g, ' ')}</p>`).join('')
            : '<p>No recommendations available.</p>';
        const explanationsDiv = document.getElementById('explanations');
        explanationsDiv.innerHTML = data.explanations && data.explanations.length
            ? data.explanations.map((expList, i) => `<div><h3>${(data.recommendations[i]?.title || data.recommendations[i]?.id || 'Movie').charAt(0).toUpperCase() + (data.recommendations[i]?.title || data.recommendations[i]?.id || 'movie').slice(1).replace(/-/g, ' ')}</h3>${expList.map(e => `<p>${e}</p>`).join('')}</div>`).join('')
            : '<p>No explanations available.</p>';
        document.getElementById('similar-users').innerHTML = data.similar_users && data.similar_users.length
            ? data.similar_users.map(u => `<p>${u.charAt(0).toUpperCase() + u.slice(1)}</p>`).join('')
            : '<p>No similar users found.</p>';
        const viewingHistoryDiv = document.getElementById('viewing-history');
        if (!viewingHistoryDiv) {
            console.error('Viewing history div not found');
            showNotification('Error: Viewing history element not found');
            return;
        }
        viewingHistoryDiv.innerHTML = data.watched && data.watched.length
            ? data.watched.map(m => {
                console.log('Rendering movie:', m);
                return `<p>${(m.title || m.id || 'Unknown').charAt(0).toUpperCase() + (m.title || m.id || 'unknown').slice(1).replace(/-/g, ' ')}</p>`;
              }).join('')
            : '<p>No viewing history available.</p>';
        showNotification('Recommendations loaded successfully', false);
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        showNotification('Network error: Unable to fetch recommendations');
    }
}

async function addUser() {
    const newUser = document.getElementById('newUser').value.trim().toLowerCase();
    if (!newUser) return showNotification("Enter user ID.");
    console.log(`Adding user: ${newUser}`);
    try {
        const response = await fetch('/add-user', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user: newUser})
        });
        const data = await response.json();
        console.log('Add user response:', data);
        if (data.error) return showNotification(data.error);
        showNotification(data.message, false);
        await refreshUserDropdown();
        document.getElementById('newUser').value = '';
    } catch (error) {
        console.error('Error adding user:', error);
        showNotification('Network error: Unable to add user');
    }
}

async function updatePreferences() {
    const user = document.getElementById('user').value;
    const newGenre = document.getElementById('newGenre').value.trim();
    if (!user) return showNotification('Please select a user');
    if (!newGenre) return showNotification("Enter genre.");
    console.log(`Updating preferences: user=${user}, genre=${newGenre}`);
    try {
        const response = await fetch('/update-preferences', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user, new_genre: newGenre})
        });
        const data = await response.json();
        console.log('Update preferences response:', data);
        if (data.error) return showNotification(data.error);
        showNotification(data.message, false);
        document.getElementById('newGenre').value = '';
    } catch (error) {
        console.error('Error updating preferences:', error);
        showNotification('Network error: Unable to update preferences');
    }
}

async function parseQuery() {
    const user = document.getElementById('user').value;
    const question = document.getElementById('question').value.trim();
    if (!user) return showNotification('Please select a user');
    if (!question) return showNotification("Enter question.");
    console.log(`Parsing query: user=${user}, question=${question}`);
    try {
        const response = await fetch('/parse-query', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user, question})
        });
        const data = await response.json();
        console.log('Parse query response:', data);
        if (data.error) {
            showNotification(data.error);
            return;
        }
        const recommendationsDiv = document.getElementById('recommendations');
        const explanationsDiv = document.getElementById('explanations');
        if (!recommendationsDiv || !explanationsDiv) {
            console.error('DOM elements missing: recommendations or explanations');
            showNotification('Error: Page elements not found');
            return;
        }
        recommendationsDiv.innerHTML = data.recommendations && data.recommendations.length
            ? data.recommendations.map(r => `<p>${(r.title || r.id || 'Unknown').charAt(0).toUpperCase() + (r.title || r.id || 'unknown').slice(1).replace(/-/g, ' ')}</p>`).join('')
            : '<p>No recommendations available.</p>';
        explanationsDiv.innerHTML = data.explanations && data.explanations.length
            ? data.explanations.map((expList, i) => `<div><h3>${(data.recommendations[i]?.title || data.recommendations[i]?.id || 'Movie').charAt(0).toUpperCase() + (data.recommendations[i]?.title || data.recommendations[i]?.id || 'movie').slice(1).replace(/-/g, ' ')}</h3>${expList.map(e => `<p>${e}</p>`).join('')}</div>`).join('')
            : '<p>No explanations available.</p>';
        showNotification('Query parsed successfully', false);
    } catch (error) {
        console.error('Error parsing query:', error);
        showNotification('Network error: Unable to parse query');
    }
}

async function refreshMovieDropdown() {
    const movieSelect = document.getElementById('movie-to-rate');
    console.log('Refreshing movie dropdown');
    movieSelect.innerHTML = '<option value="" disabled selected>Select a movie</option>';
    try {
        const response = await fetch('/get-movies', {
            method: 'GET',
            headers: {'Content-Type': 'application/json'}
        });
        const data = await response.json();
        console.log('Fetched movies:', data);
        let movies = data.movies || ['inception', 'interstellar', 'the-matrix', 'titanic', 'avatar'];
        movies.sort();
        movies.forEach(m => {
            const option = document.createElement('option');
            option.value = m;
            option.textContent = m.charAt(0).toUpperCase() + m.slice(1).replace(/-/g, ' ');
            movieSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching movies:', error);
        showNotification('Error loading movie dropdown');
        ['inception', 'interstellar', 'the-matrix', 'titanic', 'avatar'].sort().forEach(m => {
            const option = document.createElement('option');
            option.value = m;
            option.textContent = m.charAt(0).toUpperCase() + m.slice(1).replace(/-/g, ' ');
            movieSelect.appendChild(option);
        });
    }
}
refreshMovieDropdown();

async function addRating() {
    const user = document.getElementById('user').value;
    const movie = document.getElementById('movie-to-rate').value;
    const rating = document.getElementById('rating-value').value;
    if (!user) return showNotification('Please select a user');
    if (!movie || !rating) return showNotification('Movie and rating required');
    console.log(`Adding rating: user=${user}, movie=${movie}, rating=${rating}`);
    try {
        const response = await fetch('/add-rating', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user, movie, rating})
        });
        const data = await response.json();
        console.log('Add rating response:', data);
        if (data.error) return showNotification(data.error);
        showNotification(data.message, false);
        document.getElementById('rating-value').value = '';
    } catch (error) {
        console.error('Error adding rating:', error);
        showNotification('Network error: Unable to add rating');
    }
}