import numpy as np
import torch
import matplotlib.pyplot as plt

file_num = 20
file_name = f'Data/results_{file_num}.pth'
results = torch.load(file_name)

print(results['results'])
plt.subplot(2,1,1)
plt.plot(results['results'])
plt.subplot(2,1,2)
plt.plot(results['avglosses'])
plt.show()


