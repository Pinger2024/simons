# app/backtest_strategy.py
import backtrader as bt

class GeneticStrategy(bt.Strategy):
    params = (
        ('short_window', None),
        ('long_window', None),
        ('rsi_threshold', None),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.ma_short = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.short_window)
        self.ma_long = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.long_window)
        self.rsi = bt.indicators.RSI(self.datas[0], period=14)
        self.order = None

    def next(self):
        if self.order:
            return

        if self.ma_short[0] > self.ma_long[0] and self.rsi[0] < self.params.rsi_threshold:
            if not self.position:
                self.order = self.buy()
        elif self.ma_short[0] < self.ma_long[0]:
            if self.position:
                self.order = self.sell()

def backtest_strategy(data, best_params):
    cerebro = bt.Cerebro()
    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)
    cerebro.addstrategy(GeneticStrategy,
                        short_window=best_params[0],
                        long_window=best_params[1],
                        rsi_threshold=best_params[2])
    cerebro.broker.setcash(10000.0)
    cerebro.run()
    final_value = cerebro.broker.getvalue()
    return final_value
