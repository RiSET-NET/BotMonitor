# BotMonitor

<div align="center">
  <p align="center"><img src="https://profile-counter.glitch.me/{mutiara-wrt}/count.svg" alt="Maizil41 :: Visitor's Count" /></p>
  <img alt="License" src="https://img.shields.io/github/license/Maizil41/Mutiara-Wrt?style=for-the-badge&logo=github">
  <a target="_blank" href="https://github.com/Maizil41/Mutiara-Wrt/releases"><img src="https://img.shields.io/github/release/Maizil41/Mutiara-Wrt?style=for-the-badge&logo=Openwrt"></a>
  <a target="_blank" href="https://github.com/Maizil41/Mutiara-Wrt/releases"><img src="https://img.shields.io/github/downloads/Maizil41/Mutiara-Wrt/total?style=for-the-badge&logo=Openwrt"></a>
</div>
<hr/>
<p align="center">
<a href="https://sociabuzz.com/maizil41/tribe"><img src="https://img.shields.io/badge/SOCIALBUZZ-6FBB18?style=for-the-badge&logo=ko-fi&logoColor=white"></a>
<a href="https://saweria.co/mutiarawrt"><img src="https://img.shields.io/badge/SAWERIA-FFAE00?style=for-the-badge&logo=ko-fi&logoColor=white"></a>
<br><br/>
<a href="https://t.me/mutiarawrt"><img src="https://img.shields.io/badge/Telegram--Channel-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
<a href="https://www.youtube.com/@mutiara-wrt"><img src="https://img.shields.io/badge/Youtube--Channel-e02c2c?style=for-the-badge&logo=youtube&logoColor=white"></a>
<a href="https://t.me/+X1zD3nY9Fz1lNDU1"><img src="https://img.shields.io/badge/Telegram--Groups-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
</p>
<hr/>

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
