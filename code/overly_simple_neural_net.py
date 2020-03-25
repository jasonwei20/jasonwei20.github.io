# I wrote this from scratch, so there's no guarantee that this is right. -Jason, March 2020

import random
random.seed(42)
import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_deriv(x):
    return x*(1-x)

def forward(x, w1, w2, b1, b2):
    
    a0 = x                          # (1, 3)
    z1 = np.dot(a0, w1) + b1        # (1, 3) * (3, 4) = (1, 4)
    a1 = sigmoid(z1)                # (1, 4)
    z2 = np.dot(a1, w2) + b2        # (1, 4) * (4, 2) = (1, 2)
    a2 = sigmoid(z2)                # (1, 2)

    return a1, a2, z1

def backward(a0, a1, a2, y, z1):

    dz2 = a2 - y                    # (1, 2)
    dw2 = np.dot(a1.T, dz2)         # (4, 1) * (1, 2) = (4, 2)
    db2 = dz2                       # (1, 2)

    da1 = np.dot(dz2, w2.T)         # (1, 2) * (2, 4) = (1, 4)
    dz1 = da1 * sigmoid_deriv(z1)   # (1, 4)
    dw1 = np.dot(a0.T, dz1)         # (3, 1) * (1, 4) = (3, 4)
    db1 = dz1                       # (1, 4)

    return dw1, dw2, db1, db2, dz2

def train(x, y, w1, w2, b1, b2, num_epochs=600000, learning_rate=0.00001):

    for i in range(num_epochs):    

        a1, a2, z1 = forward(x, w1, w2, b1, b2)
        dw1, dw2, db1, db2, error = backward(x, a1, a2, y, z1)

        w2 -= learning_rate * dw2 
        w1 -= learning_rate * dw1 
        b2 -= learning_rate * db2
        b1 -= learning_rate * db1

        if (i % 10000) == 0:
            print (f"Error: {np.mean(np.abs(error)):.3f}")
    
    print(w2)
    print(w1)
    print(b2)
    print(b1)
    print(a2)

#input layer l0 with 3 dimensions
#hidden layer l1 with 4 dimensions
#output layer l2 with 2 dimensions
#weights w1 from l0 to l1 shape (3, 4)
#weights w2 from l1 to l2 shape (4, 2)

if __name__ == '__main__':

    x = np.array([[0, 1, 0]])
    y = np.array([0, 1])
    w1 = (2*np.random.random((3, 4))-1) / (3 + 4)
    w2 = (2*np.random.random(((4, 2)))-1) / (4 + 2)
    b1 = (2*np.random.random((1, 4))-1) / 4
    b2 = (2*np.random.random(((1, 2)))-1) / 2
    print(f"Dimensions: x {x.shape}, y {y.shape}, w1 {w1.shape}, w2 {w2.shape}")

    train(x, y, w1, w2, b1, b2)