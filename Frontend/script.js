// Extracted from original index.html
const API_BASE = 'http://localhost:8000';
let currentFilter = 'all';
let allResults = [];

const searchInput = document.getElementById('searchInput');
const resultsContainer = document.getElementById('results');
const statusElement = document.getElementById('status');
const resultsHeader = document.getElementById('resultsHeader');

// Search on input
searchInput.addEventListener('keydown', async (e) => {
    if (e.key === 'Enter') {
        await performSearch(searchInput.value);
    }
});

// Auto-search after typing stops
let searchTimeout;
searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    if (searchInput.value.length > 1) {
        searchTimeout = setTimeout(() => {
            performSearch(searchInput.value);
        }, 300);
    }
});

async function performSearch(query) {
    if (!query.trim()) return;

    showStatus(`<span class="loader"></span>Searching...`, 'loading');
    allResults = [];

    try {
        const response = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        allResults = data.results || [];

        displayResults();
        showStatus(`Found ${allResults.length} result${allResults.length !== 1 ? 's' : ''}`, 'success');

        // Add to recent
        addToRecent(query);
    } catch (error) {
        showStatus(`❌ Error: ${error.message}`, 'error');
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">⚠️</div>
                <div class="empty-text">Search failed</div>
                <div class="empty-hint">Make sure the server is running at ${API_BASE}</div>
            </div>
        `;
    }
}

function displayResults() {
    const filtered = currentFilter === 'all' 
        ? allResults 
        : allResults.filter(r => getFileType(r.extension) === currentFilter);

    if (filtered.length === 0) {
        resultsHeader.innerHTML = '';
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🚫</div>
                <div class="empty-text">No results for this filter</div>
                <div class="empty-hint">Try a different search or filter</div>
            </div>
        `;
        return;
    }

    resultsHeader.innerHTML = `<div class="results-header">${filtered.length} result${filtered.length !== 1 ? 's' : ''}</div>`;

    resultsContainer.innerHTML = filtered.map(result => `
        <div class="result-card">
            <div class="result-icon">${getFileIcon(result.extension)}</div>
            <div class="result-name">${escapeHtml(result.name)}</div>
            <div class="result-preview">${escapeHtml(result.snippet || 'No preview available')}</div>
            <div class="result-meta">
                <span>${result.extension.toUpperCase()}</span>
                <span>${result.size ? `${Math.round(result.size / 1024)} KB` : ''}</span>
            </div>
        </div>
    `).join('');
}

function getFileIcon(extension) {
    const type = extension.toLowerCase().replace('.', '');
    const icons = {
        pdf: '📄',
        txt: '📝',
        md: '📋',
        docx: '📘',
        jpg: '🖼️',
        png: '🖼️',
        gif: '🎬',
        mp3: '🎵',
        py: '🐍',
        js: '⚙️',
        java: '☕',
        default: '📁'
    };
    return icons[type] || icons.default;
}

function getFileType(extension) {
    const type = extension.toLowerCase().replace('.', '');
    if (type === 'pdf') return 'pdf';
    if (type === 'docx') return 'word';
    if (['jpg', 'png', 'gif'].includes(type)) return 'image';
    if (['py', 'js', 'java', 'cpp'].includes(type)) return 'code';
    return 'all';
}

function setFilter(filter) {
    currentFilter = filter;
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.toLowerCase().includes(filter) || (filter === 'all' && btn.textContent === 'All')) {
            btn.classList.add('active');
        }
    });
    displayResults();
}

function searchQuery(query) {
    searchInput.value = query;
    performSearch(query);
}

function addToRecent(query) {
    const recentList = document.getElementById('recentList');
    const isDuplicate = Array.from(recentList.children).some(item => item.textContent === query);
    if (!isDuplicate) {
        const item = document.createElement('div');
        item.className = 'recent-item';
        item.textContent = query;
        item.onclick = () => searchQuery(query);
        recentList.insertBefore(item, recentList.firstChild);
        if (recentList.children.length > 5) {
            recentList.lastChild.remove();
        }
    }
}

function showStatus(message, type = 'success') {
    statusElement.innerHTML = message;
    statusElement.className = `status show ${type}`;
    setTimeout(() => {
        statusElement.classList.remove('show');
    }, 4000);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Check server on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE}/`);
        if (response.ok) {
            showStatus('✅ Connected to RecallOS', 'success');
        }
    } catch (error) {
        showStatus(`⚠️ Cannot connect to server at ${API_BASE}`, 'error');
    }
});
