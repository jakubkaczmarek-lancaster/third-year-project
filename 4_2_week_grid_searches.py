# -*- coding: utf-8 -*-
"""4.2 week grid searches.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rsNy53r5YbigQARBIvqvTWgnrvYWTayL
"""

from google.colab import drive
drive.mount("/content/gdrive")

#Electricity
#MC204-L03_M9R12 Best ARIMA(4, 1, 2) RMSE=29.23177
#MC061-L04_M24R12 Best ARIMA(6, 0, 2) RMSE=19.64875
#MC134-L01_M9R14 Best ARIMA(6, 0, 2) RMSE=8.66159

#Water
#MC067-L01_M1 Best Best ARIMA(4, 0, 2) RMSE=0.07895
#MC046-L04_M4 Best Best ARIMA(6, 0, 0) RMSE=0.41601
#MC078-L02_M3 Best Best ARIMA(4, 0, 2) RMSE=0.28206

#Heat
#MC076-L01_M2 Best Best ARIMA(4, 0, 2) RMSE=0.02212
#MC065-L02_M3 Best Best ARIMA(6, 0, 2) RMSE=0.02460
#MC048-L01_M5 Best Best ARIMA(1, 0, 1) RMSE=0.00753

import pandas as pd
data pd.read_csv('/content/gdrive/My Drive/data/Synetica/meters_final/60min/MC048-L01_M5format60min.csv', header=0, index_col=0)
data.shape

#arima gridsearch
import warnings
from math import sqrt
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

# def evaluate arima (p,d,q)
def evaluate_arima_model(X, arima_order):
	# split train and test
	train, test = X[0:504], X[504:672]
	history = [x for x in train]
	#predictions
	predictions = list()
	for t in range(len(test)):
		model = ARIMA(history, order=arima_order)
		model_fit = model.fit()
		yhat = model_fit.forecast()[0]
		predictions.append(yhat)
		history.append(test[t])
	# rmse calculation
	rmse = sqrt(mean_squared_error(test, predictions))
	return rmse

# different combinations of p d and q
def evaluate_models(dataset, p_values, d_values, q_values):
	dataset = dataset.astype('float32')
	best_score, best_cfg = float("inf"), None
	for p in p_values:
		for d in d_values:
			for q in q_values:
				order = (p,d,q)
				try:
					rmse = evaluate_arima_model(dataset, order)
					if rmse < best_score:
						best_score, best_cfg = rmse, order
					print('ARIMA%s RMSE=%.5f' % (order,rmse))
				except:
					continue
	print('Best ARIMA%s RMSE=%.5f' % (best_cfg, best_score))


data = pd.read_csv('/content/gdrive/My Drive/data/Synetica/meters_final/60min/MC048-L01_M5format60min.csv', header=0, index_col=0)
# select parameters to try in gridsearch
p_values = [0, 1, 2, 4, 6]
d_values = range(0, 3)
q_values = range(0, 3)
warnings.filterwarnings("ignore")
evaluate_models(data.values, p_values, d_values, q_values)