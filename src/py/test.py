from scipy.interpolate import splrep, splev
import numpy as np
y = [1.0, 0.26666666666666666, -1.0, -0.26666666666666666]
x = np.arange(len(y))
spl = splrep(x, y, per=True)

xx = np.linspace(0, len(x)-1, 100)

import matplotlib.pyplot as plt
plt.plot(x, y, 'o')
plt.plot(xx, splev(xx, spl))
plt.show()
