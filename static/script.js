// Функциональность смены языка
document.addEventListener('DOMContentLoaded', function() {
    const languageBtn = document.getElementById('languageBtn');
    const languageDropdown = document.getElementById('languageDropdown');
    const langOptions = document.querySelectorAll('.lang-option');
    const currentLang = document.querySelector('.current-lang');

    // Открытие/закрытие выпадающего меню языка
    if (languageBtn) {
        languageBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const switcher = this.closest('.language-switcher');
            if (switcher) {
                switcher.classList.toggle('active');
            }
        });
    }

    // Закрытие меню при клике вне его
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.language-switcher')) {
            const switcher = document.querySelector('.language-switcher');
            if (switcher) {
                switcher.classList.remove('active');
            }
        }
    });

    // Обработка выбора языка - формы отправляются автоматически
    // НЕ используем preventDefault - позволяем формам отправляться
    // Просто закрываем меню при отправке формы
    if (langOptions.length > 0) {
        langOptions.forEach(option => {
            // Используем событие submit на форме, а не click на кнопке
            const form = option.closest('form');
            if (form) {
                form.addEventListener('submit', function(e) {
                    // НЕ предотвращаем отправку формы
                    // Просто закрываем меню
                    const switcher = this.closest('.language-switcher');
                    if (switcher) {
                        switcher.classList.remove('active');
                    }
                });
            }
        });
    }
});

// Плавная прокрутка для якорных ссылок
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Анимация появления элементов при прокрутке
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Применяем анимацию к карточкам товаров и категорий
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.product-card, .category-card, .feature-item');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

