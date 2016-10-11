# -*- coding: utf-8 -*-
"""
Example of use multi-layer perceptron
=====================================

Task: Approximation function: 1/2 * sin(x)

"""

import neurolab as nl
import numpy as np

min=-7
max=7

# Create train samples
x = np.linspace(min, max, 20)
y = np.sin(x) * 0.5

size = len(x)

inp = x.reshape(size,1)
tar = y.reshape(size,1)

# On crée un réseau avec deux neurones d'entrée, 5 neurones cachés et 1 neurone de sorties


# On entraine le réseau. On lui passe les inputs connus et les ouput attendu pour chacun.
# Ne pas toucher au autres paramètres


# Simulate network


# Plot result
import pylab as pl
pl.subplot(211)
pl.plot(error)
pl.xlabel('Epoch number')
pl.ylabel('error (default SSE)')

x2 = np.linspace(-6.0,6.0,150)
y2 = net.sim(x2.reshape(x2.size,1)).reshape(x2.size)

y3 = out.reshape(size)

pl.subplot(212)
pl.plot(x2, y2, '-',x , y, '.', x, y3, 'p')
pl.legend(['train target', 'net output'])
pl.show()