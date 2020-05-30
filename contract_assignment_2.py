import numpy as np

np.seterr(all="ignore")
from scipy.stats import norm
from plotly.subplots import make_subplots
import plotly.graph_objects as go


class Assignment2Contract:
    plot_title = "Assignment 2 Contract"
    plotly_template = "plotly_white"
    plot_width = 1500
    plot_height = 1000

    def __init__(
        self, lower_bound, upper_bound, init_stock_price, end_time, sigma, steps_count
    ):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.sigma = sigma
        self.init_stock_price = init_stock_price
        self.end_time = end_time
        self.steps_count = steps_count
        self.sampling_points = self.end_time * self.steps_count
        self.dt = self.end_time / self.sampling_points
        self.time_grid = self._get_time_grid()

    def _get_white_noise(self):
        white_noise = np.sqrt(self.dt) * np.random.normal(
            loc=0, scale=1.0, size=self.sampling_points
        )
        return white_noise

    def _get_brownian_motion(self):
        white_noise = self._get_white_noise()
        brownian_motion = np.cumsum(white_noise)
        brownian_motion = np.append(0, brownian_motion)
        return brownian_motion

    def _get_stock_price(self):
        brownian_motion = self._get_brownian_motion()
        output = self.sigma * brownian_motion - 0.5 * self.sigma ** 2 * self.time_grid
        return self.init_stock_price * np.exp(output)

    def _get_time_grid(self):
        time_grid = np.arange(0, self.end_time + self.dt, self.dt)
        return time_grid

    def _d_minus(self, current_time, bound):
        numerator = np.log(self.stock_price / bound) - 0.5 * self.sigma ** 2 * (
            self.end_time - current_time
        )
        denominator = self.sigma * np.sqrt(self.end_time - current_time)
        return numerator / denominator

    def _get_price(self, current_time):
        d_minus_L = self._d_minus(current_time, self.lower_bound)
        d_minus_U = self._d_minus(current_time, self.upper_bound)

        price = norm.cdf(d_minus_L) - norm.cdf(d_minus_U)
        return price

    def _get_hedge(self, current_time):
        d_minus_L = self._d_minus(current_time, self.lower_bound)
        d_minus_U = self._d_minus(current_time, self.upper_bound)

        diff_pdf = norm.pdf(d_minus_L) - norm.pdf(d_minus_U)
        diff_cdf = norm.cdf(d_minus_L) - norm.cdf(d_minus_U)

        hedge_x = diff_pdf / (
            self.stock_price * self.sigma * np.sqrt(self.end_time - current_time)
        )
        hedge_y = diff_cdf - diff_pdf / (
            self.sigma * np.sqrt(self.end_time - current_time)
        )
        return hedge_x, hedge_y

    def _get_portfolio(self, current_time):
        initial_price = self.price[0]
        stock_diff = np.diff(self.stock_price, n=1)
        stock_diff = np.append(0, stock_diff)
        hedge = np.append(0, self.hedge_x)

        diff_and_hedge_cumsum = np.cumsum(stock_diff * hedge[:-1])

        portfolio = initial_price + diff_and_hedge_cumsum
        return portfolio

    def simulate(self, random_seed=42):
        np.random.seed(random_seed)
        self.stock_price = self._get_stock_price()
        self.price = self._get_price(current_time=self.time_grid)
        self.hedge_x, self.hedge_y = self._get_hedge(current_time=self.time_grid)
        self.portfolio = self._get_portfolio(current_time=self.time_grid)

    def plot(self):
        fig = make_subplots(rows=3, cols=1)
        fig.append_trace(
            go.Scatter(x=self.time_grid, y=self.stock_price, name="Stock Price"),
            row=1,
            col=1,
        ),
        fig.append_trace(
            go.Scatter(x=self.time_grid, y=self.price, name="Contract Price"),
            row=2,
            col=1,
        ),
        fig.append_trace(
            go.Scatter(x=self.time_grid, y=self.portfolio, name="Portfolio"),
            row=2,
            col=1,
        ),
        fig.append_trace(
            go.Scatter(x=self.time_grid, y=self.hedge_x, name="Hedging"), row=3, col=1,
        ),
        fig.update_layout(
            height=self.plot_height,
            width=self.plot_width,
            title_text=self.plot_title,
            template=self.plotly_template,
        )
        fig.show()
