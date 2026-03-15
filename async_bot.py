import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import re
from urllib.parse import quote

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Токен бота (должен быть в переменных окружения Bothost)
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# База готовых конспектов
notes = {
    'ньютон': '''📚 **Конспект: Законы Ньютона**

🔹 **Первый закон** (Закон инерции)
Тело сохраняет состояние покоя или равномерного движения, если на него не действуют силы.

🔹 **Второй закон**
F = m·a
(Сила = масса × ускорение)

🔹 **Третий закон**
F₁ = -F₂
(Сила действия равна силе противодействия)''',

    'оптика': '''📚 **Конспект: Оптика**

🔹 **Отражение света**
Угол падения = угол отражения

🔹 **Преломление света** (Закон Снеллиуса)
n₁·sin(α) = n₂·sin(β)

🔹 **Формула тонкой линзы**
1/F = 1/d + 1/f''',

    'термодинамика': '''📚 **Конспект: Термодинамика**

🔹 **Первый закон**
ΔU = A + Q

🔹 **Второй закон**
Нельзя передать тепло от холодного к горячему без затрат работы

🔹 **КПД тепловой машины**
η = (T₁ - T₂)/T₁ × 100%''',

    'электричество': '''📚 **Конспект: Электричество**

🔹 **Закон Кулона**
F = k·|q₁|·|q₂|/r²

🔹 **Закон Ома**
I = U/R

🔹 **Мощность тока**
P = I·U''',

    'механика': '''📚 **Конспект: Механика**

🔹 **Равномерное движение**
S = v·t

🔹 **Равноускоренное движение**
v = v₀ + a·t
S = v₀·t + (a·t²)/2

🔹 **Второй закон Ньютона**
F = m·a

🔹 **Импульс**
p = m·v

🔹 **Кинетическая энергия**
Eк = m·v²/2''',

    '9 класс': '''📚 **Физика 9 класс (основные темы)**

🔹 **Кинематика**
• S = v·t
• v = v₀ + a·t
• S = v₀·t + (a·t²)/2

🔹 **Динамика**
• F = m·a
• Закон всемирного тяготения: F = G·m₁·m₂/r²

🔹 **Законы сохранения**
• p = m·v
• Eк = m·v²/2
• Eп = m·g·h

🔹 **Колебания и волны**
• T = 1/ν
• λ = v·T''',

    'магнетизм': '''📚 **Конспект: Магнетизм**

🔹 **Сила Ампера**
F = B·I·L·sinα

🔹 **Сила Лоренца**
F = q·v·B·sinα

🔹 **Магнитный поток**
Φ = B·S·cosα''',

    'квантовая': '''📚 **Конспект: Квантовая физика**

🔹 **Фотоэффект**
h·ν = Aвых + Eк

🔹 **Постоянная Планка**
h = 6.63·10⁻³⁴ Дж·с

🔹 **Энергия фотона**
E = h·ν'''
}

# Создаем приложение бота
application = Application.builder().token(TOKEN).build()

# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **Привет!** Я бот с ГОТОВЫМИ конспектами по физике\n\n"
        "📝 **Напиши тему:**\n"
        "• ньютон\n• оптика\n• термодинамика\n• электричество\n"
        "• механика\n• магнетизм\n• квантовая\n• 9 класс\n\n"
        "⚡ **Конспект придёт сразу в чат!**",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topics = ", ".join(notes.keys())
    await update.message.reply_text(
        f"📚 **Доступные темы:**\n{topics}",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text.lower().strip()
    
    # Ищем точное совпадение
    if topic in notes:
        await update.message.reply_text(notes[topic], parse_mode='Markdown')
        return
    
    # Ищем по ключевым словам
    for key in notes.keys():
        if key in topic:
            await update.message.reply_text(notes[key], parse_mode='Markdown')
            return
    
    # Если не нашли
    topics_list = "\n".join([f"• {t}" for t in notes.keys()])
    await update.message.reply_text(
        f"❌ **Тема '{topic}' не найдена**\n\n"
        f"📋 **Доступные темы:**\n{topics_list}\n\n"
        f"👉 Попробуй: ньютон, оптика, механика",
        parse_mode='Markdown'
    )

# Регистрируем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Запуск бота (для Bothost используем polling)
if __name__ == "__main__":
    print("🚀 Бот запускается на Bothost...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
