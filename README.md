# ServStat

Monitoring CPU, memory, and GPU usage of multiple servers.

![Demo Image](https://user-images.githubusercontent.com/17045050/76153224-2c58c500-6104-11ea-8ca1-dd9f2c1b2e37.png)

## Running backend

Use root as example:

```shell
cd /etc
git clone https://github.com/HuJK/servstat.git servstat
cd servstat/backend

python3 -m pip install -r requirements.txt
```

Simply run the API server:

```shell
python3 main.py --host=0.0.0.0 --port=9989
```

Or manage this service with systemd, so that it will always start after rebooting:

```shell
cd /etc
git clone https://github.com/HuJK/servstat.git servstat
cd servstat/backend
bash install.sh
```

## Building frontend

```shell
git clone https://github.com/HuJK/servstat.git servstat
cd servstat/frontend

npm install
npm run build
```

Edit `dist/config.json`

```json
{
    "interval": 10000,
    "links": [
        ["Server 01","https://api.server01.example.com:9989/api", "https://url.server01.example.com"] ,
        ["Server 02","https://api.server02.example.com:9989/api"]
    ]
}
```

Serve the `dist/` folder using a web server, for example:

```shell
# Copy files to document root of your web server
cp -r dist/* /var/www/html/
```
