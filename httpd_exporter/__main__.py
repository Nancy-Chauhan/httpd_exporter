import os
import re
from time import sleep

from prometheus_client import start_http_server, Counter


def main():
    start_http_server(8000)
    gather_metrics()


def gather_metrics():
    print("collecting httpd metrics")
    regex = r"\d+\.\d+\.\d+\.\d+ - \S+ \[.*\] \".*?\" (\d+) (\d+|-).*"
    request_counter = Counter('httpd_requests', 'http request', ["status_code"])
    bytes_sent = Counter('httpd_bytes_sent', 'Total bytes sent by httpd')
    for line in follow_log("/var/log/apache2/access.log"):
        match = re.match(regex, line)
        if match:
            print("updating values")
            status_code = int(match.group(1))
            request_counter.labels(status_code=status_code).inc()
            if match.group(2) != "-":
                size = int(match.group(2))
                bytes_sent.inc(size)
        else:
            print("line did not match", line)


def follow_log(file):
    with open(file, 'r') as f:
        f.seek(0, os.SEEK_END)
        # infinite loop
        while True:
            line = f.readline()
            if not line:
                sleep(0.1)
                continue

            yield line


if __name__ == '__main__':
    main()
