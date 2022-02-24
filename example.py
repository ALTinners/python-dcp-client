#!/usr/bin/env python3

import json
import threading
import time

from dcp import DcpClient, ResponseHandler


class MyHandler(ResponseHandler):

    def __init__(self):
        ResponseHandler.__init__(self)
        self.lock = threading.Lock()
        self.count = 0

    def mutation(self, response):
        self.lock.acquire()
        print("Mutation: ", response)
        self.count +=1
        self.lock.release()

    def deletion(self, response):
        self.lock.acquire()
        print("Deletion: ", response)
        self.count += 1
        self.lock.release()

    def marker(self, response):
        self.lock.acquire()
        print("Marker: ", response)
        self.lock.release()

    def stream_end(self, response):
        self.lock.acquire()
        print("Stream End: ", response)
        self.lock.release()

    def get_num_items(self):
        return self.count


def main():
    handler = MyHandler()
    client = DcpClient()
    client.connect('127.0.0.1', 8091, 'test_geospatial', 'swarmfarm', 'swarmfarm',
                   handler)
    for i in range(1024):
        failoverLog = client.return_failover_log(i)
        # print(failoverLog)
        last_failover_log = failoverLog["failover_log"][0]
        vbuuid = last_failover_log[0]
        snapStart = last_failover_log[1]
        result = client.add_stream(i, 0, 21,  0xffffffffffffffff, vbuuid, snapStart, 21)
        # print(result)
    
    while handler.has_active_streams():
        time.sleep(.25)

    print(handler.get_num_items())
    client.close()
    # print json.dumps(client.nodes, sort_keys=True, indent=2)
    # print json.dumps(client.buckets, sort_keys=True, indent=2)


if __name__ == "__main__":
    main()
