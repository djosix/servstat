# ServStat

Monitoring CPU, memory, and GPU usage of a lot of servers.

## Running backend

```shell
git clone https://github.com/djosix/servstat.git
cd backend
python3 -m pip install -r requirements.txt
python3 main.py # default host=0.0.0.0 port=9989
```

## Building frontend

```shell
git clone https://github.com/djosix/servstat.git
cd frontend
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
