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
        if 'vbucket' in response and response['vbucket'] == 1009:
            print("At 1009")
        # if 'key' in response and response['key'] == b"078c9e21-1d1c-48e0-a8c2-be7bbdf64435":
            # print("At Dinckehead")
        self.count +=1
        self.lock.release()

    def deletion(self, response):
        self.lock.acquire()
        print("Deletion: ", response)
        self.count += 1
        self.lock.release()

    def marker(self, response):
        self.lock.acquire()
        if 'vbucket' in response and response['vbucket'] == 1009:
            print("At 1009")
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
        print("Doing for " + str(i))
        # result = client.add_stream(i, 0, 0, 10000, 0, 0, 0)
        # if result['status'] != 0:
        #     print('Stream request to vb %d failed dur to error %d' %\
        #         (i, result['status']))
        if i == 1009:
            # client.add_stream(i, 0, 0, 0xffffffffffffffff, 0, 0, 0)
            # client.add_stream(i, 0, 6, 0xffffffffffffffff, 0, 6, 6)
            # client.add_stream(i, 0, 5, 0xffffffffffffffff, 44932157266479, 5, 5)

            # client.add_stream(i, 0, 8, 0xffffffffffffffff, 44932157266479, 5, 8)
            client.add_stream(i, 0, 8, 0xffffffffffffffff, 169396635402867, 5, 8)
            # client.add_stream(i, 0, 8, 0xffffffffffffffff, 0, 5, 8)


        else:
            client.add_stream(i, 0, 0, 10000000, 0, 0, 0)

    while handler.has_active_streams():
        time.sleep(.25)

    print(handler.get_num_items())
    client.close()
    #print json.dumps(client.nodes, sort_keys=True, indent=2)
    #print json.dumps(client.buckets, sort_keys=True, indent=2)

if __name__ == "__main__":
    main()

