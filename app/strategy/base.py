import time
from abc import ABC, abstractmethod
from typing import Union, Any
import asyncio
from app.core.config import Settings
from app.core.kafka_client import KafkaClient
from app.enums import StrategyTypes, EventTypes, KafkaTopics
from app.interfaces import Event
from app.utils.global_log import log_factory

logger = log_factory.get_logger(__name__)


class AbstractOrderPlacementStrategy(ABC):
    is_running = True

    def __init__(self, ticker_key: Union[str, int], settings: Settings, kafka_client: KafkaClient, key: str, name: str,
                 strategy_type: StrategyTypes):
        self.ticker_key = ticker_key
        self.settings = settings
        self.kafka_client = kafka_client
        self.key = key
        self.name = name
        self.strategy_type = strategy_type

    @abstractmethod
    def implement_logic(self):
        pass

    @staticmethod
    def generate_event(event_type: EventTypes, parent_order_key: int, order_key: int):
        return Event(event_type, parent_order_key, order_key)

    def watch(self):
        # pass
        # self.kafka_client.start()
        # logger.info('loop is here', loop=self.kafka_client.loop)
        # asyncio.set_event_loop(self.kafka_client.loop)
        # asyncio.ensure_future(self.kafka_client.start_consumer(), loop=self.kafka_client.loop)
        # asyncio.set_event_loop(self.kafka_client.loop)
        # loop = self.kafka_client.loop
        # loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.run_consumer(), loop=self.kafka_client.loop)
        # self.kafka_client.loop.run_forever()
        # self.kafka_client.loop.run_until_complete(self.kafka_client.start_consumer(KafkaTopics.StartTickerWatcher))
        # self.kafka_client.loop.run_until_complete(self.kafka_client.start_consumer())
        # self.kafka_client.loop.run_until_complete(self.kafka_client.consume(3, self.on_new_event_received, False))
        # self.kafka_client.loop.run_until_complete(self.kafka_client.consume(3, self.on_new_event_received, False))

    async def run_consumer(self):
        await self.kafka_client.start_consumer(KafkaTopics.StartTickerWatcher)
        await self.kafka_client.consume(3, lambda event: self.on_new_event_received(event=event), False)

    def on_new_event_received(self, event: Any):
        logger.info('new event: ', ticker_key=self.ticker_key, key=self.key, strategy_type=self.strategy_type,
                    event=event)

    # @abstractmethod
    # def on_start(self):
    #     pass


class PriceMatchStrategy(AbstractOrderPlacementStrategy):
    def __init__(self, ticker_key: Union[str, int], settings: Settings, kafka_client: KafkaClient):
        super().__init__(ticker_key, settings, kafka_client, key='price-match', name='price-match-order-placement',
                         strategy_type=StrategyTypes.PriceMatching)

    def implement_logic(self):
        # self.kafka_client.consume()
        '''

            if some logic happens
            trigger event

        '''
        self.kafka_client.produce(KafkaTopics.OrderExecution.value,
                                  PriceMatchStrategy.generate_event(EventTypes.Buy, 10, 222))


class VolumeMatchStrategy(AbstractOrderPlacementStrategy):
    def __init__(self, ticker_key: Union[str, int], settings: Settings, kafka_client: KafkaClient):
        super().__init__(ticker_key, settings, kafka_client, key='volume-match', name='volume-match-order-placement',
                         strategy_type=StrategyTypes.VolumeMatching)

    def implement_logic(self):
        # self.kafka_client.consume()
        '''

            if some logic happens
            trigger event

        '''
        self.kafka_client.produce(KafkaTopics.OrderExecution.value,
                                  PriceMatchStrategy.generate_event(EventTypes.Buy, 10, 222));
