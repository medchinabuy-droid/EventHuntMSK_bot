import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from sheets import get_sheet
from datetime import date

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Ближайшие", callback_data="near")],
        [InlineKeyboardButton("🆓 Бесплатные", callback_data="free")],
        [InlineKeyboardButton("🎟 С промо", callback_data="promo")],
        [InlineKeyboardButton("📅 Сегодня", callback_data="today")]
    ]
    await update.message.reply_text(
        "EventHuntMSK_bot — собираю все события по Москве и РФ 🚀",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    sheet = get_sheet()
    rows = sheet.get_all_records()
    today = str(date.today())

    if query.data == "near":
        result = rows[:5]
    elif query.data == "free":
        result = [r for r in rows if r["Статус"] == "Бесплатно"]
    elif query.data == "promo":
        result = [r for r in rows if r["Статус"] == "Промо"]
    elif query.data == "today":
        result = [r for r in rows if r["Дата"] == today]
    else:
        result = []

    if not result:
        await query.edit_message_text("Подходящих событий нет 😕")
        return

    for e in result[:5]:
        await query.message.reply_text(
            f"📅 {e['Дата']}\n🎯 {e['Название']}\n💸 {e['Статус']}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Открыть", url=e["Ссылка"])]
            ])
        )

def run_bot():
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.run_polling()
