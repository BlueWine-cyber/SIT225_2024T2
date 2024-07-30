import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('Arduino.csv')

X = df["X"]
Y = df["Y"]
Z = df["Z"]

# Plot X line graph
plt.subplot(2,2,1)
plt.plot(X)

plt.ylabel("Acceleration")
plt.title('X axis')

# Plot Y line graph
plt.subplot(2,2,2)
plt.plot(Y, color='orange')

plt.title('Y axis')

# Plot Z line graph
plt.subplot(2,2,3)
plt.plot(Z, color='green')

plt.xlabel("Data quantity")
plt.ylabel("Acceleration")
plt.title('Z axis')

# Combination of all AXIS
plt.subplot(2,2,4)
plt.plot(X)
plt.plot(Y, '--')
plt.plot(Z, '-.')

plt.legend(["X", "Y", "Z"])
plt.xlabel("Data quantity")
plt.title('ARDUINO ACCELEROMETER')
plt.show()
