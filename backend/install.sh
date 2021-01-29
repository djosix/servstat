pip3 install py-cpuinfo gpustat psutil tornado gunicorn
ln -s /etc/systemd/system/serverstat.service /etc/servstat/backend/serverstat.service
systemctl enable --now serverstat
systemctl start serverstat
