import os
import threading
from threading import Thread
from app.enums import StrategyTypes


class ThreadManager:
    def __init__(self, ticker_key: int, strategy_type: StrategyTypes, process_name: str, thread_target):
        self.ticker_key = ticker_key
        self.strategy_type = strategy_type
        self.process_name = process_name
        self.thread_name = f"thread_${ticker_key}_${strategy_type.value}"
        self.thread = Thread(target=thread_target, args=(),
                             kwargs={"ticker_key": ticker_key, "strategy_type": self.strategy_type,
                                     "process_name": self.process_name},
                             name=self.thread_name)

    def run(self):
        self.thread.start()
        print('_________________________')
        print(f"thread {self.thread_name} process:{self.process_name} started")
        print(f"process id: {os.getpid()}")
        print(f"thread id: {threading.get_native_id()}")
        print('_________________________')

    def finish(self):
        self.thread.join()
        print(f"thread {self.thread_name} process:{self.process_name} join")
