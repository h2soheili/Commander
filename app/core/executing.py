from typing import Dict

from app.core.config import Settings
from app.core.process_manager import ProcessManager
from app.core.thread_manager import ThreadManager
from app.enums import StrategyTypes
from app.mock import mocked_tickers
from app.strategy.base import PriceMatchStrategy


def run_app(settings: Settings):
    tickers_range = settings.TICKERS_RANGE_TO_WATCH
    process_dict: Dict[int, ProcessManager] = dict()
    for ticker in mocked_tickers:
        ticker_key = ticker.get('key')
        if ticker_key and tickers_range[0] <= ticker_key <= tickers_range[1]:
            process = ProcessManager(ticker_key=ticker_key, process_target=generate_process_target, )
            process_dict[ticker_key] = process
            process.run()


def generate_process_target(**kwargs):
    ticker_key = kwargs.get('ticker_key')
    thread_dict: Dict[int, ThreadManager] = dict()

    """
    PriceMatching
    
    """
    price_matching_thread = ThreadManager(ticker_key=ticker_key, strategy_type=StrategyTypes.PriceMatching,
                                          process_name=kwargs.get('process_name'),
                                          thread_target=lambda **thread_kwargs: PriceMatchStrategy({}))
    thread_dict[StrategyTypes.PriceMatching.value] = price_matching_thread
    price_matching_thread.run()

    """
    VolumeMatching

    """
    volume_matching_thread = ThreadManager(ticker_key=ticker_key, strategy_type=StrategyTypes.VolumeMatching,
                                           process_name=kwargs.get('process_name'),
                                           thread_target=lambda **thread_kwargs: PriceMatchStrategy({}))
    thread_dict[StrategyTypes.VolumeMatching.value] = volume_matching_thread
    volume_matching_thread.run()
