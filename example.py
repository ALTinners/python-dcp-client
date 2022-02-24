#!/usr/bin/env python3

import json
import threading
import time

from dcp import DcpClient, ResponseHandler, CountdownLatch

class MyHandler(ResponseHandler):

    def __init__(self, dcpMap, writeFile):
        ResponseHandler.__init__(self)
        self.lock = threading.Lock()
        self.count = 0
        self.dcpMap = dcpMap
        self.writeFile = writeFile

    def mutation(self, response):
        self.lock.acquire()
        print("Mutation: ", response)
        # if 'vbucket' in response and response['vbucket'] == 1009:
        #     print("At 1009")
        self.count +=1
        self.lock.release()

    def deletion(self, response):
        self.lock.acquire()
        print("Deletion: ", response)
        self.count += 1
        self.lock.release()

    def marker(self, response):
        self.lock.acquire()
        # if 'vbucket' in response and response['vbucket'] == 1009:
        #     print("At 1009")
        self.dcpMap["startSeq"][response["vbucket"]] = response["snap_start"]
        self.dcpMap["snapEnd"][response["vbucket"]] = response["snap_end"]
        # self.writeFile.seek(0)
        self.writeFile.write(json.dumps(self.dcpMap))
        # self.writeFile.truncate()
        print("Marker: ", response)
        self.lock.release()

    def stream_end(self, response):
        self.lock.acquire()
        print("Stream End: ", response)
        self.lock.release()

    def get_num_items(self):
        return self.count


def main():
    f = open("dcp_data.json", "r+")
    try:
        dcpMap = json.loads(f.read())
    except:
        keys = range(1024)
        dcpMap = {
            "startSeq": {key: 0 for key in keys},
            "snapEnd": {key: 0 for key in keys}
        }

    handler = MyHandler(dcpMap, f)
    client = DcpClient()
    client.connect('127.0.0.1', 8091, 'test_geospatial', 'swarmfarm', 'swarmfarm',
                   handler)

    failover_latch = CountdownLatch(1024)
    failover_map = dict()
    for i in range(1024):
        client.return_failover_log(i, failover_latch, failover_map)

    failover_latch.await_latch()

    for i in range(1024):
        # print(failoverLog)
        print("Doing for " + str(i))
        last_failover_log = failover_map[i]["failover_log"][0]
        vbuuid = last_failover_log[0]
        snapStart = last_failover_log[1]
        startSeq = snapStart
        snapEnd = snapStart

        if "startSeq" in dcpMap and "snapEnd" in dcpMap \
            and i in dcpMap["startSeq"] and i in dcpMap["snapEnd"]:
            startSeq = dcpMap["startSeq"][i]
            snapEnd = dcpMap["snapEnd"][i]

        if startSeq < snapStart:
            startSeq = snapStart
        if snapEnd < snapStart:
            snapEnd = snapStart

        # client.add_stream(i, 0, 21,  0xffffffffffffffff, vbuuid, snapStart, 21)
        # print(result)

        # result = client.add_stream(i, 0, 0, 10000, 0, 0, 0)
        # if result['status'] != 0:
        #     print('Stream request to vb %d failed dur to error %d' %\
        #         (i, result['status']))
        if i == 1009:
            # client.add_stream(i, 0, 0, 0xffffffffffffffff, 0, 0, 0)
            # client.add_stream(i, 0, 6, 0xffffffffffffffff, 0, 6, 6)
            # client.add_stream(i, 0, 5, 0xffffffffffffffff, 44932157266479, 5, 5)

            # client.add_stream(i, 0, 8, 0xffffffffffffffff, 44932157266479, 5, 8)
            client.add_stream(i, 0, startSeq, 0xffffffffffffffff, vbuuid, snapStart, snapEnd)
            # client.add_stream(i, 0, 8, 0xffffffffffffffff, 0, 5, 8)


        else:
            client.add_stream(i, 0, startSeq, 0xffffffffffffffff, vbuuid, snapStart, snapEnd)

    while handler.has_active_streams():
        time.sleep(.25)

    print(handler.get_num_items())
    client.close()
    # print json.dumps(client.nodes, sort_keys=True, indent=2)
    # print json.dumps(client.buckets, sort_keys=True, indent=2)


if __name__ == "__main__":
    main()
