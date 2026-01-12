# import serial
import csv
import pandas as pd
import matplotlib.cbook as cbook
from matplotlib import pyplot as plt

fileName = cbook.get_sample_data("D:\\ankita\\ankita_project\\final_project_code\\datasets\\emg_train_status.csv", asfileobj=False)
with cbook.get_sample_data(fileName) as file:
    fileName = pd.read_csv(fileName)

fileName.plot()
plt.show()


