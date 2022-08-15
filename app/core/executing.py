from asyncio import AbstractEventLoop
from typing import Dict, Union

from app.core.config import Settings
from app.core.loop import get_loop
from app.core.process_manager import ProcessManager
from app.core.thread_manager import ThreadManager
from app.enums import StrategyTypes, KafkaTopics
from app.mock import mocked_tickers
from app.strategy.base import PriceMatchStrategy, VolumeMatchStrategy
from app.utils.global_log import log_factory
from app.core.kafka_client import KafkaClient
import asyncio

logger = log_factory.get_logger(__name__)


def run_app(settings: Settings):
    tickers_range = settings.TICKERS_RANGE_TO_WATCH
    process_dict: Dict[int, ProcessManager] = dict()
    for ticker in mocked_tickers:
        ticker_key = ticker.get('key')
        if ticker_key and tickers_range[0] <= ticker_key <= tickers_range[1]:
            process = ProcessManager(ticker_key=ticker_key, target=generate_process_target, args=(ticker_key, settings))
            process_dict[ticker_key] = process

    for key, p in process_dict.items():
        p.start()
    # for key, p in process_dict.items():
    #     p.join()


def generate_process_target(ticker_key: Union[str, int], settings: Settings):
    # logger.info('generate_process_target args', ticker_key=ticker_key)
    thread_dict: Dict[str, ThreadManager] = dict()
    group_id = f"kafka_group_{ticker_key}"
    loop = get_loop()
    asyncio.set_event_loop(loop)

    logger.info('loop::::_>>>>    ', loop=loop)
    kafka_client = KafkaClient(loop=loop, url=settings.KAFKA_URL, group_id=group_id)
    """
    PriceMatching
    
    """
    price_matching_thread = ThreadManager(ticker_key=ticker_key, strategy_type=StrategyTypes.PriceMatching,
                                          args=(ticker_key, settings, kafka_client,),
                                          target=f1)
    thread_dict[StrategyTypes.PriceMatching.value] = price_matching_thread

    """
    VolumeMatching

    """
    volume_matching_thread = ThreadManager(ticker_key=ticker_key, strategy_type=StrategyTypes.VolumeMatching,
                                           args=(ticker_key, settings, kafka_client),
                                           target=f2)
    thread_dict[StrategyTypes.VolumeMatching.value] = volume_matching_thread
    # logger.info('thread_dict ', thread_dict=thread_dict, )

    """
        run all threads
    """
    for key, t in thread_dict.items():
        t.start()
        # t.join()
    # for key, t in thread_dict.items():
    #     t.join()
    loop.run_forever()


def f1(ticker_key: Union[str, int], settings: Settings, kafka_client: KafkaClient):
    # logger.info('PriceMatchStrategy args::::::', kafka_client=kafka_client, ticker_key=ticker_key)
    p = PriceMatchStrategy(ticker_key, settings, kafka_client)
    p.watch()


def f2(ticker_key: Union[str, int], settings: Settings, kafka_client: KafkaClient):
    # logger.info('VolumeMatchStrategy args::::::', kafka_client=kafka_client, ticker_key=ticker_key)
    p = VolumeMatchStrategy(ticker_key, settings, kafka_client)
    p.watch()
