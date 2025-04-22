from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import subprocess
import json
import asyncio
import re

# Fungsi untuk mengonversi byte ke format KB, MB, atau GB secara dinamis
def format_size(bytes):
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024 ** 2:
        return f"{bytes / 1024:.2f} KB"
    elif bytes < 1024 ** 3:
        return f"{bytes / (1024 ** 2):.2f} MB"
    else:
        return f"{bytes / (1024 ** 3):.2f} GB"

# Fungsi untuk memeriksa status baterai
async def handle_battery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        result = subprocess.run(['adb', 'shell', 'dumpsys', 'battery'], stdout=subprocess.PIPE, text=True)
        raw_info = result.stdout.strip()
        important_keys = {
            "level": "Battery Level",
            "status": "Status",
            "health": "Health",
            "temperature": "Temperature",
        }
        battery_info = {}
        for line in raw_info.splitlines():
            for key, label in important_keys.items():
                if key in line.lower():
                    value = line.split(":")[-1].strip()
                    if key == "temperature":
                        value = f"{int(value) / 10:.1f}°C"
                    battery_info[label] = value

        if not battery_info:
            await update.message.reply_text("❌ Tidak ada informasi baterai yang ditemukan.")
        else:
            formatted_info = "\n".join([f"🔋 *{key}*: `{value}`" for key, value in battery_info.items()])
            await update.message.reply_text(f"🔋 *Status Baterai:*\n\n{formatted_info}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Terjadi kesalahan saat mengambil status baterai: {e}")


# Fungsi untuk memeriksa penggunaan data menggunakan vnstat
def get_data_usage():
    try:
        # Jalankan perintah vnstat dengan format JSON
        result = subprocess.run(['vnstat', '--json'], stdout=subprocess.PIPE, text=True)
        data = json.loads(result.stdout)

        # Ambil informasi dari interface pertama
        interface = data['interfaces'][0]
        traffic = interface['traffic']

        # Data untuk hari ini
        today = traffic['day'][-1]  # Data hari terakhir
        today_download = today['rx']  # Download dalam byte
        today_upload = today['tx']    # Upload dalam byte
        today_total = today_download + today_upload

        # Data untuk bulan ini
        current_month = traffic['month'][-1]
        month_download = current_month['rx']  # Download dalam byte
        month_upload = current_month['tx']    # Upload dalam byte
        month_total = month_download + month_upload

        # Riwayat data harian
        daily_history = traffic['day']
        daily_history_formatted = [
            f"Tanggal: {day['date']['year']}-{day['date']['month']:02d}-{day['date']['day']:02d}, "
            f"⬇️ Download: {format_size(day['rx'])}, ⬆️ Upload: {format_size(day['tx'])}, "
            f"🔄 Total: {format_size(day['rx'] + day['tx'])}"
            for day in daily_history
        ]

        # Format hasil untuk ditampilkan
        result_text = (
            "📊 *Penggunaan Data (vnstat):*\n\n"
            f"📅 *Hari Ini:*\n"
            f"⬇️ *Download*: `{format_size(today_download)}`\n"
            f"⬆️ *Upload*: `{format_size(today_upload)}`\n"
            f"🔄 *Total*: `{format_size(today_total)}`\n\n"
            f"🗓️ *Bulan Ini:*\n"
            f"⬇️ *Download*: `{format_size(month_download)}`\n"
            f"⬆️ *Upload*: `{format_size(month_upload)}`\n"
            f"🔄 *Total*: `{format_size(month_total)}`\n\n"
            f"📖 *Riwayat Harian:*\n" + "\n".join(daily_history_formatted)
        )
        return result_text
    except Exception as e:
        return f"⚠️ Terjadi kesalahan saat mengambil informasi penggunaan data dengan vnstat: {e}"


# Fungsi untuk menangani perintah "monitor"
async def handle_monitor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data_usage = get_data_usage()
    await update.message.reply_text(data_usage, parse_mode="Markdown")

# Fungsi untuk mendapatkan informasi perangkat
def get_device_info():
    try:
        result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True)
        devices = result.stdout.strip()
        if "device" not in devices:
            return "❌ Tidak ada perangkat yang terhubung melalui ADB."
        result = subprocess.run(['adb', 'shell', 'getprop'], stdout=subprocess.PIPE, text=True)
        raw_info = result.stdout.strip()
        important_keys = {
            "ro.product.model": "Model",
            "ro.product.brand": "Brand",
            "ro.build.version.release": "Android Version",
            "ro.serialno": "Serial Number",
        }
        info = {}
        for line in raw_info.splitlines():
            if line.startswith("[") and "]: [" in line:
                key, value = line[1:].split("]: [", 1)
                value = value[:-1]
                if key in important_keys:
                    info[important_keys[key]] = value

        if not info:
            return "❌ Tidak ada informasi penting yang ditemukan pada perangkat."
        formatted_info = "\n".join([f"🔹 *{key}*: `{value}`" for key, value in info.items()])
        return f"📱 *Informasi Perangkat Anda:*\n\n{formatted_info}"
    except Exception as e:
        return f"⚠️ Terjadi kesalahan saat mengambil informasi perangkat: {e}"

# Fungsi untuk menangani perintah "info"
async def handle_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    device_info = get_device_info()
    await update.message.reply_text(device_info, parse_mode="Markdown")

# Fungsi untuk menampilkan menu
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    menu_text = (
        "📜 *Menu Perintah Bot:*\n\n"
        "1. 📱 *info*: Menampilkan informasi perangkat.\n"
        "2. ✈️ *pesawat*: Mengirimkan status *'Fitur sedang Maintenance'*.\n"
        "3. 🔋 *baterai*: Menampilkan status baterai perangkat.\n"
        "4. 📊 *monitor*: Menampilkan informasi penggunaan data perangkat.\n"
        "5. ♻️ *reboot*: Me-reboot perangkat.\n"
        "6. 🌐 *clash*: Mengirimkan tautan MetaCubeXD dan Zashboard.\n"
        "7. 🏠 *menu*: Menampilkan menu ini."
    )
    await update.message.reply_text(menu_text, parse_mode="Markdown")

# Fungsi untuk menangani perintah "pesawat" (sekarang hanya menampilkan pesan Maintenance)
async def handle_airplane(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✈️ *Fitur sedang Maintenance*", parse_mode="Markdown")

# Wrapper untuk menampilkan menu setelah setiap perintah
async def execute_with_menu(command_function, update, context):
    await command_function(update, context)
    await handle_menu(update, context)

# Fungsi untuk memulai bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🤖 Bot sudah berjalan! Kirim *menu* untuk melihat daftar perintah.", parse_mode="Markdown")

# Fungsi utama
def main():
    # Token bot Telegram Anda
    TOKEN = "7894823712:AAH1ScVaEgfYSV_hOl6ejLFuKhi4gKem0vs"

    application = Application.builder().token(TOKEN).build()

    # Tambahkan handler untuk setiap perintah dengan wrapper
    application.add_handler(CommandHandler("start", lambda u, c: execute_with_menu(start, u, c)))
    application.add_handler(CommandHandler("info", lambda u, c: execute_with_menu(handle_info, u, c)))
    application.add_handler(CommandHandler("pesawat", lambda u, c: execute_with_menu(handle_airplane, u, c)))
    application.add_handler(CommandHandler("baterai", lambda u, c: execute_with_menu(handle_battery, u, c)))
    application.add_handler(CommandHandler("monitor", lambda u, c: execute_with_menu(handle_monitor, u, c)))
    application.add_handler(CommandHandler("menu", handle_menu))

    # Jalankan bot
    print("🤖 Bot sedang berjalan...")
    application.run_polling()

if __name__ == '__main__':
    main()
