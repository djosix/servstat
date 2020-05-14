# ServStat

Monitoring CPU, memory, and GPU usage of multiple servers.

![Demo Image](https://user-images.githubusercontent.com/17045050/81972895-dfd6bc00-9655-11ea-9e1c-bda752e6b6bc.png)

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

Or manage this service with supervisor, so that it will always start after rebooting:

```shell
# Install supervisor
apt install supervisor # using your package manager

cp servstat.conf /etc/supervisor/conf.d/servstat.conf
vim /etc/supervisor/conf.d/servstat.conf # customize your service

systemctl reload supervisor
supervisorctl start servstat
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
  "title": "Any Optional Title",
  "interval": 5000,
  "servers": [
    "http://backend.server.ip:port/stat",
    {
      "name": "Any Optional Server Name",
      "link": "http://another.backend.server.ip:port/stat",
    }
  ]
}
```

Serve the `dist/` folder using a web server, for example:

```shell
# Copy files to document root of your web server
cp -r dist/* /var/www/html/
```
