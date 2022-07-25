from abc import ABC, abstractmethod

from app.core.kafka_client import KafkaClient
from app.enums import StrategyTypes, EventTypes, KafkaTopics
from app.interfaces import Event


class AbstractOrderPlacementStrategy(ABC):
    def __init__(self, key: str, name: str, strategy_type: StrategyTypes):
        self.key = key
        self.name = name
        self.strategy_type = strategy_type

    @abstractmethod
    def implement_logic(self):
        pass

    @staticmethod
    def generate_event(event_type: EventTypes, parent_order_key: int, order_key: int):
        return Event(event_type, parent_order_key, order_key)


class PriceMatchStrategy(AbstractOrderPlacementStrategy):
    def __init__(self, kafka_client: KafkaClient):
        AbstractOrderPlacementStrategy.__init__(self, key='price-match', name='price-match-order-placement',
                                                strategy_type=StrategyTypes.PriceMatching)
        self.kafka_client = KafkaClient

    def implement_logic(self):
        # self.kafka_client.consume()
        '''

            if some logic happens
            trigger event

        '''
        self.kafka_client.produce(KafkaTopics.OrderExecution.value,
                                  PriceMatchStrategy.generate_event(EventTypes.Buy, 10, 222));


class VolumeMatchStrategy(AbstractOrderPlacementStrategy):
    def __init__(self, kafka_client: KafkaClient):
        AbstractOrderPlacementStrategy.__init__(self, key='volume-match', name='volume-match-order-placement',
                                                strategy_type=StrategyTypes.VolumeMatching)
        self.kafka_client = KafkaClient

    def implement_logic(self):
        # self.kafka_client.consume()
        '''

            if some logic happens
            trigger event

        '''
        self.kafka_client.produce(KafkaTopics.OrderExecution.value,
                                  PriceMatchStrategy.generate_event(EventTypes.Buy, 10, 222));
