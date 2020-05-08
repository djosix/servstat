#!/usr/bin/env python3

import tornado.web
import tornado.ioloop
import tornado.httpclient
from tornado.httpclient import HTTPClientError
import tornado.gen
import json
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
    return {'info': cpu_info_data,
            'count': psutil.cpu_count(),
            'usage': psutil.cpu_percent(),
            'percent': psutil.cpu_percent(percpu=True),
            'stats': dict(psutil.cpu_stats()._asdict()),
            'freq': dict(psutil.cpu_freq()._asdict()),
            'times': dict(psutil.cpu_times()._asdict()),
            'times_percent': dict(psutil.cpu_times_percent()._asdict())}


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




def stat():
    return {'host': os.uname()[1],
            'time': time.time(),
            'cpu': cpu_info(),
            'mem': dict(psutil.virtual_memory()._asdict()),
            'swap': dict(psutil.swap_memory()._asdict()),
            'gpu': gpu_info()}
class RequestHandlerWithCROS(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(RequestHandlerWithCROS, self).__init__(*args, **kwargs)
class statHandler(RequestHandlerWithCROS):
    async def get(self, *args, **kwargs):
        self.write(json.dumps(stat(), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    import argparse, sys
    
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=9989)
    parser.add_argument('--ssl', default="false")
    parser.add_argument('--cert', default="/etc/code-server-hub/cert/ssl.pem")
    parser.add_argument('--key', default="/etc/code-server-hub/cert/ssl.key")
    args = parser.parse_args()
    
    sys.argv = [sys.argv[0]]
    app = tornado.web.Application(handlers=[
        (r'/stat', statHandler)
    ])
    ssl_options={ "certfile": args.cert,  "keyfile": args.key } if args.ssl == "true" else None
    server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
    server.bind(args.port,args.host)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
