import numpy as np
from scipy.stats import norm
from plotly.subplots import make_subplots
import plotly.graph_objects as go


class EuropeanCallOption:
    plot_title = "European Call Option"
    plotly_template = "plotly_white"
    plot_width = 1500
    plot_height = 1000

    def __init__(self, strike_price, end_time, sigma, steps_count):
        self.strike_price = strike_price
        self.end_time = end_time
        self.sigma = sigma
        self.steps_count = steps_count
        self.sampling_points = self.end_time * self.steps_count
        self.dt = self.end_time / self.sampling_points
        self.time_grid = self._get_time_grid()

    def _get_time_grid(self):
        time_grid = np.arange(0, self.end_time + self.dt, self.dt)
        return time_grid

    def _d_plus(self, stock_price, current_time):
        numerator = np.log(stock_price / self.strike_price) + (self.sigma ** 2 / 2) * (
            self.end_time - current_time
        )
        denominator = self.sigma * np.sqrt(self.end_time - current_time)
        return numerator / denominator

    def _d_minus(self, stock_price, current_time):
        numerator = np.log(stock_price / self.strike_price) - (self.sigma ** 2 / 2) * (
            self.end_time - current_time
        )
        denominator = self.sigma * np.sqrt(self.end_time - current_time)
        return numerator / denominator

    def _get_price(self, stock_price, current_time):
        d_plus = self._d_plus(stock_price, current_time)
        d_minus = self._d_minus(stock_price, current_time)
        return norm.cdf(d_plus) * stock_price - self.strike_price * norm.cdf(d_minus)

    def _get_hedge(self, stock_price, current_time):
        d_plus = self._d_plus(stock_price, current_time)
        return norm.cdf(d_plus)

    def _get_portfolio(self, stock_price):
        initial_price = self.price[0]
        diff = np.diff(stock_price, n=1)
        diff_and_hedge_cumsum = np.cumsum(diff * self.hedge[:-1])
        diff_and_hedge_cumsum = np.append(0, diff_and_hedge_cumsum)
        portfolio = initial_price + diff_and_hedge_cumsum
        return portfolio

    def simulate(self, stock_price, random_seed=42):
        np.random.seed(random_seed)
        self.price = self._get_price(
            stock_price=stock_price, current_time=self.time_grid
        )
        self.hedge = self._get_hedge(
            stock_price=stock_price, current_time=self.time_grid
        )
        self.portfolio = self._get_portfolio(stock_price=stock_price)

    def plot(self):
        fig = make_subplots(rows=2, cols=1)
        fig.append_trace(
            go.Scatter(x=self.time_grid, y=self.price, name="Price"), row=1, col=1,
        ),
        fig.append_trace(
            go.Scatter(x=self.time_grid, y=self.hedge, name="Hedging",), row=2, col=1,
        ),
        fig.append_trace(
            go.Scatter(x=self.time_grid, y=self.portfolio, name="Portfolio"),
            row=1,
            col=1,
        ),
        fig.update_layout(
            height=self.plot_height,
            width=self.plot_width,
            title_text=self.plot_title,
            template=self.plotly_template,
        )
        fig.show()
