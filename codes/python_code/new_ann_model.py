# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 09:00:26 2025

@author: Asus
"""

from torch.utils.data import DataLoader#, ramdon_split
import pandas as pd
from torch import nnimport torch.nn.functional as F

transforms = transforms.Compose([
    tranforms.ToTensor()
    ])

train_data = pd.read_csv("D:\\msc_rtmnu\\major_project\\final_project_code\\datasets\\emg_train.csv")
val_data = pd.read_csv("D:\\msc_rtmnu\\major_project\\final_project_code\\datasets\\emg_val.csv")
test_data = pd.read_csv("D:\\msc_rtmnu\\major_project\\final_project_code\\datasets\\emg_test.csv")


train_loader = DataLoader(train_data, batch_size=32)

class model(nn.Module):
    def __init__(self):
        
super(Network, self).__init__()

        