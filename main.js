// TPMS - Main JavaScript File

// Initialize animations when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeCharts();
    initializeCalendar();
});

// Animation initialization
function initializeAnimations() {
    // Animate stats cards
    anime({
        targets: '.slide-in',
        translateY: [30, 0],
        opacity: [0, 1],
        delay: anime.stagger(100),
        duration: 600,
        easing: 'easeOutQuart'
    });

    // Hover effects for cards
    const hoverElements = document.querySelectorAll('.hover-lift');
    hoverElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            anime({
                targets: this,
                translateY: -5,
                duration: 300,
                easing: 'easeOutQuart'
            });
        });

        element.addEventListener('mouseleave', function() {
            anime({
                targets: this,
                translateY: 0,
                duration: 300,
                easing: 'easeOutQuart'
            });
        });
    });
}

// Chart initialization
function initializeCharts() {
    const chartElement = document.getElementById('publicationChart');
    if (!chartElement) return;

    const chart = echarts.init(chartElement);
    
    const option = {
        tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            borderColor: '#e5e7eb',
            borderWidth: 1,
            textStyle: {
                color: '#374151'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['11.06', '12.06', '13.06', '14.06', '15.06', '16.06', '17.06'],
            axisLine: {
                lineStyle: {
                    color: '#e5e7eb'
                }
            },
            axisLabel: {
                color: '#6b7280'
            }
        },
        yAxis: {
            type: 'value',
            axisLine: {
                lineStyle: {
                    color: '#e5e7eb'
                }
            },
            axisLabel: {
                color: '#6b7280'
            },
            splitLine: {
                lineStyle: {
                    color: '#f3f4f6'
                }
            }
        },
        series: [
            {
                name: 'Опубликовано',
                type: 'line',
                smooth: true,
                data: [45, 52, 38, 67, 73, 89, 95],
                lineStyle: {
                    color: '#3b82f6',
                    width: 3
                },
                areaStyle: {
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [
                            { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
                            { offset: 1, color: 'rgba(59, 130, 246, 0.05)' }
                        ]
                    }
                },
                itemStyle: {
                    color: '#3b82f6'
                }
            },
            {
                name: 'Запланировано',
                type: 'line',
                smooth: true,
                data: [32, 41, 45, 52, 48, 56, 62],
                lineStyle: {
                    color: '#8b5cf6',
                    width: 3
                },
                itemStyle: {
                    color: '#8b5cf6'
                }
            }
        ]
    };

    chart.setOption(option);

    // Make chart responsive
    window.addEventListener('resize', function() {
        chart.resize();
    });
}

// Calendar initialization
function initializeCalendar() {
    const calendarDays = document.querySelectorAll('.calendar-day');
    
    calendarDays.forEach(day => {
        if (day.textContent.trim()) {
            day.addEventListener('click', function() {
                // Remove active class from all days
                calendarDays.forEach(d => d.classList.remove('bg-blue-100'));
                // Add active class to clicked day
                this.classList.add('bg-blue-100');
                
                // Show posts for this day
                showDayPosts(this.textContent.trim());
            });
        }
    });
}

// Modal functions
function showModal(type) {
    const modal = document.getElementById('modal');
    const modalContent = document.getElementById('modalContent');
    
    let content = '';
    
    switch(type) {
        case 'newPost':
            content = `
                <div class="flex items-center justify-between mb-6">
                    <h3 class="text-2xl font-bold text-gray-900">Создать новый пост</h3>
                    <button onclick="closeModal()" class="text-gray-400 hover:text-gray-600">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
                <form class="space-y-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Канал</label>
                        <select class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                            <option>Выберите канал</option>
                            <option>Tech News</option>
                            <option>Бизнес</option>
                            <option>Маркетинг</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Текст поста</label>
                        <textarea rows="6" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="Введите текст поста..."></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Форматирование</label>
                        <div class="flex space-x-4">
                            <label class="flex items-center">
                                <input type="radio" name="format" value="markdown" class="mr-2" checked>
                                <span class="text-sm">Markdown</span>
                            </label>
                            <label class="flex items-center">
                                <input type="radio" name="format" value="html" class="mr-2">
                                <span class="text-sm">HTML</span>
                            </label>
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Медиа</label>
                        <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                            <i class="fas fa-cloud-upload-alt text-gray-400 text-2xl mb-2"></i>
                            <p class="text-sm text-gray-600">Перетащите файлы сюда или нажмите для выбора</p>
                            <p class="text-xs text-gray-500 mt-1">Максимум 10 МБ для изображений, 50 МБ для видео</p>
                        </div>
                    </div>
                    <div class="flex justify-end space-x-4">
                        <button type="button" onclick="closeModal()" class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
                            Отмена
                        </button>
                        <button type="submit" class="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all">
                            Создать пост
                        </button>
                    </div>
                </form>
            `;
            break;
            
        case 'schedulePost':
            content = `
                <div class="flex items-center justify-between mb-6">
                    <h3 class="text-2xl font-bold text-gray-900">Запланировать публикацию</h3>
                    <button onclick="closeModal()" class="text-gray-400 hover:text-gray-600">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
                <form class="space-y-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Выберите пост</label>
                        <select class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                            <option>Новости технологий</option>
                            <option>Советы по маркетингу</option>
                            <option>Финансовый обзор</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Дата и время</label>
                        <div class="grid grid-cols-2 gap-4">
                            <input type="date" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                            <input type="time" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Настройки публикации</label>
                        <div class="space-y-3">
                            <label class="flex items-center">
                                <input type="checkbox" class="mr-3" checked>
                                <span class="text-sm">Отправить уведомление подписчикам</span>
                            </label>
                            <label class="flex items-center">
                                <input type="checkbox" class="mr-3">
                                <span class="text-sm">Защитить контент от копирования</span>
                            </label>
                            <label class="flex items-center">
                                <input type="checkbox" class="mr-3">
                                <span class="text-sm">Добавить спойлер</span>
                            </label>
                        </div>
                    </div>
                    <div class="flex justify-end space-x-4">
                        <button type="button" onclick="closeModal()" class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
                            Отмена
                        </button>
                        <button type="submit" class="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg hover:shadow-lg transition-all">
                            Запланировать
                        </button>
                    </div>
                </form>
            `;
            break;
            
        case 'addChannel':
            content = `
                <div class="flex items-center justify-between mb-6">
                    <h3 class="text-2xl font-bold text-gray-900">Добавить канал</h3>
                    <button onclick="closeModal()" class="text-gray-400 hover:text-gray-600">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
                <form class="space-y-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Способ добавления</label>
                        <div class="flex space-x-4">
                            <label class="flex items-center">
                                <input type="radio" name="method" value="username" class="mr-2" checked>
                                <span class="text-sm">По @username</span>
                            </label>
                            <label class="flex items-center">
                                <input type="radio" name="method" value="link" class="mr-2">
                                <span class="text-sm">По ссылке</span>
                            </label>
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">@username или ссылка</label>
                        <input type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="@channel_username или https://t.me/...">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Токен бота</label>
                        <input type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="Введите токен вашего Telegram-бота">
                        <p class="text-xs text-gray-500 mt-1">Токен будет зашифрован и безопасно сохранен</p>
                    </div>
                    <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <div class="flex items-start space-x-3">
                            <i class="fas fa-info-circle text-blue-600 mt-0.5"></i>
                            <div class="text-sm text-blue-800">
                                <p class="font-medium mb-1">Инструкция:</p>
                                <ul class="space-y-1 text-xs">
                                    <li>• Добавьте вашего бота в канал как администратора</li>
                                    <li>• Убедитесь, что у бота есть права на отправку сообщений</li>
                                    <li>• Система автоматически проверит права доступа</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="flex justify-end space-x-4">
                        <button type="button" onclick="closeModal()" class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
                            Отмена
                        </button>
                        <button type="submit" class="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all">
                            Добавить канал
                        </button>
                    </div>
                </form>
            `;
            break;
    }
    
    modalContent.innerHTML = content;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    
    // Animate modal appearance
    anime({
        targets: modal.querySelector('.bg-white'),
        scale: [0.8, 1],
        opacity: [0, 1],
        duration: 300,
        easing: 'easeOutQuart'
    });
}

function closeModal() {
    const modal = document.getElementById('modal');
    
    anime({
        targets: modal.querySelector('.bg-white'),
        scale: [1, 0.8],
        opacity: [1, 0],
        duration: 200,
        easing: 'easeInQuart',
        complete: function() {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
    });
}

function showDayPosts(day) {
    // This function would show posts for a specific day
    console.log(`Showing posts for day ${day}`);
    // In a real application, this would fetch and display posts for the selected day
}

// Close modal when clicking outside
document.addEventListener('click', function(e) {
    const modal = document.getElementById('modal');
    if (e.target === modal) {
        closeModal();
    }
});

// Form submission handlers
document.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Show success message
    const modalContent = document.getElementById('modalContent');
    const successMessage = `
        <div class="text-center py-8">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <i class="fas fa-check text-green-600 text-2xl"></i>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Успешно!</h3>
            <p class="text-gray-600 mb-6">Действие выполнено успешно</p>
            <button onclick="closeModal()" class="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all">
                Закрыть
            </button>
        </div>
    `;
    
    modalContent.innerHTML = successMessage;
    
    // Auto-close after 2 seconds
    setTimeout(() => {
        closeModal();
    }, 2000);
});

// Utility functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg ${
        type === 'success' ? 'bg-green-500 text-white' : 
        type === 'error' ? 'bg-red-500 text-white' : 
        'bg-blue-500 text-white'
    }`;
    notification.innerHTML = `
        <div class="flex items-center space-x-3">
            <i class="fas ${
                type === 'success' ? 'fa-check' : 
                type === 'error' ? 'fa-exclamation' : 
                'fa-info'
            }"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    anime({
        targets: notification,
        translateX: [300, 0],
        opacity: [0, 1],
        duration: 300,
        easing: 'easeOutQuart'
    });
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        anime({
            targets: notification,
            translateX: [0, 300],
            opacity: [1, 0],
            duration: 300,
            easing: 'easeInQuart',
            complete: () => {
                document.body.removeChild(notification);
            }
        });
    }, 3000);
}