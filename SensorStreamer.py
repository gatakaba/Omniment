# coding:utf-8

import math
import socket
import struct
import time


class SensorStreamer():

    def __init__(self, port=6151):
        host = ''        # Bind to all interfaces
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(10**-3)
        self.s.bind((host, port))
        self.old_val = [0] * 9

    def get_data(self):
        message = None
        while True:
            try:
                message, address = self.s.recvfrom(2**20)
            except socket.timeout:
                break
            except Exception as e:
                print(e)
        if not message is None:
            ax = struct.unpack('f', message[4:8])[0]
            ay = struct.unpack('f', message[8:12])[0]
            az = struct.unpack('f', message[12:16])[0]

            gx = struct.unpack('f', message[16:20])[0]
            gy = struct.unpack('f', message[20:24])[0]
            gz = struct.unpack('f', message[24:28])[0]

            mx = struct.unpack('d', message[28:36])[0]
            my = struct.unpack('d', message[36:44])[0]
            mz = struct.unpack('d', message[44:52])[0]
            self.old_val = [ax, ay, az, gx, gy, gz, mx, my, mz]
            return [ax, ay, az, gx, gy, gz, mx, my, mz]
        else:
            return self.old_val

if __name__ == "__main__":
    ss = SensorStreamer()
    while True:
        ax, ay, az, gx, gy, gz, mx, my, mz = ss.get_data()
        print(ss.get_data())
        time.sleep(0.1)
