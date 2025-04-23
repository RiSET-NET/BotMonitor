import json
import subprocess
import time
import speedtest
import vnstat
import platform
from datetime import timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from threading import Thread

# Load config
with open("config.json") as f:
    config = json.load(f)

BOT_TOKEN = config["BOT_TOKEN"]
AUTHORIZED_USERS = config["AUTHORIZED_USERS"]

# Utility
def run_adb(command: str) -> str:
    try:
        output = subprocess.check_output(["adb", "shell"] + command.split(), stderr=subprocess.STDOUT)
        return output.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode()}"

def authorized(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in AUTHORIZED_USERS:
            await update.message.reply_text("🚫 Tidak diizinkan.")
            return
        await func(update, context)
    return wrapper

# Commands
@authorized
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ADB Telegram Siap!")

@authorized
async def battery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = run_adb("dumpsys battery")
    await update.message.reply_text(f"🔋 Info Baterai:\n{output}")

@authorized
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 Ping Google...")
    result = run_adb("ping -c 4 8.8.8.8")
    await update.message.reply_text(f"🌐 Hasil Ping:\n{result}")

@authorized
async def speed_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Menguji kecepatan internet...")
    
    def test_speed():
        try:
            st = speedtest.Speedtest()
            st.download()
            st.upload()
            res = st.results.dict()
            message = (
                f"🌍 ISP: {res['client']['isp']}\n"
                f"📶 Download: {res['download'] / 1_000_000:.2f} Mbps\n"
                f"📤 Upload: {res['upload'] / 1_000_000:.2f} Mbps\n"
                f"📍 Server: {res['server']['name']} ({res['server']['country']})\n"
                f"⏱️ Ping: {res['ping']} ms"
            )
        except Exception as e:
            message = f"❌ Speedtest gagal: {e}"
        app.create_task(update.message.reply_text(message))

    Thread(target=test_speed).start()

@authorized
async def data_usage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = vnstat.interface("wlan0").last_24_hours()
        usage = (
            f"📊 Penggunaan Data (wlan0):\n"
            f"⬇️ Download: {data.rx:.2f} MB\n"
            f"⬆️ Upload: {data.tx:.2f} MB\n"
            f"🔄 Total: {data.total:.2f} MB"
        )
    except Exception as e:
        usage = f"❌ Gagal ambil data vnstat: {e}"
    await update.message.reply_text(usage)

@authorized
async def device_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    props = run_adb("getprop")
    info = "\n".join([
        f"🧠 CPU: {run_adb('cat /proc/cpuinfo | grep Hardware')}",
        f"📱 Model: {run_adb('getprop ro.product.model')}",
        f"📟 Brand: {run_adb('getprop ro.product.brand')}",
        f"📦 Versi: {run_adb('getprop ro.build.version.release')}",
        f"🔧 API: {run_adb('getprop ro.build.version.sdk')}",
        f"🆔 Build: {run_adb('getprop ro.build.display.id')}",
    ])
    await update.message.reply_text(info)

@authorized
async def ram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mem = run_adb("cat /proc/meminfo | grep MemAvailable")
    await update.message.reply_text(f"💾 RAM Tersedia:\n{mem}")

@authorized
async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    seconds = float(run_adb("cat /proc/uptime").split()[0])
    uptime_str = str(timedelta(seconds=int(seconds)))
    await update.message.reply_text(f"⏱️ Uptime: {uptime_str}")

# Setup
app = Application.builder().token(BOT_TOKEN).build()

# Register
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("battery", battery))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("speedtest", speed_test))
app.add_handler(CommandHandler("data", data_usage))
app.add_handler(CommandHandler("info", device_info))
app.add_handler(CommandHandler("ram", ram))
app.add_handler(CommandHandler("uptime", uptime))

# Run bot
if __name__ == "__main__":
    print("🚀 Bot Telegram ADB dijalankan...")
    app.run_polling()
