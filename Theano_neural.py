#########################
# Theano for Training a
# Neural Network on MNIST
#########################

import numpy as np

import theano
import theano.tensor as tensor

#On charge les données a utilisé pour l'entrainement
x = np.load('data_x.npy')
y = np.load('data_y.npy')

# On déclare deux matrices et une mémoire partagée que l'on initie aléatoirement.
#New matrice
sx = tensor.matrix()
sy = tensor.matrix()
#New mémoire partagée (CPU/GPU) avec dedans une matrice 784x500 de chiffre dont la moyenne est 0 et donc la variation autour de 0 est de moyenne 0.1
w = theano.shared(np.random.normal(avg=0, std=.1,
                                   size=(784, 500)))
#Nouvelle mémoire partagée avec dedans un vecteur ou une matrice de zéro et de taille spécifié
b = theano.shared(np.zeros(500))
v = theano.shared(np.zeros((500, 10)))
c = theano.shared(np.zeros(10))

# Hid et Out sont deux fonction représentant des variante de la tangante hyperbolique.
# Hid représente la fonction qui sera utilisé dans la couche caché pour calculer l'activation, out celle de la couche de sortie
# Tensor.dot correspond à un multiplication matriciel
hid = tensor.tanh(tensor.dot(sx, w) + b)
out = tensor.tanh(tensor.dot(hid, v) + c)
err = 0.5 * tensor.sum(out - sy) ** 2 # Erreur quadratique habituel

#Calcule d'un gradient d'erreur pour les différentes variables
gw, gb, gv, gc = tensor.grad(err, [w, b, v, c])

# On crée la fonction d'entrainement. Celle-ci prend deux paramètre, sx et xy et retourne la marge d'erreur de cette itération
#
train = theano.function([sx, sy], err,
    updates={
        w: w - lr * gw,
        b: b - lr * gb,
        v: v - lr * gv,
        c: c - lr * gc})

# now do the computations
batchsize = 100
for i in range(1000):
    x_i = x[i * batchsize: (i + 1) * batchsize]
    y_i = y[i * batchsize: (i + 1) * batchsize]
    err_i = train(x_i, y_i)