// AtalantaClaudiens — Gallery & Lightbox
// Adapted from HPMarginalia script.js

let allEntries = [];
let filteredEntries = [];
let currentIndex = 0;

async function loadData() {
    const resp = await fetch('data.json');
    const data = await resp.json();
    allEntries = data.entries || [];
    filteredEntries = [...allEntries];
    renderStats(data.stats || {});
    renderGallery();
}

function renderStats(stats) {
    const container = document.getElementById('stats');
    if (!container) return;
    container.innerHTML = `
        <div class="stat-card"><span class="stat-number">${stats.total_emblems || 0}</span><span class="stat-label">Emblems</span></div>
        <div class="stat-card"><span class="stat-number">${stats.with_motto || 0}</span><span class="stat-label">With Motto</span></div>
        <div class="stat-card"><span class="stat-number">${stats.scholarly_refs || 0}</span><span class="stat-label">Scholarly References</span></div>
        <div class="stat-card"><span class="stat-number">${stats.source_links || 0}</span><span class="stat-label">Source Links</span></div>
    `;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function renderGallery() {
    const gallery = document.getElementById('gallery');
    if (!gallery) return;
    gallery.innerHTML = filteredEntries.map((entry, i) => `
        <div class="card" onclick="openLightbox(${i})">
            <div class="card-placeholder">${entry.roman || 'F'}</div>
            <div class="card-body">
                <div class="card-sig">${entry.roman ? 'Emblem ' + entry.roman : 'Frontispiece'}</div>
                <div class="card-label">${escapeHtml(entry.label)}</div>
                <div class="card-desc">${escapeHtml(entry.motto || '')}</div>
            </div>
        </div>
    `).join('');
}

function openLightbox(index) {
    currentIndex = index;
    const entry = filteredEntries[index];
    const lb = document.getElementById('lightbox');
    const details = lb.querySelector('.lightbox-details');
    details.innerHTML = `
        <h3>${entry.roman ? 'Emblem ' + entry.roman : 'Frontispiece'} — ${escapeHtml(entry.label)}</h3>
        ${entry.motto ? `<div class="lightbox-motto">${escapeHtml(entry.motto)}</div>` : ''}
        ${entry.discourse ? `<div class="lightbox-desc">${escapeHtml(entry.discourse).substring(0, 600)}${entry.discourse.length > 600 ? '...' : ''}</div>` : ''}
        <p style="margin-top:1rem"><a href="emblems/${entry.page}" style="color:var(--accent-light)">View full emblem page &rarr;</a></p>
    `;
    lb.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    document.getElementById('lightbox').classList.remove('active');
    document.body.style.overflow = '';
}

function navigateLightbox(dir) {
    const newIndex = currentIndex + dir;
    if (newIndex >= 0 && newIndex < filteredEntries.length) {
        openLightbox(newIndex);
    }
}

document.addEventListener('keydown', (e) => {
    const lb = document.getElementById('lightbox');
    if (!lb || !lb.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') navigateLightbox(-1);
    if (e.key === 'ArrowRight') navigateLightbox(1);
});

document.addEventListener('DOMContentLoaded', loadData);
