function animateValue(element, start, end, duration, suffix = '') {
    if (start === null || end === null) {
        element.textContent = 'N/A';
        return;
    }
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value + suffix;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            element.textContent = end + suffix;
        }
    };
    window.requestAnimationFrame(step);
}

function fetchCurrentSpeed() {
    const speedDiv = document.getElementById('speedInfo');
    speedDiv.textContent = 'Loading...';
    fetch('/current_speed')
        .then(res => res.json())
        .then(data => {
            if (!data.ssid) {
                speedDiv.textContent = 'Not connected to any Wi-Fi network.';
                return;
            }
            speedDiv.innerHTML = `<b>SSID:</b> ${data.ssid}<br>
                <b>Ping:</b> <span id="pingVal"></span> ms<br>
                <b>Download:</b> <span id="downVal"></span> Mbps<br>
                <b>Upload:</b> <span id="upVal"></span> Mbps`;
            animateValue(document.getElementById('pingVal'), 0, data.ping, 800);
            animateValue(document.getElementById('downVal'), 0, data.download, 1200);
            animateValue(document.getElementById('upVal'), 0, data.upload, 1200);
        })
        .catch(() => {
            speedDiv.textContent = 'Failed to get speed info.';
        });
}

window.addEventListener('DOMContentLoaded', fetchCurrentSpeed);

document.getElementById('scanBtn').addEventListener('click', function() {
    fetchCurrentSpeed();
});


document.getElementById('scanBtn').addEventListener('click', function() {
    document.getElementById('loading').style.display = 'block';
    fetch('/scan')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#results tbody');
            tbody.innerHTML = '';
            document.getElementById('networkCount').textContent = `Available Networks: ${data.count}`;
            data.networks.forEach(net => {
                const row = document.createElement('tr');
                let percent = 0;
                const match = /([0-9]{1,3})%/.exec(net.signal);
                if (match) percent = parseInt(match[1]);
                let bars = 0;
                if (percent >= 80) bars = 4;
                else if (percent >= 60) bars = 3;
                else if (percent >= 40) bars = 2;
                else if (percent >= 20) bars = 1;
                let tower = '<span class="tower">';
                for (let i = 1; i <= 4; i++) {
                    tower += `<span class="bar${i} ${i<=bars?'active':''}"></span>`;
                }
                tower += `</span> <span class="signal-text">${percent}%</span>`;
                row.innerHTML = `<td>${net.ssid}</td><td>${tower}</td>`;
                tbody.appendChild(row);
            });
            document.getElementById('loading').style.display = 'none';
        })
        .catch(() => {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('networkCount').textContent = '';
            alert('Failed to scan networks.');
        });
});
