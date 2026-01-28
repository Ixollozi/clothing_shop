"""
Модуль для отправки уведомлений в Telegram через бота
"""
import telebot
from django.conf import settings
from django.utils.html import escape
from .models import TelegramConfig, Order
import logging

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Класс для отправки уведомлений в Telegram"""
    
    def __init__(self):
        self._bot = None
        self._config = None
    
    def _get_config(self):
        """Получает актуальную конфигурацию"""
        return TelegramConfig.get_active_config()
    
    def _get_bot(self):
        """Получает или создает экземпляр бота"""
        config = self._get_config()
        if not config or not config.is_active or not config.bot_token:
            if not config:
                logger.debug("Конфигурация Telegram не найдена")
            elif not config.is_active:
                logger.debug("Telegram уведомления отключены")
            elif not config.bot_token:
                logger.debug("Токен бота не указан")
            return None
        
        # Всегда пересоздаем бота для актуальной конфигурации
        try:
            logger.debug(f"Инициализация Telegram бота (token: {config.bot_token[:10]}...)")
            self._bot = telebot.TeleBot(config.bot_token)
            self._config = config
            # Проверяем, что бот работает
            bot_info = self._bot.get_me()
            logger.info(f"Telegram бот инициализирован: @{bot_info.username}")
            return self._bot
        except Exception as e:
            logger.error(f"Ошибка инициализации Telegram бота: {e}", exc_info=True)
            self._bot = None
            self._config = None
            return None
    
    def _send_message(self, message, parse_mode='HTML'):
        """Отправляет сообщение в группу"""
        bot = self._get_bot()
        config = self._get_config()
        
        if not bot:
            logger.error("Бот не инициализирован")
            return False
        
        if not config:
            logger.error("Конфигурация не найдена")
            return False
        
        if not config.group_chat_id:
            logger.error("ID группы не указан")
            return False
        
        try:
            logger.debug(f"Попытка отправить сообщение в Telegram (chat_id: {config.group_chat_id})")
            bot.send_message(
                chat_id=config.group_chat_id,
                text=message,
                parse_mode=parse_mode
            )
            logger.info("Сообщение успешно отправлено в Telegram")
            return True
        except telebot.apihelper.ApiTelegramException as e:
            logger.error(f"Ошибка API Telegram при отправке сообщения: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Неожиданная ошибка при отправке в Telegram: {e}", exc_info=True)
            return False
    
    def notify_new_order(self, order):
        """Отправляет уведомление о новом заказе"""
        config = self._get_config()
        if not config:
            logger.warning("TelegramConfig не найдена или не активна")
            return False
        
        if not config.is_active:
            logger.warning("Telegram уведомления отключены (is_active=False)")
            return False
        
        if not config.notify_new_orders:
            logger.info("Уведомления о новых заказах отключены")
            return False
        
        if not config.bot_token:
            logger.warning("Токен бота не указан")
            return False
        
        if not config.group_chat_id:
            logger.warning("ID группы не указан")
            return False
        
        try:
            # Экранируем данные для безопасного использования в HTML
            first_name = escape(str(order.first_name))
            last_name = escape(str(order.last_name))
            phone = escape(str(order.phone))
            city = escape(str(order.city))
            address = escape(str(order.address))
            postal_code = escape(str(order.postal_code)) if order.postal_code else ''
            notes = escape(str(order.notes)) if order.notes else ''
            
            # Формируем сообщение о новом заказе
            message = f"""🛒 <b>НОВЫЙ ЗАКАЗ #{order.id}</b>

👤 <b>Клиент:</b>
• Имя: {first_name} {last_name}
• Телефон: {phone}

📍 <b>Адрес доставки:</b>
• Город: {city}
• Адрес: {address}
{f'• Индекс: {postal_code}' if postal_code else ''}

📦 <b>Товары:</b>
"""
            
            # Добавляем информацию о товарах
            for item in order.items.all():
                product_name = escape(str(item.product.name))
                size = escape(str(item.size)) if item.size else ''
                color = escape(str(item.color)) if item.color else ''
                message += f"• {product_name} x{item.quantity}\n"
                if size:
                    message += f"  Размер: {size}\n"
                if color:
                    message += f"  Цвет: {color}\n"
                message += f"  Цена: {item.price:,.0f} сум\n\n"
            
            message += f"\n💰 <b>Итого: {order.total:,.0f} сум</b>"
            
            if notes:
                message += f"\n\n📝 <b>Примечания:</b>\n{notes}"
            
            message += f"\n\n⏰ {order.created_at.strftime('%d.%m.%Y %H:%M')}"
            
            logger.info(f"Отправка уведомления о заказе #{order.id} в Telegram")
            result = self._send_message(message)
            if result:
                logger.info(f"Уведомление о заказе #{order.id} успешно отправлено в Telegram")
            else:
                logger.error(f"Не удалось отправить уведомление о заказе #{order.id} в Telegram")
            return result
        except Exception as e:
            logger.error(f"Ошибка формирования уведомления о новом заказе #{order.id}: {e}", exc_info=True)
            return False
    
    def notify_status_change(self, order, old_status=None):
        """Отправляет уведомление об изменении статуса заказа"""
        config = self._get_config()
        if not config or not config.notify_status_changes:
            return False
        
        try:
            # Эмодзи для разных статусов
            status_emojis = {
                'pending': '⏳',
                'processing': '🔄',
                'shipped': '📦',
                'delivered': '✅',
                'cancelled': '❌',
            }
            
            emoji = status_emojis.get(order.status, '📋')
            
            # Экранируем данные для безопасного использования в HTML
            first_name = escape(str(order.first_name))
            last_name = escape(str(order.last_name))
            phone = escape(str(order.phone))
            status_display = escape(str(order.get_status_display()))
            
            message = f"""{emoji} <b>ИЗМЕНЕНИЕ СТАТУСА ЗАКАЗА #{order.id}</b>

👤 <b>Клиент:</b> {first_name} {last_name}
📞 <b>Телефон:</b> {phone}

<b>Статус:</b> {status_display}
"""
            
            if old_status and old_status != order.status:
                old_status_display = escape(str(dict(Order.STATUS_CHOICES).get(old_status, old_status)))
                message += f"<b>Предыдущий статус:</b> {old_status_display}\n"
            
            message += f"\n💰 <b>Сумма:</b> {order.total:,.0f} сум"
            message += f"\n⏰ {order.updated_at.strftime('%d.%m.%Y %H:%M')}"
            
            return self._send_message(message)
        except Exception as e:
            logger.error(f"Ошибка формирования уведомления об изменении статуса: {e}")
            return False
    
    def notify_contact_message(self, contact_message):
        """Отправляет уведомление о новом сообщении из формы контактов"""
        config = self._get_config()
        if not config or not config.notify_contact_messages:
            return False
        
        try:
            # Экранируем данные для безопасного использования в HTML
            name = escape(str(contact_message.name))
            email = escape(str(contact_message.email))
            phone = escape(str(contact_message.phone)) if contact_message.phone else 'Не указан'
            subject = escape(str(contact_message.get_subject_display()))
            message = escape(str(contact_message.message))
            
            # Формируем сообщение
            telegram_message = f"""📧 <b>НОВОЕ СООБЩЕНИЕ ИЗ КОНТАКТОВ</b>

👤 <b>От:</b> {name}
📧 <b>Email:</b> {email}
📞 <b>Телефон:</b> {phone}

📋 <b>Тема:</b> {subject}

💬 <b>Сообщение:</b>
{message}

⏰ {contact_message.created_at.strftime('%d.%m.%Y %H:%M')}"""
            
            return self._send_message(telegram_message)
        except Exception as e:
            logger.error(f"Ошибка формирования уведомления о сообщении из контактов: {e}")
            return False


# Глобальный экземпляр для использования в проекте
telegram_notifier = TelegramNotifier()
