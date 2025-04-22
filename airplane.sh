#!/data/data/com.termux/files/usr/bin/bash

# Lama mode pesawat aktif (dalam detik)
INTERVAL_ON=2

# Fungsi konfigurasi airplane_mode_radios (tanpa matikan WiFi & Hotspot)
set_airplane_radios() {
    echo "[INFO] Mengatur airplane_mode_radios (cell, nfc, wimax)..."
    su -c 'settings put global airplane_mode_radios "cell,nfc,wimax"'
    su -c 'content update --uri content://settings/global --bind value:s:"cell,nfc,wimax" --where "name=\'airplane_mode_radios\'"'
}

# Fungsi untuk mengaktifkan mode pesawat
enable_airplane_mode() {
    echo "[INFO] Mengaktifkan Mode Pesawat..."
    su -c 'settings put global airplane_mode_on 1'
    su -c 'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true'
}

# Fungsi untuk menonaktifkan mode pesawat
disable_airplane_mode() {
    echo "[INFO] Menonaktifkan Mode Pesawat..."
    su -c 'settings put global airplane_mode_on 0'
    su -c 'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false'
}

# Eksekusi
set_airplane_radios
enable_airplane_mode
sleep "$INTERVAL_ON"
disable_airplane_mode
