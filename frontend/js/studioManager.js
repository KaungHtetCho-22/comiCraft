/**
 * StudioManager - Handles custom characters and art styles
 */

class StudioManager {
    constructor() {
        this.charactersKey = 'comiccraft_studio_characters';
        this.stylesKey = 'comiccraft_studio_styles';
        this.currentTab = 'characters'; // 'characters' or 'styles'
        
        this.initElements();
    }

    initElements() {
        this.modal = document.getElementById('studio-modal');
        this.listView = document.getElementById('studio-list-view');
        this.formView = document.getElementById('studio-form-view');
        this.grid = document.getElementById('studio-items-grid');
        
        this.idInput = document.getElementById('studio-item-id');
        this.nameInput = document.getElementById('studio-item-name');
        this.descInput = document.getElementById('studio-item-desc');
        this.imagePreview = document.getElementById('studio-item-image-preview');
        this.imagePlaceholder = document.getElementById('studio-image-placeholder');
        this.generateBtn = document.getElementById('studio-generate-btn');
    }

    // Data Access
    getItems(type) {
        const key = type === 'characters' ? this.charactersKey : this.stylesKey;
        const data = localStorage.getItem(key);
        const items = data ? JSON.parse(data) : [];
        return items.map((item) => ({
            ...item,
            active: item.active !== false
        }));
    }

    getActiveItems(type) {
        return this.getItems(type).filter((item) => item.active !== false);
    }

    saveItems(type, items) {
        const key = type === 'characters' ? this.charactersKey : this.stylesKey;
        localStorage.setItem(key, JSON.stringify(items));
    }

    updateImageState(imageSrc = '') {
        if (imageSrc) {
            this.imagePreview.src = imageSrc;
            this.imagePreview.style.display = 'block';
            if (this.imagePlaceholder) this.imagePlaceholder.style.display = 'none';
            return;
        }

        this.imagePreview.src = '';
        this.imagePreview.style.display = 'none';
        if (this.imagePlaceholder) this.imagePlaceholder.style.display = 'flex';
    }

    async readFileAsDataUrl(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = () => reject(new Error('Failed to read the selected file.'));
            reader.readAsDataURL(file);
        });
    }

    async compressImage(imageSrc, options = {}) {
        const {
            maxWidth = 640,
            maxHeight = 640,
            quality = 0.82,
            mimeType = 'image/webp'
        } = options;

        if (!imageSrc) return '';
        if (!imageSrc.startsWith('data:')) return imageSrc;

        const img = await new Promise((resolve, reject) => {
            const image = new Image();
            image.onload = () => resolve(image);
            image.onerror = () => reject(new Error('Failed to process image.'));
            image.src = imageSrc;
        });

        let { width, height } = img;
        const scale = Math.min(maxWidth / width, maxHeight / height, 1);
        width = Math.max(1, Math.round(width * scale));
        height = Math.max(1, Math.round(height * scale));

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;

        const ctx = canvas.getContext('2d');
        if (!ctx) throw new Error('Failed to prepare image for storage.');
        ctx.drawImage(img, 0, 0, width, height);

        return canvas.toDataURL(mimeType, quality);
    }

    async compactItemsForStorage(items, level = 0) {
        const presets = [
            { maxWidth: 640, maxHeight: 640, quality: 0.82 },
            { maxWidth: 512, maxHeight: 512, quality: 0.72 },
            { maxWidth: 384, maxHeight: 384, quality: 0.62 }
        ];
        const preset = presets[Math.min(level, presets.length - 1)];

        return Promise.all(items.map(async (item) => {
            if (!item.image || !item.image.startsWith('data:')) return item;
            return {
                ...item,
                image: await this.compressImage(item.image, preset)
            };
        }));
    }

    async persistItems(type, items) {
        try {
            this.saveItems(type, items);
            return items;
        } catch (error) {
            if (error.name !== 'QuotaExceededError') throw error;
        }

        for (let level = 1; level <= 2; level += 1) {
            const compacted = await this.compactItemsForStorage(items, level);
            try {
                this.saveItems(type, compacted);
                return compacted;
            } catch (error) {
                if (error.name !== 'QuotaExceededError') throw error;
            }
        }

        throw new Error('Studio storage is full. Delete a few saved items or use smaller images.');
    }

    // UI Logic
    open() {
        this.modal.style.display = 'flex';
        this.renderList();
    }

    close() {
        this.modal.style.display = 'none';
    }

    switchTab(tab) {
        this.currentTab = tab;
        
        // Update tab buttons visually
        document.querySelectorAll('.studio-tab').forEach(btn => {
            btn.classList.remove('active');
            if (btn.innerText.toLowerCase().includes(tab.replace('s', ''))) { // Simple match 'Character' or 'Style'
                btn.classList.add('active');
            }
        });
        
        this.hideForm();
        this.renderList();
    }

    showForm(id = null) {
        this.listView.style.display = 'none';
        this.formView.style.display = 'block';
        
        if (id) {
            // Edit mode
            const items = this.getItems(this.currentTab);
            const item = items.find(i => i.id === id);
            if (item) {
                this.idInput.value = item.id;
                this.nameInput.value = item.name;
                this.descInput.value = item.description;
                this.updateImageState(item.image || '');
            }
        } else {
            // Add mode
            this.idInput.value = '';
            this.nameInput.value = '';
            this.descInput.value = '';
            this.updateImageState('');
        }
    }

    hideForm() {
        this.listView.style.display = 'block';
        this.formView.style.display = 'none';
    }

    renderList() {
        const items = this.getItems(this.currentTab);
        this.grid.innerHTML = '';
        
        if (items.length === 0) {
            this.grid.innerHTML = `<div class="studio-empty">No ${this.currentTab} added yet. Click "+ Add New" to create one!</div>`;
            return;
        }
        
        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'studio-card';
            if (!item.active) card.classList.add('inactive');
            
            const img = document.createElement('img');
            img.src = item.image || 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="%23eee"/><text x="50" y="50" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="12" fill="%23aaa">No Image</text></svg>';
            
            const info = document.createElement('div');
            info.className = 'studio-card-info';
            const typeLabel = this.currentTab === 'characters' ? 'Character reference' : 'Art style reference';
            const statusBadge = item.active
                ? `<span class="studio-consistency-badge">&#10003; LOCKED IN</span>`
                : `<span style="font-size:11px;color:var(--text-tertiary);font-weight:700;">Inactive</span>`;
            info.innerHTML = `<strong>${item.name}</strong><div style="font-size:11px;color:var(--text-tertiary);margin:2px 0;">${typeLabel}</div><div style="margin-top:4px;">${statusBadge}</div>`;
            
            const actions = document.createElement('div');
            actions.className = 'studio-card-actions';

            const toggleBtn = document.createElement('button');
            toggleBtn.className = `studio-toggle-btn ${item.active ? 'is-active' : ''}`;
            toggleBtn.textContent = item.active ? 'ON' : 'OFF';
            toggleBtn.title = item.active ? 'Disable this item' : 'Enable this item';
            toggleBtn.onclick = async (e) => {
                e.stopPropagation();
                await this.toggleItemActive(item.id);
            };
            
            const editBtn = document.createElement('button');
            editBtn.innerHTML = '✏️';
            editBtn.onclick = (e) => { e.stopPropagation(); this.showForm(item.id); };
            
            const deleteBtn = document.createElement('button');
            deleteBtn.innerHTML = '🗑️';
            deleteBtn.className = 'delete';
            deleteBtn.onclick = (e) => { 
                e.stopPropagation(); 
                if (confirm(`Delete ${item.name}?`)) {
                    this.deleteItem(item.id);
                } 
            };
            
            actions.appendChild(toggleBtn);
            actions.appendChild(editBtn);
            actions.appendChild(deleteBtn);
            
            card.appendChild(img);
            card.appendChild(info);
            card.appendChild(actions);
            
            this.grid.appendChild(card);
        });
    }

    handleImageUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        if (file.size > 5 * 1024 * 1024) {
            alert('File is too large. Limit is 5MB.');
            return;
        }
        
        this.readFileAsDataUrl(file)
            .then((result) => this.compressImage(result, { maxWidth: 640, maxHeight: 640, quality: 0.82 }))
            .then((compressed) => this.updateImageState(compressed))
            .catch((error) => {
                console.error('Image upload failed:', error);
                alert(error.message || 'Failed to read the selected image.');
            });
        event.target.value = '';
    }

    async generateImage() {
        const desc = this.descInput.value.trim();
        const googleApiKeyInput = document.getElementById('google-api-key');
        const googleApiKey = googleApiKeyInput ? googleApiKeyInput.value.trim() : '';
        
        if (!desc) {
            alert('Please enter a Visual Description first to generate an image.');
            return;
        }
        if (!googleApiKey) {
            alert('Please configure your Gemini API Key in the config panel first.');
            return;
        }
        
        const originalText = this.generateBtn.innerText;
        this.generateBtn.disabled = true;
        this.generateBtn.innerText = 'Generating...';
        
        const imageBase64 = this.imagePreview.src && this.imagePreview.src.startsWith('data:') ? this.imagePreview.src : null;

        // Use the currently selected comic style so the reference image matches the storyboard
        const comicStyleSelect = document.getElementById('comic-style');
        const comicStyle = (comicStyleSelect && comicStyleSelect.value) ? comicStyleSelect.value : 'doraemon';
        const itemName = this.nameInput.value.trim() || 'Reference';

        try {
            // Craft a style-matched reference prompt
            let prompt;
            if (this.currentTab === 'characters') {
                prompt = `CHARACTER MODEL SHEET for "${itemName}" drawn in ${comicStyle} comic art style.
Visual description: ${desc}
Draw the character in a clean front-facing pose against a plain light background.
Use the exact art style of ${comicStyle} comics — same linework, body proportions, and coloring.
No panels, no speech bubbles, no background scenery, no text labels. One clear full-body character view only.`;
            } else {
                prompt = `ART STYLE SAMPLE for "${itemName}".
Style description: ${desc}
Create a single illustrative scene (no character dialogue) that clearly demonstrates this art style's color palette, line weight, atmosphere, and environment, drawn in ${comicStyle} style.
Make it immediately recognisable as a visual reference for this comic art style.`;
            }

            // We fake a page_data to use the existing image-generation backend
            const fakePageData = {
                title: itemName,
                rows: [{ panels: [{ text: prompt }] }]
            };

            // Pass the currently uploaded base64 image (if any) as referenceImg
            const result = await ComicAPI.generateComicImage(
                fakePageData,
                googleApiKey,
                imageBase64 ? [imageBase64] : null,
                null,
                comicStyle,
                null,
                'en'
            );
            
            if (result && result.image_url) {
                try {
                    // Try to fetch the generated image to convert it into base64 for localstorage
                    let fullUrl = result.image_url;
                    if (!fullUrl.startsWith('http')) {
                        // Ensure it has a leading slash
                        fullUrl = window.location.protocol + "//" + window.location.host + (fullUrl.startsWith('/') ? '' : '/') + fullUrl;
                    }
                    
                    const response = await fetch(fullUrl);
                    const blob = await response.blob();
                    const base64Image = await this.readFileAsDataUrl(blob);
                    const compressed = await this.compressImage(base64Image, { maxWidth: 640, maxHeight: 640, quality: 0.8 });
                    this.updateImageState(compressed);
                } catch (err) {
                    console.error('Failed to convert generated image to base64', err);
                    this.updateImageState(result.image_url);
                }
            } else {
                throw new Error("No image URL returned");
            }
            
        } catch (error) {
            console.error('Generation failed:', error);
            alert('Generation failed: ' + error.message);
        } finally {
            this.generateBtn.disabled = false;
            this.generateBtn.innerText = originalText;
        }
    }

    async saveItem() {
        const name = this.nameInput.value.trim();
        const desc = this.descInput.value.trim();
        const id = this.idInput.value || Date.now().toString();
        const image = this.imagePreview.src;
        
        if (!name || !desc) {
            alert('Name and Description are required.');
            return;
        }
        
        if (!image || image === window.location.href) {
            alert('Please upload or generate an reference image.');
            return;
        }
        
        try {
            const items = this.getItems(this.currentTab);
            const existingIdx = items.findIndex(i => i.id === id);
            const preparedImage = await this.compressImage(image, { maxWidth: 640, maxHeight: 640, quality: 0.82 });
            const existingItem = existingIdx >= 0 ? items[existingIdx] : null;
            const newItem = { id, name, description: desc, image: preparedImage, active: existingItem ? existingItem.active !== false : true };

            if (existingIdx >= 0) {
                items[existingIdx] = newItem;
            } else {
                items.push(newItem);
            }

            await this.persistItems(this.currentTab, items);
            this.hideForm();
            this.renderList();
            if (typeof updatePromptHighlights === 'function') updatePromptHighlights();
        } catch (error) {
            console.error('Failed to save studio item:', error);
            alert(error.message || 'Failed to save this studio item.');
        }
    }
    
    deleteItem(id) {
        let items = this.getItems(this.currentTab);
        items = items.filter(i => i.id !== id);
        this.saveItems(this.currentTab, items);
        this.renderList();
        if (typeof updatePromptHighlights === 'function') updatePromptHighlights();
    }

    async toggleItemActive(id) {
        const items = this.getItems(this.currentTab);
        const updatedItems = items.map((item) => (
            item.id === id ? { ...item, active: item.active === false } : item
        ));

        try {
            await this.persistItems(this.currentTab, updatedItems);
            this.renderList();
            if (typeof updatePromptHighlights === 'function') updatePromptHighlights();
        } catch (error) {
            console.error('Failed to toggle studio item:', error);
            alert(error.message || 'Failed to update this studio item.');
        }
    }
}
