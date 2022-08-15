import os
import time
from threading import Thread
from typing import Union

from app.enums import StrategyTypes
from app.utils.global_log import log_factory

logger = log_factory.get_logger(__name__)


class ThreadManager(Thread):
    def __init__(self, ticker_key: Union[int, str], strategy_type: StrategyTypes, target=None, args=tuple()):
        # logger.info('thread args', ticker_key=ticker_key, strategy_type=strategy_type.value, args=args)
        self._name = f"thread_{ticker_key}_{strategy_type.value}"
        self._ticker_key = ticker_key
        self._strategy_type = strategy_type
        super().__init__(group=None, name=self._name, target=target, args=args)

    @property
    def ticker_key(self):
        return self._ticker_key

    @ticker_key.setter
    def ticker_key(self, ticker_key: Union[int, str]):
        self._ticker_key = ticker_key

    @property
    def strategy_type(self):
        return self._strategy_type

    @strategy_type.setter
    def strategy_type(self, strategy_type: StrategyTypes):
        self._strategy_type = strategy_type

    def start(self):
        super().start()
        logger.info(f"thread {self.name} in {self.ticker_key} started  pid:{os.getpid()}   tid:{self.ident}")

    def join(self, timeout=None):
        logger.info(f"thread {self.name} process:{self.ticker_key} join")
        try:
            super().join()
        except Exception as e:
            logger.error('thread join error: ', error=e)
