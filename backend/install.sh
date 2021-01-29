pip3 install py-cpuinfo gpustat psutil tornado gunicorn
ln -s /etc/servstat/backend/serverstat.service /etc/systemd/system/serverstat.service 
systemctl enable --now serverstat
systemctl start serverstat
