# coding = utf-8
import warnings
import itertools
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


class arimaClass:
    start = '2016-01-01'
    obse_time = '2016'
    pred_time = '2016-08-01'
    pred_steps = 2

    # ARIMA model 类模块
    def __init__(self):
        super(arimaClass, self).__init__()

    def step1(self, hist_data):
        # 加载数据文件并保存为DataFrame
        df = pd.read_csv(hist_data, header=0, index_col=0, parse_dates=True, sep=',')
        y = df['runtime'].resample('MS').mean()
        y.plot(figsize=(15, 6))
        plt.show()
        return y

    def step23(self, y):
        # Step 2 — Parameter Selection for the ARIMA Time Series Model
        # Define the p, d and q parameters to take any value between 0 and 2
        p = d = q = range(0, 2)

        # Generate all different combinations of p, q and q triplets
        pdq = list(itertools.product(p, d, q))

        # Generate all different combinations of seasonal p, q and q triplets
        # seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
        # seasonal_pdq = [(x[0], x[1], x[2], 30) for x in list(itertools.product(p, d, q))]
        # print('Examples of parameter combinations for Seasonal ARIMA...')
        # print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
        # print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
        # print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
        # print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))
        warnings.filterwarnings("ignore") # specify to ignore warning messages
        for param in pdq:
            # for param_seasonal in seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    # seasonal_order=param_seasonal,
                                                    enforce_stationarity=True,
                                                    enforce_invertibility=True)

                    results = mod.fit()
                    # print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                    print('ARIMA{} - AIC:{}'.format(param, results.aic))
                    # return 'ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic)
                except:
                    continue

        # Step 3 — Fitting an ARIMA Time Series Model
        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=(1, 1, 1),
                                        # seasonal_order=(1, 1, 1, 30),
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)

        results = mod.fit()
        print(results.summary().tables[1])
        results.plot_diagnostics(figsize=(15, 12))
        plt.show()
        return results

    def step4(self, y, results):
        # Step 4 — Validating Forecasts
        pred = results.get_prediction(start=pd.to_datetime(self.start), dynamic=False)
        pred_ci = pred.conf_int()

        ax = y[self.obse_time:].plot(label='observed')
        pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)

        ax.fill_between(pred_ci.index,
                        pred_ci.iloc[:, 0],
                        pred_ci.iloc[:, 1], color='k', alpha=.2)

        ax.set_xlabel('Date')
        ax.set_ylabel('runtime')
        plt.legend()
        plt.show()

        y_forecasted = pred.predicted_mean
        y_truth = y[self.pred_time:]


        # Compute the mean square error
        mse = ((y_forecasted - y_truth) ** 2).mean()
        print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
        return round(mse, 2), y_forecasted, y_truth

    def step5(self, y, results):
        # Step 5 Producing and Visualizing Forecasts
        # Get forecast prediction steps ahead in future
        pred_uc = results.get_forecast(steps=self.pred_steps)

        # Get confidence intervals of forecasts
        pred_ci = pred_uc.conf_int()
        ax = y.plot(label='observed', figsize=(20, 15))
        pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
        ax.fill_between(pred_ci.index,
                        pred_ci.iloc[:, 0],
                        pred_ci.iloc[:, 1], color='k', alpha=.25)
        ax.set_xlabel('Date')
        ax.set_ylabel('runtime')

        plt.legend()
        plt.show()
        return pred_uc, pred_ci