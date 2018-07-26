from arima_base import arimaClass
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

if __name__ == '__main__':
    t = arimaClass()
    series = t.step1('t3.csv')

    pdq = t.step23(series)
    # print(pdq)
    s4, y_forecasted, y_truth = t.step4(series, pdq)
    # print(y_forecasted, y_truth)
    s5a, s5b = t.step5(series, pdq)
    # print(s5a, s5b)
    for i in y_forecasted:
        print(i)
