# ServStat: Server Usage Monitoring Tool

ServStat is a robust tool designed to monitor multiple servers for CPU, memory, and GPU usage. 

![Demonstration Image](https://user-images.githubusercontent.com/17045050/81972895-dfd6bc00-9655-11ea-9e1c-bda752e6b6bc.png)

## Backend Deployment

Ensure that you are logged in as the root user. 

```shell
cd /root
git clone https://github.com/djosix/servstat.git .servstat
cd .servstat/backend

python3 -m pip install -r requirements.txt
```

To launch the API server:

```shell
python3 main.py --host=0.0.0.0 --port=9989
```

Optionally, you can manage the service with supervisor to ensure it always restarts after system reboots:

```shell
# Install supervisor
apt install supervisor

cp servstat.conf /etc/supervisor/conf.d/servstat.conf
vim /etc/supervisor/conf.d/servstat.conf # Customization allowed

systemctl reload supervisor
supervisorctl start servstat
```

## Frontend Building Process

This process has been tested with Node.js v14.16.0 and Ubuntu 20.04.

```shell
git clone https://github.com/djosix/servstat.git
cd servstat/frontend

npm install

# Add your server configuration
vim public/config.json

# Build the static site
npm run build

# Or build with a custom base path
npx vite build --base=/base/path/
```

After building, serve the `dist/` folder using a web server:

```shell
# Copy files to the document root
cp -r dist/* /var/www/html/
```

These instructions will assist you in getting a copy of the project up and running on your local machines for development and testing purposes.
