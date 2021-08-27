# ServStat

Monitoring CPU, memory, and GPU usage of multiple servers.

![Demo Image](https://user-images.githubusercontent.com/17045050/81972895-dfd6bc00-9655-11ea-9e1c-bda752e6b6bc.png)

## Running backend

Using root user.

```shell
cd /root
git clone https://github.com/djosix/servstat.git .servstat
cd .servstat/backend

python3 -m pip install -r requirements.txt
```

Directly run the API server:

```shell
python3 main.py --host=0.0.0.0 --port=9989
```

Or manage this service with supervisor, so it always starts after system reboot:

```shell
# Install supervisor
apt install supervisor

cp servstat.conf /etc/supervisor/conf.d/servstat.conf
vim /etc/supervisor/conf.d/servstat.conf # you can customize this

systemctl reload supervisor
supervisorctl start servstat
```

## Building frontend

Tested on Node.js v14.16.0 and Ubuntu 20.04.

```shell
git clone https://github.com/djosix/servstat.git
cd servstat/frontend

npm install

# Add your servers
vim public/config.json

# Build static site
npm run build

# Or build with another base path
npx vite build --base=/base/path/
```

Serve the `dist/` folder using a web server, for example:

```shell
# Copy files to document root
cp -r dist/* /var/www/html/
```
