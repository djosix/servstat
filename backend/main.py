#!/usr/bin/env python3

import bottle
import cpuinfo
import gpustat
import psutil
import time
import os
import platform


cpu_info_data = None
gpu_info_data = None
gpu_info_expires = 0


def cpu_info():
    global cpu_info_data
    if cpu_info_data is None:
        cpu_info_data = cpuinfo.get_cpu_info()
    return {'cpu_info': cpu_info_data,
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(percpu=True),
            'cpu_stats': dict(psutil.cpu_stats()._asdict()),
            'cpu_freq': dict(psutil.cpu_freq()._asdict()),
            'cpu_times': dict(psutil.cpu_times()._asdict()),
            'cpu_times_percent': dict(psutil.cpu_times_percent()._asdict())}


def gpu_info():
    global gpu_info_data, gpu_info_expires
    try:
        if gpu_info_expires < time.time():
            gpu_info_data = None
        if gpu_info_data is None:
            query_result = gpustat.new_query()
            gpu_info_data = [dict(gpu) for gpu in query_result]
            gpu_info_expires = time.time() + 5
    except:
        gpu_info_data = []
    return gpu_info_data


@bottle.get('/stat')
def stat():
    bottle.response.set_header('Access-Control-Allow-Origin', '*')
    return {'host': os.uname()[1],
            'time': time.time(),
            'cpu': cpu_info(),
            'gpu': gpu_info()}


bottle.run(server='gunicorn', host='0.0.0.0', port=9988)
