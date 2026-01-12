# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 17:16:36 2025

@author: USER8
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file with columns: ["EMG Value", "True Status", "Predicted Status"]
df = pd.read_csv("D:\\ankita\\ankita_project\\final_project_code\\datasets\\predictions.csv")

# Map categories to numeric values for plotting
status_map = {'Open': 1, 'Close': 0}
df['Predicted Numeric'] = df['Predicted Status'].map(status_map)
df['True Numeric'] = df['True Status'].map(status_map)

plt.figure(figsize=(15, 5))

# Plot EMG values
plt.plot(df['EMG Value'], label='EMG Value', color='gray', alpha=0.3)

# Plot predicted categories
plt.scatter(df.index, df['Predicted Numeric'], label='Predicted Status', marker='o', color='blue', s=10)

# Optionally, plot true categories if available
if 'True Status' in df.columns:
    plt.scatter(df.index, df['True Numeric'], label='True Status', marker='x', color='red', s=10)

plt.yticks([0, 1], ['Close', 'Open'])
plt.xlabel('Sample Index')
plt.ylabel('Category')
plt.title('EMG Value and Predicted Status Over Time')
plt.legend()
plt.tight_layout()
plt.show()
