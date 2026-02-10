// StellarPulse GitHub Pages App

const app = {
    data: null,
    
    async init() {
        try {
            await this.loadData();
            this.render();
        } catch (err) {
            console.error('Failed to load data:', err);
            this.showError();
        }
    },
    
    async loadData() {
        const response = await fetch('data/site_data.json');
        this.data = await response.json();
    },
    
    render() {
        if (!this.data) return;
        
        this.renderHeader();
        this.renderCategories();
        this.renderTrending();
        this.renderLatest();
        this.renderSources();
    },
    
    renderHeader() {
        const site = this.data.site;
        document.getElementById('tagline').textContent = `${site.tagline} | ${site.tagline_cn}`;
        document.getElementById('stat-total').textContent = this.data.stats.total_items.toLocaleString();
        document.getElementById('stat-today').textContent = this.data.stats.today_items;
        document.getElementById('stat-time').textContent = this.formatTime(this.data.updated_at);
    },
    
    renderCategories() {
        const grid = document.getElementById('cat-grid');
        const cats = this.data.categories;
        
        grid.innerHTML = Object.entries(cats).map(([key, cat]) => `
            <div class="cat-card" onclick="app.filterByCategory('${key}')">
                <div class="emoji">${cat.emoji}</div>
                <h3>${cat.name}</h3>
                <div class="name-cn">${cat.name_cn}</div>
                <div class="count">${cat.count}</div>
            </div>
        `).join('');
    },
    
    renderTrending() {
        const grid = document.getElementById('trending-grid');
        const trending = this.data.trending || [];
        
        if (trending.length === 0) {
            grid.innerHTML = '<div class="loading">No trending items yet</div>';
            return;
        }
        
        grid.innerHTML = trending.slice(0, 6).map(item => `
            <div class="news-card">
                <div class="category">
                    ${this.getCategoryEmoji(item.category)} ${item.category}
                </div>
                <h4>
                    <a href="${item.link}" target="_blank" rel="noopener">
                        ${this.escapeHtml(item.title)}
                    </a>
                </h4>
                <div class="meta">
                    <span>${item.source}</span>
                    <span class="importance">${'⭐'.repeat(Math.floor(item.importance || 0))}</span>
                </div>
            </div>
        `).join('');
    },
    
    renderLatest() {
        const list = document.getElementById('latest-list');
        const latest = this.data.latest || [];
        
        if (latest.length === 0) {
            list.innerHTML = '<div class="loading">No items yet</div>';
            return;
        }
        
        list.innerHTML = latest.slice(0, 10).map((item, idx) => `
            <div class="news-item">
                <span class="num">${idx + 1}</span>
                <div class="content">
                    <h4>
                        <a href="${item.link}" target="_blank" rel="noopener">
                            ${this.escapeHtml(item.title)}
                        </a>
                    </h4>
                    <div class="meta">
                        ${item.source} · ${this.formatTime(item.time)}
                    </div>
                </div>
                <span class="category-badge">${this.getCategoryEmoji(item.category)}</span>
            </div>
        `).join('');
    },
    
    renderSources() {
        const container = document.getElementById('source-tags');
        const sources = this.data.stats.sources || {};
        
        container.innerHTML = Object.entries(sources)
            .sort((a, b) => b[1] - a[1])
            .map(([name, count]) => `
                <span class="source-tag">
                    ${name}
                    <span class="count">${count}</span>
                </span>
            `).join('');
    },
    
    getCategoryEmoji(cat) {
        const map = { ai: '🤖', robotics: '🦾', space: '🚀' };
        return map[cat] || '📰';
    },
    
    formatTime(isoTime) {
        if (!isoTime) return 'N/A';
        const date = new Date(isoTime);
        const now = new Date();
        const diff = (now - date) / 1000;
        
        if (diff < 60) return 'Just now';
        if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
        if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
        return `${Math.floor(diff / 86400)}d ago`;
    },
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    filterByCategory(cat) {
        // Could implement filtering here
        console.log('Filter by:', cat);
    },
    
    showError() {
        document.body.innerHTML = `
            <div style="text-align: center; padding: 100px 20px; color: #94a3b8;">
                <h2>Failed to load data</h2>
                <p>Please try again later</p>
            </div>
        `;
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => app.init());
