'''

'''

import argparse
import collections
import dataclasses
import logging
import random
import time
import threading
import socket

from . import term
from . import packet

LOG = logging.getLogger(__name__)


@dataclasses.dataclass
class Ping:
  send_time: float = dataclasses.field(kw_only=True, default=0)
  recv_time: float = dataclasses.field(kw_only=True, default=0)
  id: tuple = dataclasses.field(kw_only=True, default=0)
  send_ip: str = dataclasses.field(kw_only=True, default='')
  recv_ip: str = dataclasses.field(kw_only=True, default='')

  @property
  def lag(self):
    return self.recv_time - self.send_time

  @property
  def status(self):
    return self.recv_time > 1

class NetHealth:
  host = collections.defaultdict(list)
  pings = {}


  def __init__(self, args) -> None:
    self.socket = socket.socket(
      socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    # TODO accept bind addr arg
    self.socket.bind(('0.0.0.0', 0))

    self.hosts = [
      '172.17.64.1',
      '142.250.64.238',
      '172.217.2.206',
      '8.8.8.8',
      '54.186.50.116',
    ]

  def ping(self, ip, i, s):
    p = Ping(
      id=(i, s),
      send_time=time.time(),
      send_ip=ip,
    )
    self.pings[p.id] = p
    self.host[ip].append(p)
    icmp = packet.IcmpPing(typ=8, code=0, identifier=i, sequence=s, data=b'Hello World')
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
    start = time.time()
    interval = 0.1
    count = 0
    while self.running:
      try:
        for h in self.hosts:
          i = random.getrandbits(16)
          s = random.getrandbits(16)
          self.ping(h, i, s)
      except:
        LOG.exception('Error in NetHealth loop')
        count += 9
      count += 1
      time.sleep(start + count * interval - time.time())

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
      ip_header = packet.Ipv4.from_bytes(data[:20])
      # print(ip_header)
      # TODO read header first
      p = packet.IcmpPing.from_bytes(data[20:])
      # print(p)
      rq = self.pings.pop((p.identifier, p.sequence), None)
      if not rq:
        LOG.error("got echo reply we did not requst")
      else:
        rq.recv_time = time.time()
        rq.recv_ip = ip_header.src
        # LOG.info(rq)
        # self.host[rq.send_ip].append(rq)
    except:
      LOG.exception('failed to parse IcmpPing')


class Dataset:
  def __init__(self, data) -> None:
    self.data = list(data)
    self.max = 0
    self.min = 1
    self.sum = 0
    self.n = 0
    for d in self.data:
      if d.status:
        l = d.lag
        self.n += 1
        self.sum += l
        self.max = max(self.max, l)
        self.min = min(self.min, l)
    if self.max == 0:
      self.max = 1

  def as_graph(self):
    blocks = '▁▂▃▄▅▆▇'
    s = []
    for d in self.data:
      if d.status:
        l = d.lag
        m = l / self.max
        s.append(term.ANSI.color_fg8(term.ANSI.COLOR8.CYAN))
        s.append(blocks[int((len(blocks) - 1) * m)])
      else:
        s.append(term.ANSI.color_fg8(term.ANSI.COLOR8.RED))
        s.append('━')
    s.append(term.ANSI.graphics_reset())
    return ''.join(s)




class NetTui:
  def __init__(self, nh, args):
    self.nh = nh

  def run(self):
    while 1:
      print(term.ANSI.cursor_pos(1, 1), end='')
      for host, rqs in list(self.nh.host.items()):
        ds = Dataset(rqs[-60:])
        print(f'{host:>20}: {ds.as_graph()}', end='')
        print(term.ANSI.erase_line(0), end='')
        print(term.ANSI.cursor_column(85), end='')
        print(f'[max: {ds.max * 1000:3.0f}, min: {ds.min * 1000:3.0f}]', end='')
        print(term.ANSI.erase_line(0))
      print(term.ANSI.erase_display(0), end='')

      time.sleep(0.05)


def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter, description=__doc__)

  args = parser.parse_args()
  nh = NetHealth(args)
  nh.start()

  tui = NetTui(nh, args)
  tui.run()

