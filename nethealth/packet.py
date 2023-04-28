
import dataclasses
import struct


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

