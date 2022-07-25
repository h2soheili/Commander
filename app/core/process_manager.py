from multiprocessing import Pool, Process


class ProcessManager:
    def __init__(self, ticker_key: int, process_target):
        self.ticker_key = ticker_key
        self.process_name = f"process_${ticker_key}"
        self.process = Process(target=process_target,
                               args=(),
                               kwargs={"ticker_key": self.ticker_key, "process_name": self.process_name},
                               name=self.process_name)

    def run(self):
        self.process.start()
        print(f"process {self.process_name} started")

    def finish(self):
        self.process.join()
        print(f"process {self.process_name} join")
