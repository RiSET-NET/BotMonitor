# 🛰️ R4X Monitoring Bot

![Platform](https://img.shields.io/badge/platform-Termux-blue?logo=termux)
![License](https://img.shields.io/badge/license-MIT-green)

🔔 Telegram bot pemantau koneksi internet berbasis Termux. Bot ini akan mengirim pesan ke Telegram saat koneksi internet kembali, serta mendeteksi perubahan ISP dan lokasi IP publik secara otomatis.

---

## ✨ Fitur Utama

- ⚠️ kirim alert ke Channel Telegram
- ✅ Notifikasi saat koneksi kembali, dengan:
  - Durasi offline
  - Informasi ISP sebelum dan sesudah
  - Lokasi IP publik (jika diaktifkan)
- 🔁 Deteksi pergantian ISP harian
- 🔧 Berjalan otomatis saat boot Termux
- 🧪 Ringan dan bisa jalan di latar belakang

---
---

## 📦 Dokumentasi Instalasi & Pemakaian

-Termux dan Termux:Boot terbaru
-Koneksi internet aktif
-Token Bot Telegram dan Channel ID
-Optional: Akses root (untuk menjalankan via sudo, bisa diubah kalau tanpa root)

---
## 🚀 Instalasi

```bash
pkg update && pkg install curl -y
```

### jalankan script installer:

```bash
bash <(curl -s https://raw.githubusercontent.com/RiSET-NET/BotMonitor/refs/heads/main/monitor.sh)
```
