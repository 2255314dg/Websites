/**
 * 作品集页面交互脚本
 * 功能：分页导航、分类筛选、项目卡片动画
 */

document.addEventListener('DOMContentLoaded', function() {
    // ========== 分页相关 ==========
    const paginationLinks = document.querySelectorAll('.pagination a');
    
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // 禁用默认行为，改为平滑过渡
            const href = this.getAttribute('href');
            if (href && !this.parentElement.classList.contains('disabled')) {
                window.scrollTo({ top: 0, behavior: 'smooth' });
                setTimeout(() => {
                    window.location.href = href;
                }, 300);
                e.preventDefault();
            }
        });
    });

    // ========== 分类筛选按钮 ==========
    const categoryLinks = document.querySelectorAll('.filters-section a');
    
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // 平滑滚动并动画过渡
            window.scrollTo({ top: 0, behavior: 'smooth' });
            setTimeout(() => {
                window.location.href = this.getAttribute('href');
            }, 300);
            e.preventDefault();
        });
    });

    // ========== 项目卡片淡入动画 ==========
    const projectItems = document.querySelectorAll('.project-item');
    
    projectItems.forEach((item, index) => {
        // 初始状态：透明且向下偏移
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        // 延迟动画，逐个淡入
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 50);
    });

    // ========== 卡片悬停效果 ==========
    projectItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
            // 添加阴影效果
            const card = this.querySelector('.card');
            if (card) {
                card.style.boxShadow = '0 8px 16px rgba(0,0,0,0.15)';
                card.style.transition = 'box-shadow 0.3s ease';
            }
        });

        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            const card = this.querySelector('.card');
            if (card) {
                card.style.boxShadow = '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)';
            }
        });
    });

    // ========== 图片加载完成时的动画 ==========
    const projectImages = document.querySelectorAll('.card-img-top');
    
    projectImages.forEach(img => {
        if (img.complete) {
            // 如果图片已加载（缓存）
            img.style.animation = 'fadeIn 0.6s ease-in';
        } else {
            // 等待图片加载完成后动画
            img.addEventListener('load', function() {
                this.style.animation = 'fadeIn 0.6s ease-in';
            });
        }

        // 图片加载失败时显示占位符处理
        img.addEventListener('error', function() {
            this.style.display = 'none';
            const placeholder = document.createElement('div');
            placeholder.className = 'bg-secondary text-white d-flex align-items-center justify-content-center';
            placeholder.style.height = '250px';
            placeholder.innerHTML = '<p class="mb-0">图片加载失败</p>';
            this.parentElement.insertBefore(placeholder, this);
        });
    });

    // ========== 按钮状态同步 ==========
    // 确保当前分类按钮有正确的样式（由服务器端渲染，这里作为备用）
    const urlParams = new URLSearchParams(window.location.search);
    const currentCategory = urlParams.get('category') || 'all';
    
    categoryLinks.forEach(link => {
        const linkCategory = new URLSearchParams(new URL(link.href, window.location).search).get('category') || 'all';
        if (linkCategory === currentCategory) {
            link.classList.add('active', 'btn-primary');
            link.classList.remove('btn-outline-primary');
        }
    });
});

// ========== 全局 CSS 动画定义 ==========
// 创建样式表并注入
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    .project-item {
        transition: transform 0.3s ease, opacity 0.5s ease;
    }

    .project-item .card {
        transition: box-shadow 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }

    .pagination a {
        cursor: pointer;
    }

    .filters-section a {
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .filters-section a:hover {
        transform: scale(1.05);
    }
`;
document.head.appendChild(style);
