# Wi-Fi Network Scanner Web App

A cross-platform (Windows/Linux) web application for scanning nearby Wi-Fi networks, displaying their signal strength, and showing current network speed (ping, download, upload). Built with Python (Flask) and modern HTML/CSS/JavaScript.

## Features
- **Scan Nearby Wi-Fi Networks:**
  - Lists SSID, signal strength (bars and percentage), and other details.
  - Works on both Windows (using `netsh`) and Linux (using `nmcli`).
- **Current Network Speed:**
  - Shows ping, download, and upload speeds using `speedtest-cli`.
- **Modern UI:**
  - Responsive, animated, and color-themed web interface.
  - Signal strength visualized with bars and percentage.
- **Network Count:**
  - Displays the number of available networks.

## Requirements
- Python 3.7+
- pip (Python package manager)
- Windows or Linux OS

### Python Packages
Install all requirements with:
```bash
pip install -r requirements.txt
```

#### Main dependencies:
- Flask
- speedtest-cli

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/wifi-scanner-web.git
   cd wifi-scanner-web
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **(Optional) Install system tools:**
   - **Windows:** `netsh` is included by default.
   - **Linux:** Ensure `nmcli` is installed (usually part of NetworkManager).
     ```bash
     sudo apt install network-manager
     ```

## Usage
1. **Run the Flask app:**
   ```bash
   python app.py
   ```
2. **Open your browser and go to:**
   ```
   http://127.0.0.1:5000/
   ```
3. **Click "Scan Wi-Fi" to view available networks and current speed.**

## File Structure
```
wifi_scanner_web/
├── app.py                # Flask backend
├── requirements.txt      # Python dependencies
├── static/
│   ├── app.js            # Frontend JS logic
│   └── style.css         # CSS styles
└── templates/
    └── index.html        # Main web UI
```

## Notes
- **Admin/Root Privileges:**
  - On some systems, scanning Wi-Fi networks may require administrator/root privileges.
- **speedtest-cli:**
  - If download/upload speeds show as N/A, ensure `speedtest-cli` is installed and working.
- **Browser Compatibility:**
  - Modern browsers recommended for best UI experience.

## Troubleshooting
- If you see errors or N/A for speed, try running `speedtest-cli` directly in your terminal to check for issues.
- For Linux, make sure `nmcli` is available and your user has permission to scan networks.
- For Windows, ensure you are not running in a restricted environment.

## License
MIT License

## Author
- [Rishika](https://github.com/Rishikaaz)
