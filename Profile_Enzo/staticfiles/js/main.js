// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化滚动动画
    initScrollAnimations();
    
    // 初始化作品集筛选功能
    initPortfolioFilter();
    
    // 初始化技能进度条动画
    initSkillProgress();
    
    // 初始化导航栏滚动效果
    initNavbarScroll();
    
    // 初始化平滑滚动
    initSmoothScroll();
    
    // 初始化音乐播放器
    initMusicPlayer();
});

// 滚动动画
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    // 观察所有需要动画的元素
    const animatedElements = document.querySelectorAll('.project-card, .skill-card, .timeline-item, .portfolio-item');
    animatedElements.forEach(el => {
        observer.observe(el);
    });
}

// 作品集筛选功能
function initPortfolioFilter() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    
    if (filterButtons.length === 0 || portfolioItems.length === 0) {
        return;
    }
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 移除所有按钮的active类
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // 添加当前按钮的active类
            this.classList.add('active');
            
            const filterValue = this.getAttribute('data-filter');
            
            // 筛选作品集项目
            portfolioItems.forEach(item => {
                if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                    item.classList.remove('hidden');
                } else {
                    item.classList.add('hidden');
                }
            });
        });
    });
}

// 技能进度条动画
function initSkillProgress() {
    const skillBars = document.querySelectorAll('.skill-progress-bar');
    
    if (skillBars.length === 0) {
        return;
    }
    
    const observerOptions = {
        threshold: 0.5
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const skillBar = entry.target;
                const width = skillBar.getAttribute('data-width');
                skillBar.style.width = width;
            }
        });
    }, observerOptions);
    
    skillBars.forEach(bar => {
        observer.observe(bar);
    });
}

// 导航栏滚动效果
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    if (!navbar) {
        return;
    }
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
            navbar.style.padding = '0.5rem 0';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 1)';
            navbar.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
            navbar.style.padding = '1rem 0';
        }
    });
}

// 平滑滚动
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// 表单验证
function validateContactForm() {
    const form = document.querySelector('form');
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });
    
    // 邮箱验证
    const emailInput = form.querySelector('input[type="email"]');
    if (emailInput && !validateEmail(emailInput.value)) {
        isValid = false;
        emailInput.classList.add('is-invalid');
    }
    
    return isValid;
}

// 邮箱格式验证
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// 项目详情图片点击放大
function initProjectGallery() {
    const galleryImages = document.querySelectorAll('.gallery-item img');
    
    galleryImages.forEach(img => {
        img.addEventListener('click', function() {
            // 这里可以实现图片放大功能
            console.log('Image clicked:', this.src);
        });
    });
}

// 页面加载指示器
window.addEventListener('load', function() {
    const loader = document.querySelector('.loader');
    if (loader) {
        loader.style.display = 'none';
    }
});

// 音乐播放器功能
function initMusicPlayer() {
    const audio = document.getElementById('background-music');
    const toggleButton = document.getElementById('music-toggle');
    const controlIcon = toggleButton.querySelector('.music-control-icon');
    
    if (!audio || !toggleButton || !controlIcon) {
        return;
    }
    
    // 设置初始音量（可选，0.0到1.0之间）
    audio.volume = 0.5;
    
    // 从Session Storage恢复音乐状态
    const isPlaying = sessionStorage.getItem('musicPlaying') === 'true';
    if (isPlaying) {
        // 尝试恢复播放
        audio.play().catch(function(error) {
            console.error('恢复音乐播放失败:', error);
            // 如果播放失败，重置状态
            sessionStorage.setItem('musicPlaying', 'false');
        });
        controlIcon.classList.add('rotating');
    }
    
    // 添加点击事件监听器
    toggleButton.addEventListener('click', function() {
        if (audio.paused) {
            // 播放音乐
            audio.play().catch(function(error) {
                console.error('播放音乐失败:', error);
                console.error('音乐文件路径:', audio.src);
            });
            // 添加旋转类
            controlIcon.classList.add('rotating');
            // 保存播放状态
            sessionStorage.setItem('musicPlaying', 'true');
        } else {
            // 暂停音乐
            audio.pause();
            // 移除旋转类
            controlIcon.classList.remove('rotating');
            // 保存暂停状态
            sessionStorage.setItem('musicPlaying', 'false');
        }
    });
}
