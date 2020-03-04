# ServStat

Monitoring CPU, memory, and GPU usage of a lot of servers.

## Running backend

Use root as example

```shell
cd /root
git clone https://github.com/djosix/servstat.git .servstat
cd .servstat/backend
python3 -m pip install -r requirements.txt
```

Run server

```shell
python3 main.py --host=0.0.0.0 --port=9989 --server=gunicorn --workers=1
```

Add service to supervisor

```shell
# install supervisor
cp servstat.conf /etc/supervisor/conf.d/servstat.conf
vim /etc/supervisor/conf.d/servstat.conf # customize

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
  "interval": 5000,
  "links": [
    "http://backend.server.ip:port/stat"
  ]
}
```

Serve the `dist/` folder using a web server.
