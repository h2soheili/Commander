import json
from asyncio import AbstractEventLoop

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
from typing import Optional, Callable

from app.utils.global_log import log_factory

logger = log_factory.get_logger(__name__)


class KafkaClient(object):

    def __init__(self, loop: AbstractEventLoop, url: str, topic: str, group_id: str):
        self.loop = loop
        self.lock = asyncio.Lock(loop=loop)
        self.url = url
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
        self.producer = None
        self.is_running = True

    def start(self):
        logger.info('KafkaClient start ...')
        asyncio.ensure_future(self.run_kafka())
        asyncio.ensure_future(self.consume())

    async def run_kafka(self):
        try:
            self.producer = AIOKafkaProducer(loop=self.loop,
                                             bootstrap_servers=self.url)
            await self.producer.start()
            logger.warn('producer started')
        except Exception as e:
            print(e)
        try:
            self.consumer = AIOKafkaConsumer(
                self.topic,
                loop=self.loop,
                bootstrap_servers=self.url,
                group_id=self.group_id)
            await self.consumer.start()
            logger.warn('consumer started')
        except Exception as e:
            logger.error(e)

    async def consume(self, pulling_interval: int = 1, on_new_event_received: Callable = None, auto_commit=True):
        logger.warn('self.is_running', self.is_running)
        while self.is_running:
            try:
                # some delay for decrease cpu usage
                await asyncio.sleep(pulling_interval)
                async with self.lock:
                    result = await self.consumer.getmany(timeout_ms=10 * 1000)
                    for tp, messages in result.items():
                        if messages:
                            for msg in messages:
                                logger.warn("consumed message: ", msg.value.decode())
                                if on_new_event_received is not None:
                                    on_new_event_received(msg)
                    if auto_commit:
                        await self.consumer.commit()

            except Exception as e:
                self.is_running = False
                logger.error(e)

    async def produce(self, topic: Optional[str] = None, value: str = ""):
        try:
            if not topic:
                topic = self.topic
            await self.producer.start()
            await self.producer.send_and_wait(topic, value=json.dumps(value).encode())

        except Exception as e:
            logger.error(e)
            asyncio.ensure_future(self.stop_producer())

    async def stop_producer(self):
        try:
            await self.producer.stop()
        except Exception as e:
            logger.error(e)
        self.is_running = False
