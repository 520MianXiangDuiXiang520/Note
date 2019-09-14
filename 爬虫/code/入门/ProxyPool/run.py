from .GetProxy import GetProxy
from .is_usable import IsUsable
from time import sleep

POLL = set([])


class ProxyPool:
    def get(self):
        while True:
            POLL.add(GetProxy().get_proxy0())
            sleep(8)

