# BotMonitor
<div align="center">
  <a href="https://t.me/RiSET_NET"><img src="https://img.shields.io/badge/Telegram--Channel-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
</div>
<div align="center">
  <a href="https://ibb.co.com/PsDMhgtb"><img src="https://i.ibb.co.com/20ZStd5L/IMG-1176.jpg" alt="IMG-1176" border="0" /></a>
</div>

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
