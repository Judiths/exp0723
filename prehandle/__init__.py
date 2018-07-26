from prehandle.options import OptsClass


csv_pos = 'D:\\PycharmProjects\\arima_MDGT\\arima\\'

opts = OptsClass()
data = opts.origin(csv_pos+'y_pred.csv')
print(data)