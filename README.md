# BotMonitor

### 1. **Persiapan Awal di Termux**
   - Pastikan Termux terinstal di perangkat Anda.
   - Perbarui paket dan repositori:
     ```bash
     pkg update && pkg upgrade -y
     ```
     ```bash
     pkg install git python -y
     ```
     ```bash
     git clone https://github.com/RiSET-NET/BotMonitor.git
     ```
     ```bash
     cd BotMonitor
     ```
     ```bash
     python setup.py
     ```


### 2. **Konfigurasi Token Bot Telegram**
   - Ganti token bot Telegram di script "config.json" pada bagian ini:
     ```json
     TOKEN = "MASUKAN_TOKEN_DISINI"
     ```
   - Anda bisa mendapatkan token dari **BotFather** di Telegram dengan membuat bot baru.


### 3. **Menjalankan Script**
   - Jalankan script Python:
     ```bash
     sudo python3 bot.py
     ```
   - Pastikan script berjalan tanpa error, dan bot mulai menerima perintah.

---

### **Catatan Penting**
- **ADB** membutuhkan perangkat Android dengan debugging USB aktif. Aktifkan di perangkat Anda melalui opsi pengembang.
- **MONITOR** hanya berfungsi jika interface jaringan perangkat Anda kompatibel.
- Pastikan perangkat memiliki koneksi internet untuk menjalankan **speedtest** dan bot Telegram.
- Jika menggunakan script ini untuk pertama kali, pastikan Anda memahami izin dan akses yang digunakan oleh `ADB` untuk mengontrol perangkat.

Jika ada kendala dalam instalasi atau eksekusi, beri tahu saya untuk bantuan lebih lanjut!

![Telegram](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://t.me/RiSET_NET)
[![Github](https://img.shields.io/:chat-on_gitter-ED2067.svg)](https://github.com/RiSET-NET/)
[![Country](https://img.shields.io/badge/country-indonesia-blue.svg)](#)

