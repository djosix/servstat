# ServStat

Monitoring CPU, memory, and GPU usage of multiple servers.

![Demo Image](https://user-images.githubusercontent.com/17045050/76153224-2c58c500-6104-11ea-8ca1-dd9f2c1b2e37.png)

## Running backend

Use root as example:

```shell
cd /root
git clone https://github.com/djosix/servstat.git .servstat
cd .servstat/backend

python3 -m pip install -r requirements.txt
```

Simply run the API server:

```shell
python3 main.py --host=0.0.0.0 --port=9989
```

Or manage this service with systemd, so that it will always start after rebooting:

```shell
echo "[Unit]
Description=ServerStat
After=syslog.target network.target
[Service]
User=root
WorkingDirectory=/root/.servstat/backend
Environment="PATH=/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin"
ExecStart=/usr/bin/python3 main.py --host=0.0.0.0 --port=9989
[Install]
WantedBy=multi-user.target" > /etc/systemd/system/serverstat.service
systemctl enable --now serverstat
```

## Building frontend

```shell
git clone https://github.com/djosix/servstat.git /tmp/servstat
cd /tmp/servstat/frontend

npm install
npm run build
```

Edit `dist/config.json`

```json
{
  "interval": 5000,
  "links": [
    "http://backend.server.ip:port/stat"
  ]
}
```

Serve the `dist/` folder using a web server, for example:

```shell
# Copy files to document root of your web server
cp -r dist/* /var/www/html/
```
