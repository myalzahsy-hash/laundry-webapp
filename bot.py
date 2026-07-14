import os
import json
import logging
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === KONFIG ===
TOKEN = "8541476833:AAHpgtTRGEJ1kF468TTEAlsPgcZbKZxRVEE"
WEBAPP_URL = "https://myalzahsy-hash.github.io/laundry-webapp/"

logging.basicConfig(level=logging.INFO)

# === HANDLER START ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    webapp_btn = KeyboardButton(
        text="🧺 BUKA INPUT STRUK",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    keyboard = ReplyKeyboardMarkup([[webapp_btn]], resize_keyboard=True)

    await update.message.reply_text(
        "👋 Selamat datang di Laundry Bot!\n"
        "Klik tombol di bawah buat input struk 👇",
        reply_markup=keyboard
    )

# === HANDLER DATA DARI WEBAPP ===
async def webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = json.loads(update.effective_message.web_app_data.data)
        logging.info(f"📦 DATA MASUK: {data}")

        nama = data.get('nama', '-')
        nota = data.get('nota', '-')
        items = data.get('items', {})
        total = data.get('total', 0)

        # Format pesan ringkasan
        msg = f"✅ *STRUK BARU*\n"
        msg += f"👤 Nama: {nama}\n"
        msg += f"📋 No. Nota: {nota}\n"
        msg += f"─────────────\n"

        label_map = {
            'pakaian': '👕 Pakaian',
            'cd': '👖 Celana',
            'bh': '👔 BH',
            'kaoskaki': '🧦 Kaos Kaki',
            'lainnya': '📦 Lainnya'
        }

        for key, label in label_map.items():
            qty = items.get(key, 0)
            if qty > 0:
                msg += f"{label}: {qty} pcs\n"

        msg += f"─────────────\n"
        msg += f"📦 Total: {total} pcs\n"

        await update.message.reply_text(msg, parse_mode='Markdown')

        # 🔥 TARUH KODE PRINT QZ TRAY DI SINI NANTI

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("❌ Gagal memproses data struk.")

# === HANDLER BIASA ===
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Klik tombol 🧺 BUKA INPUT STRUK buat mulai.")

# === MAIN ===
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("✅ Bot jalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
