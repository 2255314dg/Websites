/**
 * Video Gallery Interactive Script
 * Handles video card hover effects, modal playback, and gallery interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize video gallery
    initVideoGallery();
});

/**
 * Initialize video gallery functionality
 */
function initVideoGallery() {
    const videoCards = document.querySelectorAll('.video-item');
    const videoModal = document.getElementById('videoModal');
    const modalVideo = document.getElementById('modal-video');
    const modalTitle = document.getElementById('modal-video-title');
    const modalDescription = document.getElementById('modal-video-description');

    // Add hover effects to video cards
    videoCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 12px 24px rgba(0, 0, 0, 0.15)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
        });
    });

    // Add click handlers for play buttons and video cards
    const playButtons = document.querySelectorAll('.play-btn');
    playButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const videoId = this.getAttribute('data-video-id');
            playVideo(videoId, modalVideo, modalTitle, modalDescription, videoModal);
        });
    });

    // Also make entire video card clickable
    const videoGalleryCards = document.querySelectorAll('.video-card');
    videoGalleryCards.forEach(card => {
        card.addEventListener('click', function() {
            const videoId = this.getAttribute('data-video-id');
            const playBtn = this.querySelector('.play-btn');
            if (playBtn) {
                playBtn.click();
            }
        });
    });

    // Handle modal cleanup when closed
    if (videoModal) {
        videoModal.addEventListener('hidden.bs.modal', function() {
            if (modalVideo) {
                modalVideo.pause();
                modalVideo.src = '';
            }
        });
    }

    // Fade-in animation for gallery cards
    animateGalleryCards();
}

/**
 * Play video in modal
 * @param {string} videoId - The video database ID
 * @param {HTMLVideoElement} modalVideo - Modal video element
 * @param {HTMLElement} modalTitle - Modal title element
 * @param {HTMLElement} modalDescription - Modal description element
 * @param {HTMLElement} videoModal - Bootstrap modal element
 */
function playVideo(videoId, modalVideo, modalTitle, modalDescription, videoModal) {
    // Find the video card to get video data
    const videoCard = document.querySelector(`[data-video-id="${videoId}"]`);
    if (!videoCard) return;

    // Extract video data from card
    const titleElement = videoCard.querySelector('.card-title');
    const descElement = videoCard.querySelector('.card-text');
    const title = titleElement ? titleElement.textContent : '视频';
    const description = descElement ? descElement.textContent : '';

    // Get video source from data attribute (set by Django template)
    const videoSrc = videoCard.getAttribute('data-video-src');

    // Set modal content
    if (modalVideo && videoSrc) {
        modalVideo.src = videoSrc;
    }
    
    if (modalTitle) {
        modalTitle.textContent = title;
    }
    
    if (modalDescription) {
        modalDescription.textContent = description;
    }

    // Show modal
    if (videoModal) {
        const bsModal = new bootstrap.Modal(videoModal);
        bsModal.show();

        // Auto-play video when modal is shown
        videoModal.addEventListener('shown.bs.modal', function() {
            if (modalVideo) {
                modalVideo.play().catch(error => {
                    console.log('Auto-play prevented:', error);
                });
            }
        }, { once: true });
    }
}

/**
 * Animate gallery cards on page load
 */
function animateGalleryCards() {
    const gallery = document.getElementById('video-gallery');
    if (!gallery) return;

    const cards = gallery.querySelectorAll('.video-card');
    cards.forEach((card, index) => {
        // Initial state
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';

        // Staggered animation
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

/**
 * Format duration seconds to MM:SS format
 * @param {number} seconds - Duration in seconds
 * @returns {string} Formatted duration
 */
function formatDuration(seconds) {
    if (!seconds) return '';
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}m ${secs.toString().padStart(2, '0')}s`;
}

/**
 * Handle video file upload preview (for admin use)
 * @param {File} file - Video file to preview
 */
function previewVideoFile(file) {
    if (!file || !file.type.startsWith('video/')) {
        console.warn('Not a valid video file');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        // Optionally generate thumbnail or display preview
        console.log('Video file loaded:', file.name);
    };
    reader.readAsArrayBuffer(file);
}
