#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

loading() {
  local pid=$!
  local delay=0.1
  local spinstr='|/-\'
  while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
    local temp=${spinstr#?}
    printf " [%c]  " "$spinstr"
    local spinstr=$temp${spinstr%"$temp"}
    sleep $delay
    printf "\b\b\b\b\b\b"
  done
  printf "    \b\b\b\b"
}

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "   🚀 ${GREEN}R4X Auto Installer${NC} by RiSET"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -ne "${YELLOW}[*] Updating Termux repositories...${NC}"
(pkg update -y > /dev/null 2>&1) & loading
echo -e "${GREEN} [DONE]${NC}"

echo -ne "${YELLOW}[*] Installing dependencies...${NC}"
(pkg install python sudo curl git termux-tools -y > /dev/null 2>&1 && pip install requests > /dev/null 2>&1) & loading
echo -e "${GREEN} [DONE]${NC}"

echo -ne "${YELLOW}[*] Preparing directory...${NC}"
mkdir -p ~/.termux/boot > /dev/null 2>&1 & loading
echo -e "${GREEN} [DONE]${NC}"

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
read -p "[?] Enter your Telegram Bot Token: " BOT_TOKEN
read -p "[?] Enter your Channel ID (e.g. -100xxxx): " CHANNEL_ID

cat > ~/.termux/boot/tmp.json <<EOL
{
  "BOT_TOKEN": "$BOT_TOKEN",
  "CHANNEL_ID": "$CHANNEL_ID",
  "SHOW_IP_LOCATION": true
}
EOL


echo -ne "${YELLOW}[*] Downloading bot...${NC}"
cat > ~/.termux/boot/tmp.py <<'PYTHON_EOF'
import json
import subprocess
import time
import requests
from datetime import datetime

# Load config
with open('/data/data/com.termux/files/home/.termux/boot/tmp.json') as f:
    config = json.load(f)

BOT_TOKEN = config['BOT_TOKEN']
CHANNEL_ID = config['CHANNEL_ID']
SHOW_IP_LOCATION = config.get("SHOW_IP_LOCATION", False)

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHANNEL_ID,
        'text': text,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"[!] Gagal kirim Telegram: {e}")

def ping_host(host="8.8.8.8"):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "2", host], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def get_isp_info():
    try:
        ip = subprocess.check_output(['curl', '-s', 'https://ipinfo.io/ip']).decode().strip()
        isp = subprocess.check_output(['curl', '-s', 'https://ipinfo.io/org']).decode().strip()
        isp = isp.replace("AS", "").strip()
        return ip or "N/A", isp or "N/A"
    except Exception as e:
        return "N/A", f"Error: {e}"

def get_location(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=city,regionName,country"
        res = requests.get(url, timeout=5).json()
        return f"{res.get('city', '')}, {res.get('regionName', '')}, {res.get('country', '')}"
    except Exception:
        return None

# Inisialisasi
fail_count = 0
PING_FAIL_THRESHOLD = 7
offline_start = None
has_alerted = False
alert_start_sent = False
isp_change_count = 0
last_reset_time = datetime.now()

# Cek ISP awal untuk referensi
isp_prev_ip, isp_prev_name = get_isp_info()
print(f"[✓] ISP Awal: {isp_prev_name} ({isp_prev_ip})")

# Kirim alert awal
if not alert_start_sent:
    send_telegram(
        "━━━━━━━━━━━━━━━━━\n"
        "<b>🛰️ R4X Monitoring</b>\n"
        "━━━━━━━━━━━━━━━━━\n"
        "Bot sedang berjalan...\n"
        "━━━━━━━━━━━━━━━━━"
    )
    alert_start_sent = True

# Loop utama
while True:
    now = datetime.now()

    # Reset perubahan ISP harian jika tanggal berganti
    if now.date() != last_reset_time.date():
        isp_change_count = 0
        last_reset_time = now
        print("[✓] Reset jumlah perubahan ISP harian.")

    online = ping_host()

    if online:
        if fail_count >= PING_FAIL_THRESHOLD:
            offline_end = now
            offline_duration = str(offline_end - offline_start).split(".")[0]

            time.sleep(1)  # Tunggu sebelum ambil ISP

            ip_now, isp_now = get_isp_info()
            waktu = offline_end.strftime('%Y-%m-%d %H:%M:%S')

            location_text = ""
            if SHOW_IP_LOCATION and ip_now and ip_now != "N/A":
                loc = get_location(ip_now)
                if loc:
                    location_text = f"\n📍 <b>Lokasi IP</b>      : {loc}"

            # Hitung perubahan ISP
            if isp_now != isp_prev_name or ip_now != isp_prev_ip:
                isp_change_count += 1

            alert_text = (
                "━━━━━━━━━━━━━━━━━\n"
                "<b>🛰️ R4X Monitoring</b>\n"
                "━━━━━━━━━━━━━━━━━\n\n"
                "<b>✅ Koneksi Internet Kembali</b>\n"
                "━━━━━━━━━━━━━━━━━\n"
                "📡 <b>Durasi Offline</b> : " + offline_duration + "\n"
                "🕓 <b>Waktu</b>  : " + waktu + "\n"
                "━━━━━━━━━━━━━━━━━\n"
                "🔁 <b>ISP Sebelumnya</b>:\n"
                f"   • IP   : {isp_prev_ip}\n"
                f"   • ISP  : {isp_prev_name}\n"
                "━━━━━━━━━━━━━━━━━\n"
                "📶 <b>ISP Sekarang</b>:\n"
                f"   • IP   : {ip_now}\n"
                f"   • ISP  : {isp_now}" +
                location_text + "\n"
                "━━━━━━━━━━━━━━━━━\n"
                "🧮 <b>Total perubahan hari ini</b>: " + str(isp_change_count) + "\n"
                "━━━━━━━━━━━━━━━━━"
            )
            send_telegram(alert_text)

            # Perbarui ISP sebelumnya
            isp_prev_ip, isp_prev_name = ip_now, isp_now
            has_alerted = False

        fail_count = 0
    else:
        fail_count += 1
        if fail_count == PING_FAIL_THRESHOLD:
            offline_start = now
            send_telegram(
                "<b>⚠️ Koneksi Internet Hilang</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━\n"
                "Bot tidak dapat menjangkau internet.\n"
                f"Ping gagal sebanyak {PING_FAIL_THRESHOLD} .\n"
                "━━━━━━━━━━━━━━━━━━━━━━━"
            )
            has_alerted = True

    time.sleep(1)

PYTHON_EOF
loading
echo -e "${GREEN} [DONE]${NC}"

echo -ne "${YELLOW}[*] Setting auto-start...${NC}"
cat > ~/.termux/boot/start.sh <<EOL
#!/bin/bash
sudo python3 /data/data/com.termux/files/home/.termux/boot/tmp.py
EOL

chmod +x ~/.termux/boot/start.sh ~/.termux/boot/tmp.py ~/.termux/boot/tmp.json
chmod 777 ~/.termux/boot/start.sh ~/.termux/boot/tmp.py ~/.termux/boot/tmp.json > /dev/null 2>&1
echo -e "${GREEN} [DONE]${NC}"

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e " ✅ ${GREEN}Installation complete! Bot ready to run on boot.${NC}"
echo -e " ℹ️ ${RED}You can Reboot Device...${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
