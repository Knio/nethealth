'''

'''

import argparse
import collections
import dataclasses
import logging
import time
import threading
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
class Ipv4:
  FORMAT = '!BBHHHBB2s4s4s'
  FORMAT_LEN = struct.calcsize(FORMAT)
  version: int
  ihl: int
  tos: int
  total_length: int
  identification: int
  flags: int
  fragment_offset: int
  ttl: int
  protocol: int
  checksum: bytes = dataclasses.field(kw_only=True, default=b'\0\0')
  src: int
  dst: int
  options: bytes

  def __bytes__(self):
    for i in range(2):
      version_ihl = (self.version << 4) | self.ihl
      flags_frag = (self.flags << 3) | self.fragment_offset
      b = struct.pack(self.FORMAT,
        version_ihl,
        self.tos,
        self.total_length,
        self.identification,
        flags_frag,
        self.ttl,
        self.protocol,
        self.checksum,
        self.src,
        self.dst,
      ) + self.options
      self.checksum = checksum(b)
    return b

  @classmethod
  def from_bytes(cls, bytes):
    (
      version_ihl,
      tos,
      total_length,
      identification,
      flags_frag,
      ttl,
      protocol,
      checksum,
      src,
      dst,
    ) = struct.unpack(cls.FORMAT, bytes[:cls.FORMAT_LEN])
    return cls(
      version=version_ihl >> 4,
      ihl=version_ihl & 0x0f,
      tos=tos,
      total_length=total_length,
      identification=identification,
      flags=flags_frag >> 13,
      fragment_offset=flags_frag & 0x1fff,
      ttl=ttl,
      protocol=protocol,
      checksum=checksum,
      src=src,
      dst=dst,
      options=bytes[cls.FORMAT_LEN:],
    )


@dataclasses.dataclass
class IcmpPing:
  FORMAT = '!BB2sHH'
  FORMAT_LEN = struct.calcsize(FORMAT)

  typ: int
  code: int
  checksum: bytes = dataclasses.field(kw_only=True, default=b'\0\0')
  identifier: int
  sequence: int
  data: bytes

  def __bytes__(self):
    for i in range(2):
      b = struct.pack(self.FORMAT,
        self.typ,
        self.code,
        self.checksum,
        self.identifier,
        self.sequence,
      ) + self.data
      self.checksum = checksum(b)
    return b


  @classmethod
  def from_bytes(cls, data):
    (
      typ, code, checksum,
      identifier, sequence
    ) = struct.unpack(cls.FORMAT, data[:cls.FORMAT_LEN])
    return cls(
      typ=typ, code=code, checksum=checksum,
      identifier=identifier, sequence=sequence,
      data=data[cls.FORMAT_LEN:])


@dataclasses.dataclass
class Ping:
  send_time: float = dataclasses.field(kw_only=True, default=0)
  recv_time: float = dataclasses.field(kw_only=True, default=0)
  seq: int = dataclasses.field(kw_only=True, default=0)
  send_ip: str = dataclasses.field(kw_only=True, default='')
  recv_ip: str = dataclasses.field(kw_only=True, default='')

  @property
  def lag(self):
    return self.recv_time - self.send_time


class NetHealth:
  host = collections.defaultdict(list)
  pings = {}


  def __init__(self, args) -> None:
    self.socket = socket.socket(
      socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    # TODO accept bind addr arg
    self.socket.bind(('0.0.0.0', 0))

  def ping(self, ip, i, s):
    p = Ping(
      seq=s,
      send_time=time.time(),
      send_ip=ip,
    )
    self.pings[p.seq] = p
    icmp = IcmpPing(typ=8, code=0, identifier=i, sequence=s, data=b'Hello World')
    self.socket.sendto(bytes(icmp), (ip, 1))

  def start(self):
    self.running = True
    self.thread = threading.Thread(target=self.run)
    self.thread.daemon = True
    self.thread.start()
    self.recv_thread = threading.Thread(target=self.run_recv)
    self.recv_thread.daemon = True
    self.recv_thread.start()

  def stop(self):
    self.running = False
    self.thread.join()
    self.recv_thread.join()

  def run(self):
    i = 0xfef0
    s = 0
    while self.running:
      try:
        s += 1
        self.ping('142.250.64.238', i, s)
        time.sleep(0.1)
      except:
        LOG.exception('Error in NetHealth loop')
        time.sleep(1)

  def run_recv(self):
    while self.running:
      try:
        self.recv()
      except:
        LOG.exception('Error in NetHealth recv loop')
        time.sleep(1)

  def recv(self):
    data, host = self.socket.recvfrom(512)
    # print((data, host))
    try:
      ip_header = Ipv4.from_bytes(data[:20])
      # print(ip_header)
      # TODO read header first
      p = IcmpPing.from_bytes(data[20:])
      # print(p)
      rq = self.pings.pop(p.sequence, None)
      if not rq:
        LOG.error("got echo reply we did not requst")
      else:
        rq.recv_time = time.time()
        rq.recv_ip = ip_header.src
        self.host[rq.send_ip].append(rq)
    except:
      LOG.exception('failed to parse IcmpPing')


class Dataset:
  def __init__(self, data) -> None:
    self.data = list(data)
    self.max = 1
    self.min = 0
    if self.data:
      self.max = max(self.data)
      self.min = min(self.data)

  def as_graph(self):
    blocks = '▁▂▃▄▅▆▇'
    return ''.join(blocks[int((len(blocks) - 1) * x / self.max)] for x in self.data)




class NetTui:
  def __init__(self, nh, args):
    self.nh = nh

  def run(self):
    while 1:
      # print("Hello world!")
      for host, rqs in self.nh.host.items():
        ds = Dataset(r.lag for r in rqs[-40:])
        # print SOL
        print('\033[F')
        print(f'{host}: {ds.as_graph()} [max: {ds.max * 1000:.0f}, min: {ds.min * 1000:.0f}]', end='')


      time.sleep(0.05)


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