from multiprocessing import Process
from typing import Union

from app.utils.global_log import log_factory

logger = log_factory.get_logger(__name__)


class ProcessManager(Process):
    def __init__(self, ticker_key: Union[int, str], target=None, args=tuple()):
        logger.info('process args', ticker_key=ticker_key)
        self._name = str(f"process_{ticker_key}")
        self._ticker_key = ticker_key
        super().__init__(group=None, name=self._name, target=target, args=args)

    @property
    def ticker_key(self):
        return self._ticker_key

    @ticker_key.setter
    def ticker_key(self, ticker_key: Union[int, str]):
        self._ticker_key = ticker_key

    def start(self):
        logger.info(f"process {self.name} started")
        super().start()

    def join(self, timeout=None):
        logger.info(f"process {self.name} join")
        try:
            super().join()
        except Exception as e:
            logger.error('thread join error: ', error=e)