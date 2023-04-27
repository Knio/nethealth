'''

'''

import argparse
import binascii
import collections
import dataclasses
import logging
import time
import threading
import sys
import socket
import struct


LOG = logging.getLogger(__name__)

def checksum(bytes):
  if len(bytes) & 1:
    m = memoryview(bytes)[:-1].cast('@H')
    s = bytes[-1]
  else:
    m = memoryview(bytes).cast('@H')
    s = 0

  s += sum(m)
  s += (s >> 16)
  s = (~s) & 0xffff
  return struct.pack('@H', s)

@dataclasses.dataclass
class IcmpPing:
  FORMAT = '!BB2BHH'
  FORMAT_LEN = struct.calcsize(FORMAT)

  typ: int
  code: int
  checksum: bytes = dataclasses.field(kw_only=True, default=b'\0\0')
  identifier: int
  sequence: int
  data: bytes

  def __bytes__(self):
    b1 = struct.pack(self.FORMAT,
        self.typ,
        self.code,
        self.checksum[0],
        self.checksum[1],
        self.identifier,
        self.sequence,
    ) + self.data
    self.checksum = checksum(b1)
    b2 = struct.pack(self.FORMAT,
        self.typ,
        self.code,
        self.checksum[0],
        self.checksum[1],
        self.identifier,
        self.sequence,
    ) + self.data
    return b2


  @classmethod
  def from_bytes(cls, data):
    args = struct.unpack(cls.FORMAT, data[:cls.FORMAT_LEN])
    return IcmpPing(*args, data=data[cls.FORMAT_LEN:])



class NetHealth:
  pings = collections.defaultdict(list)

  def __init__(self, args) -> None:
    self.socket = socket.socket(
      socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    # TODO accept bind addr arg
    self.socket.bind(('0.0.0.0', 0))

  def ping(self, ip, i, s):
    p = IcmpPing(typ=8, code=0, identifier=i, sequence=s, data=b'Hello World')
    self.socket.sendto(bytes(p), (ip, 1))

  def start(self):
    self.running = True
    self.thread = threading.Thread(target=self.run)
    self.thread.daemon = True
    self.thread.start()

  def stop(self):
    self.running = False
    self.thread.join()

  def run(self):
    i = 0xfef0
    s = 0
    while self.running:
      try:
        s += 1
        self.ping('142.250.64.238', i, s)
      except:
        LOG.exception('Error in NetHealth loop')
      time.sleep(1)

class NetTui:
  def __init__(self, nh, args):
    self.nh = nh

  def run(self):
    while 1:
      print("Hello world!")
      time.sleep(1)


def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter, description=__doc__)

  args = parser.parse_args()
  nh = NetHealth(args)
  nh.start()

  tui = NetTui(nh, args)
  tui.run()


if __name__ == '__main__':
  main()