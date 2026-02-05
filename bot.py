import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from sheets import get_sheet
from datetime import date

def format_event(e):
    text = (
        f"📅 {e['Дата']}\n"
        f"📍 {e['Локация']}\n"
        f"🎯 {e['Название']}\n"
        f"💸 {e['Статус']}\n"
    )
    return text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Ближайшие", callback_data="near")],
        [InlineKeyboardButton("🆓 Бесплатные", callback_data="free")],
        [InlineKeyboardButton("🎟 С промо", callback_data="promo")],
        [InlineKeyboardButton("📅 На сегодня", callback_data="today")]
    ]
    await update.message.reply_text(
        "Привет! Я EventHuntMSK_bot — ищу полезные мероприятия по Москве 🚀",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    sheet = get_sheet()
    rows = sheet.get_all_records()

    today = str(date.today())
    result = []

    if query.data == "near":
        result = sorted(rows, key=lambda x: x["Дата"])[:5]
    elif query.data == "free":
        result = [r for r in rows if r["Статус"] == "Бесплатно"]
    elif query.data == "promo":
        result = [r for r in rows if r["Статус"] == "Промо"]
    elif query.data == "today":
        result = [r for r in rows if r["Дата"] == today]

    if not result:
        await query.edit_message_text("Пока нет подходящих событий 😕")
        return

    for e in result[:5]:
        buttons = [
            [InlineKeyboardButton("🔗 Открыть событие", url=e["Ссылка"])]
        ]
        await query.message.reply_text(
            format_event(e),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

def run_bot():
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.run_polling()
