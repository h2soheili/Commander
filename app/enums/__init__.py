from enum import Enum


class StrategyTypes(Enum):
    PriceMatching = 1
    VolumeMatching = 2
    VolumeFiling = 3


class EventTypes(Enum):
    Buy = 1
    Sell = 2
    Stop = 3
    CancelParentOrder = 4
    CancelOrder = 5
    EditPrice = 6
    EditVolume = 7
    OrderIsDone = 9
    SuspendSystem = 8


class KafkaTopics(Enum):
    OrderExecution = 'ir.mofid.sub.order.execution'
    MarketData = 'ir.mofid.sub.market.data'
