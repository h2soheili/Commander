from typing import List


def setup_database_queries() -> List[str]:
    create_order = '''CREATE TABLE IF NOT EXISTS Order(
        Key INT(11),
        Volume DECIMAL(12,4),
        Price DECIMAL(12,4),
        StrategyType SMALLINT(2),
        OrderType SMALLINT(2),
        UserId INT(11),
        State SMALLINT(2),
        TimeToLive DATETIME
    )'''

    create_ticker = '''CREATE TABLE IF NOT EXISTS Ticker(
            Key INT(11),
            Symbol CHAR(120),
            State SMALLINT(2),
        )'''

    create_process = '''CREATE TABLE IF NOT EXISTS Process(
            Key INT(11) PRIMARY KEY,
            LocalId INT(11),
            State SMALLINT(2),
        )'''

    create_process_ticker = '''CREATE TABLE IF NOT EXISTS ProcessTicker(
                Key INT(11) PRIMARY KEY,
                ProcessKey INT(11),
                TickerKey INT(11),
                State SMALLINT(2),
            )'''

    create_index_order = 'CREATE INDEX idx_order_id ON order(Key)'
    create_index_ticker = 'CREATE INDEX idx_ticker_id ON ticker(Key)'
    create_index_process = 'CREATE INDEX idx_order_id ON process(Key)'
    create_index_process_ticker = 'CREATE INDEX idx_order_id ON process_ticker(Key)'

    return [create_order, create_ticker, create_process, create_process_ticker, create_index_order,
            create_index_ticker, create_index_process, create_index_process_ticker]