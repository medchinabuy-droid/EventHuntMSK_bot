import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sheets import get_sheet

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /events — покажу ближайшие мероприятия 🚀")

async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheet = get_sheet()
    rows = sheet.get_all_records()

    msg = "Ближайшие мероприятия:\n\n"
    for r in rows[-5:]:
        msg += f"📅 {r['Дата']} — {r['Название']}\n"
        msg += f"💸 {r['Статус']} | {r['Цена']}\n"
        msg += f"🔗 {r['Ссылка']}\n\n"

    await update.message.reply_text(msg[:4000])

def run_bot():
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("events", events))
    app.run_polling()
