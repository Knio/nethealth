import logging

from . import nethealth


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  nethealth.main()
