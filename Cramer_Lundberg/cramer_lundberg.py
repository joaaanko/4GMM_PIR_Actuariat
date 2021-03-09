import numpy as np
import matplotlib.pyplot as plt

def get_claims_uniform(u, n, premium, claims_probability, claims_max_cost):
    #t is the x axis, used to track the time.
    t = np.arange(0, n+.1, .1)
    #R is the fortune of the company, we will track it using the Cramér-Lundberg model.
    R = premium*t+u
    N = np.zeros(len(t))
    for i in range(len(t)-1):
        if np.random.uniform() < claims_probability:
            N[i:] += 1
            X = X = np.random.uniform(0, claims_max_cost)
            R[i:] = R[i:]-X
    return R, N, t

def get_claims_poisson(u, n, premium, lamb, claims_max_cost):
    #n is the number of days.
    #t is the x axis, used to track the time.
    t = np.arange(0, n+.1, .1)
    #R is the fortune of the company, we will track it using the Cramér-Lundberg model.
    R = premium*t+u
    #lambda is the parameter for the Poisson process.
    N = len(t)
    X_T = [np.random.poisson(lamb, N)]
    S = [[np.sum(X[0:i]) for i in range(N)] for X in X_T]
    S = np.reshape(S, (N,))
    for i in range(len(t)-1):
        if S[i] < S[i+1]:
            X = np.random.uniform(0, claims_max_cost)
            R[i+1:] -= X
    return R, S, t


def plot_growth(R, N, t):
    fig=plt.figure(figsize=(12.8,9.6))
    fig, ax1 = plt.subplots(figsize=(12.8,9.6))
    g1 = ax1.plot(t, R, label="Fortune (€)")
    ax1.set_ylabel("Fortune (€)")
    ax1.set_xlabel("Number of days")
    #plot claims using a secondary y axis
    ax2 = ax1.twinx()
    ax2.set_ylabel("Number of claims")
    g2 = ax2.step(t, N, color='orange', label="Number of claims")
    #prepare legend
    lns = g1+g2
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs)
    plt.title("Tracking of the fortune using Cramér-Lundberg Model")
    plt.show()