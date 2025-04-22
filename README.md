# BotMonitor

### 1. **Persiapan Awal di Termux**
   - Pastikan Termux terinstal di perangkat Anda.
   - Perbarui paket dan repositori:
     ```bash
     pkg update && pkg upgrade
     ```

### 2. **Instalasi Python dan Pip**
   - Instal Python (minimal versi 3.7):
     ```bash
     pkg install python
     ```
   - Verifikasi instalasi Python:
     ```bash
     python --version
     ```
   - Instal `pip` (Python Package Manager):
     ```bash
     pkg install python-pip
     ```

### 3. **Instalasi Modul Python**
   - Instal semua modul Python yang diperlukan oleh script:
     ```bash
     pip install python-telegram-bot speedtest-cli psutil
     ```
   - Bila ada modul tambahan yang diperlukan seperti `asyncio` atau `re`, pastikan modul tersebut sudah terinstal. (Kebanyakan modul ini sudah bawaan Python.)

### 4. **Instalasi `ADB` untuk Kontrol Perangkat Android**
   - Instal `ADB` (Android Debug Bridge):
     ```bash
     pkg install android-tools
     ```
   - Pastikan perangkat Android Anda dihubungkan ke Termux dengan mode debugging USB aktif.

### 5. **Instalasi `vnstat` untuk Pemantauan Bandwidth**
   - Instal `vnstat`:
     ```bash
     pkg install vnstat
     ```
   - Konfigurasi `vnstat` untuk interface jaringan (misalnya `wlan0`):
     ```bash
     vnstat --update --interface wlan0
     ```

### 6. **Buat File `airplane.sh`**
   - Pastikan file `airplane.sh` sudah dibuat dan berisi perintah untuk mengaktifkan dan menonaktifkan mode pesawat. Contoh sederhana:
     ```bash
     echo -e '#!/bin/bash\nadb shell settings put global airplane_mode_on 1\nsleep 2\nadb shell settings put global airplane_mode_on 0' > airplane.sh
     chmod +x airplane.sh
     ```

### 7. **Konfigurasi Token Bot Telegram**
   - Ganti token bot Telegram di script pada bagian ini:
     ```python
     TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
     ```
   - Anda bisa mendapatkan token dari **BotFather** di Telegram dengan membuat bot baru.

### 8. **Menjalankan Script**
   - Jalankan script Python:
     ```bash
     python bot.py
     ```
   - Pastikan script berjalan tanpa error, dan bot mulai menerima perintah.

---

### **Catatan Penting**
- **ADB** membutuhkan perangkat Android dengan debugging USB aktif. Aktifkan di perangkat Anda melalui opsi pengembang.
- **vnstat** hanya berfungsi jika interface jaringan perangkat Anda kompatibel.
- Pastikan perangkat memiliki koneksi internet untuk menjalankan **speedtest** dan bot Telegram.
- Jika menggunakan script ini untuk pertama kali, pastikan Anda memahami izin dan akses yang digunakan oleh `ADB` untuk mengontrol perangkat.

Jika ada kendala dalam instalasi atau eksekusi, beri tahu saya untuk bantuan lebih lanjut!
