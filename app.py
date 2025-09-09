
import subprocess
import re
import platform
import socket
from flask import Flask, jsonify, render_template

app = Flask(__name__)

def get_current_ssid():
    os_type = platform.system().lower()
    ssid = None
    if os_type == "windows":
        try:
            output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], encoding='utf-8')
            for line in output.split('\n'):
                if 'SSID' in line and 'BSSID' not in line:
                    ssid = line.split(':', 1)[-1].strip()
                    break
        except Exception:
            pass
    elif os_type == "linux":
        try:
            output = subprocess.check_output(['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'], encoding='utf-8')
            for line in output.strip().split('\n'):
                if line.startswith('yes:'):
                    ssid = line.split(':', 1)[-1]
                    break
        except Exception:
            pass
    return ssid

def get_ping(host='8.8.8.8'):
    os_type = platform.system().lower()
    try:
        if os_type == "windows":
            output = subprocess.check_output(['ping', '-n', '1', host], encoding='utf-8')
            for line in output.split('\n'):
                if 'Average' in line:
                    return int(line.split('=')[-1].replace('ms','').strip())
        else:
            output = subprocess.check_output(['ping', '-c', '1', host], encoding='utf-8')
            for line in output.split('\n'):
                if 'time=' in line:
                    return int(float(line.split('time=')[-1].split()[0]))
    except Exception:
        pass
    return None

def get_speedtest():
    try:
        import speedtest
    except ImportError:
        return None, None
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000  # Mbps
        upload = st.upload() / 1_000_000      # Mbps
        return round(download, 2), round(upload, 2)
    except Exception:
        return None, None


def get_current_ssid():
    os_type = platform.system().lower()
    ssid = None
    if os_type == "windows":
        try:
            output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], encoding='utf-8')
            for line in output.split('\n'):
                if 'SSID' in line and 'BSSID' not in line:
                    ssid = line.split(':', 1)[-1].strip()
                    break
        except Exception:
            pass
    elif os_type == "linux":
        try:
            output = subprocess.check_output(['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'], encoding='utf-8')
            for line in output.strip().split('\n'):
                if line.startswith('yes:'):
                    ssid = line.split(':', 1)[-1]
                    break
        except Exception:
            pass
    return ssid

def get_ping(host='8.8.8.8'):
    os_type = platform.system().lower()
    try:
        if os_type == "windows":
            output = subprocess.check_output(['ping', '-n', '1', host], encoding='utf-8')
            for line in output.split('\n'):
                if 'Average' in line:
                    return int(line.split('=')[-1].replace('ms','').strip())
        else:
            output = subprocess.check_output(['ping', '-c', '1', host], encoding='utf-8')
            for line in output.split('\n'):
                if 'time=' in line:
                    return int(float(line.split('time=')[-1].split()[0]))
    except Exception:
        pass
    return None

def get_speedtest():
    try:
        import speedtest
    except ImportError:
        return None, None
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000  # Mbps
        upload = st.upload() / 1_000_000      # Mbps
        return round(download, 2), round(upload, 2)
    except Exception:
        return None, None

@app.route("/current_speed")
def current_speed():
    ssid = get_current_ssid()
    ping = get_ping()
    download, upload = get_speedtest()
    return jsonify({
        'ssid': ssid,
        'ping': ping,
        'download': download,
        'upload': upload
    })

def scan_wifi():
    os_type = platform.system().lower()
    raw_networks = []
    if os_type == "windows":
        try:
            output = subprocess.check_output(['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'], encoding='utf-8')
            ssid = None
            signal = None
            speed = None
            for line in output.split('\n'):
                line = line.strip()
                ssid_match = re.match(r'SSID \d+ : (.+)', line)
                signal_match = re.match(r'Signal *: (.+)', line)
                if ssid_match:
                    ssid = ssid_match.group(1)
                elif signal_match and ssid:
                    signal = signal_match.group(1)
                elif re.match(r'\s*\d+\s+Mbps', line):
                    speed = line.strip()
                elif (line.startswith('BSSID') or line == '') and ssid and signal:
                    raw_networks.append({'ssid': ssid, 'signal': signal, 'speed': speed if speed else 'N/A'})
                    signal = None
                    speed = None
        except Exception as e:
            return []
    elif os_type == "linux":
        try:
            output = subprocess.check_output(["nmcli", "-t", "-f", "SSID,SIGNAL", "dev", "wifi"], encoding='utf-8')
            for line in output.strip().split('\n'):
                if line:
                    parts = line.split(":")
                    if len(parts) == 2:
                        ssid, signal = parts
                        raw_networks.append({'ssid': ssid, 'signal': signal, 'speed': 'N/A'})
        except Exception as e:
            return []

    best_networks = {}
    for net in raw_networks:
        ssid = net['ssid']
        # Try to extract a number, and always format as a percentage string
        percent = 0
        match = re.search(r'(\d{1,3})', str(net['signal']))
        if match:
            percent = int(match.group(1))
        signal_str = f"{percent}%"
        if ssid not in best_networks or percent > best_networks[ssid]['_percent']:
            best_networks[ssid] = {**net, 'signal': signal_str, '_percent': percent}

    return [{k: v for k, v in net.items() if k != '_percent'} for net in best_networks.values()]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan")
def scan():
    networks = scan_wifi()
    return jsonify({
        'count': len(networks),
        'networks': networks
    })

if __name__ == "__main__":
    app.run(debug=True)
