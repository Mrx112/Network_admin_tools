##### Network Admin Tools #####

Network Admin Tool adalah aplikasi administrasi jaringan yang komprehensif dengan antarmuka grafis yang dirancang untuk membantu administrator sistem dalam mengelola, memantau, dan mengontrol perangkat jaringan secara efisien.
🚀 Fitur Utama

    🔍 Network Scanning - Deteksi perangkat dengan ARP scanning dan Nmap integration

    📊 Device Management - Tabel interaktif dengan informasi detail perangkat

    ⚡ Remote Control - Eksekusi perintah dan kontrol perangkat remote

    📁 File Transfer - Transfer file aman antara lokal dan remote

    📜 Script Generator - Pembuatan script otomatis (PowerShell/Batch)

    🚀 Application Launcher - Manajemen aplikasi lokal dan remote

    🔐 Security Features - Manajemen kredensial dan privilege checking

📦 Struktur Proyek
text

NetworkAdminTool/
├── src/                    # Source code utama
│   ├── main.py            # Entry point aplikasi
│   ├── NetworkManager.py  # Manajemen jaringan dasar
│   ├── DeviceInfo.py      # Informasi perangkat
│   ├── FileTransfer.py    # Transfer file
│   ├── RemoteControl.py   # Kontrol remote
│   ├── GUI.py             # Antarmuka dasar
│   ├── EnhancedGUI.py     # Antarmuka enhanced
│   ├── EnhancedNetworkTable.py # Tabel perangkat
│   ├── NmapScanner.py     # Scanner Nmap
│   └── NmapDevice.py      # Device model Nmap
├── assets/                # Aset aplikasi
│   ├── icons/            # Ikon aplikasi
│   └── styles/           # Stylesheet CSS
├── scripts/              # Script utilitas
├── docs/                 # Dokumentasi
└── Makefile             # Build automation

🛠️ Instalasi
Prerequisites

    Python 3.6 atau lebih tinggi

    Nmap (untuk fitur scanning advanced)

    Tkinter (biasanya sudah termasuk dengan instalasi Python)

Linux/macOS
bash

# Clone repository
git clone https://github.com/yourusername/NetworkAdminTool.git
cd NetworkAdminTool

# Install dependencies
sudo ./scripts/install_dependencies.sh

# Atau install manual
pip install -r requirements.txt

# Install nmap (jika belum terinstall)
# Ubuntu/Debian
sudo apt-get install nmap
# macOS
brew install nmap

Windows

    Download dan install Python 3.6+ dari python.org

    Download dan install Nmap dari nmap.org

    Clone atau download repository ini

    Install dependencies:
    cmd

    pip install -r requirements.txt

🚀 Cara Penggunaan
Menjalankan Aplikasi
bash

# Mode normal
python src/main.py

# Mode administrator (disarankan untuk fitur lengkap)
sudo python src/main.py  # Linux/macOS
# Atau Run as Administrator di Windows

Tab Network Scan

    Pilih network interface dari dropdown

    Masukkan IP range target (contoh: 192.168.1.0/24)

    Pilih jenis scan: Quick Scan, Full Scan, OS Detection, atau Service Detection

    Klik "Scan Network" untuk memulai scanning

Tab Network Devices

    Lihat semua perangkat yang terdeteksi dalam tabel terorganisir

    Gunakan fitur refresh untuk update data terbaru

    Klik pada perangkat untuk melihat detail

Tab Script Generator

    Masukkan target IP

    Pilih jenis script (PowerShell atau Batch)

    Pilih dari predefined scripts atau buat custom

    Generate, execute, atau save script

Tab Application Launcher

    Masukkan kredensial remote device

    Pilih aplikasi dari daftar atau masukkan manual

    Tambahkan arguments jika diperlukan

    Launch aplikasi secara lokal atau remote

📖 Dokumentasi

Lihat docs/manual.md untuk panduan penggunaan lengkap dan penjelasan fitur detail.
🎯 Contoh Penggunaan
Scanning Jaringan
python

# Melakukan quick scan pada subnet
network_manager.arp_scan("192.168.1.0/24")

# Melakukan advanced scan dengan Nmap
nmap_scanner.scan("192.168.1.1-100", options="-O -sV")

Remote Execution
python

# Menjalankan command pada remote device
app_launcher.launch_remote_application(
    "192.168.1.10", 
    "username", 
    "password", 
    "notepad.exe", 
    "C:\\file.txt"
)

Script Generation
python

# Generate PowerShell script
script_generator.generate_script(
    "powershell",
    ["Get-Process", "Get-Service"],
    "192.168.1.10",
    "System Diagnostics"
)

🔧 Development
Menambah Fitur Baru

    Fork repository

    Buat branch untuk fitur baru (git checkout -b feature/AmazingFeature)

    Commit perubahan (git commit -m 'Add some AmazingFeature')

    Push ke branch (git push origin feature/AmazingFeature)

    Buat Pull Request

Build dari Source
bash

# Menggunakan Makefile
make build

# Atau menggunakan script
./scripts/build.sh

🤝 Berkontribusi

Kontribusi selalu diterima! Silakan lihat CONTRIBUTING.md untuk panduan detail.

Beberapa area yang bisa dikontribusikan:

    Penambahan protocol support baru

    Enhancement security features

    UI/UX improvements

    Documentation translations

    Bug fixes dan optimizations

📊 Screenshots

(Tambahkan screenshot aplikasi di sini)

    Tampilan Network Scan dengan hasil detection

    Tabel Network Devices dengan informasi detail

    Interface Script Generator dengan output

    Application Launcher dengan remote execution results

🐛 Troubleshooting
Common Issues

Error: "No permission to perform network scan"

    Solusi: Jalankan aplikasi dengan privileges administrator

Error: "Nmap not found"

    Solusi: Pastikan Nmap terinstall dan ada di PATH system

GUI tidak muncul atau error

    Solusi: Pastikan Tkinter terinstall (python -m tkinter untuk test)

Debug Mode

Aktifkan debug mode dengan environment variable:
bash

export NETWORK_ADMIN_DEBUG=1
python src/main.py

📄 Lisensi

Distributed under the MIT License. Lihat LICENSE untuk detail lebih lanjut.
🙏 Acknowledgments

    Nmap untuk network scanning capabilities

    Tkinter untuk GUI framework

    Komunitas open source untuk berbagai library pendukung

📞 Support

Jika Anda memiliki pertanyaan atau masalah:

    Cek documentation terlebih dahulu

    Cari solusi di Issues

    Buat issue baru jika belum ada solusi

🔄 Changelog

Lihat CHANGELOG.md untuk history perubahan dan versi.
