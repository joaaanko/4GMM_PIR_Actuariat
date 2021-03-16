import numpy as np
import matplotlib.pyplot as plt


# Our goal is to have a np.random.poisson() vector that only increases 
# by one in the case of a claim. However, this is not the case so the
# transform_S_1_increment() will "flatten" the vector so that our number 
# of claims increases by 1 each time.
def transform_S_1_increment(N_T):
    for i in range(len(N_T)):
        if N_T[i] > 1:
            N_T[i] = 1
    return N_T


# The function below tracks the evolution of the number of claims throughout 
# the observed period of time. 
def claims_times(N_T):
    S=np.zeros(len(N_T))
    n = len(S)
    for i in range(len(S)):
        if N_T[i]==1:
            S[i:]+=1
    for i in range(len(S)):
        S[i]=int(S[i])
    return S

# get_W_times() tracks the W_k~Exp(lambda) and stores them in a vector
def get_W_times(S):
    N_T = S[-1]
    W = []
    t_claim_0 = 0
    for i in range(len(S)-1):
        if S[i] < S[i+1]:
            W.append(S[i+1]-t_claim_0)
            t_claim_0 = S[i+1]
    W.append(S[-1]-t_claim_0)
    W=np.array(W)
    return W

#Computes all of the values for y_tilde_n and stores them in a vector
def y_tilde_n(X, premium, W):
    N = len(X)
    y = np.zeros(N)
    #first index=1!!!!!!
    for n in range(1,N):
        sum_value=0
        for k in range(1,n+1):
            sum_value += X[k]-premium*W[k]
        y[n] = sum_value
    return y

def get_claims_poisson(u, n, premium, lamb, claims_max_cost):
    #n is the number of days.
    #t is the x axis, used to track the time.
    grad=10
    t = np.arange(0, n+.1, 1/grad)
    #R is the fortune of the company, we will track it using the Cramér-Lundberg model.
    R = premium*t+u
    #lambda is the parameter for the Poisson process.
    N = len(t)
    print("creating the poisson process history vector...")
    S=claims_times(transform_S_1_increment(np.random.poisson(lamb/grad, N)))
    print("done !")
    X_sum=0
    X_claim_history=[]
    print("changing the course of R...")
    for i in range(len(t)-1):
        if S[i] < S[i+1]:
            X = np.random.uniform(0, claims_max_cost)
            X_claim_history.append(X)
            R[i:] -= X
            X_sum+=X
    print("done !")
    
    X_claim_history=np.array(X_claim_history)
    W=get_W_times(S)
    #Create arrays to track Y and Y tilde
    Y = R-u
#     ytn = y_tilde_n(X_claim_history, premium, W)
    ytn=0
    #expected value for X_1
    mu=1/S[-1]*X_sum
    rho = (lamb*mu)/premium
    
    return (R, S, t, Y, rho, mu, ytn)



def plot_growth(R, N, t, Y):
    fig=plt.figure(figsize=(12.8,9.6))
    fig, ax1 = plt.subplots(figsize=(12.8,9.6))
    g1 = ax1.plot(t, R, label="Fortune (€)")
    g2 = ax1.plot(t,Y,label="Surplus Process (€)")
    ax1.set_ylabel("Fortune (€)")
    ax1.set_xlabel("Number of days")
    #plot claims using a secondary y axis
    ax2 = ax1.twinx()
    ax2.set_ylabel("Number of claims")
    g3 = ax2.step(t, N, color='orange', label="Number of claims")
    #prepare legend
    lns = g1+g2+g3
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs)
    plt.title("Tracking of the fortune using Cramér-Lundberg Model")
    plt.show()

def plot_y_tilde_n(ytn,rho, mu, lamb):
    print("\u03BC = "+str(mu))
    print("\u03BB = "+str(lamb))
    print("\u03C1 = "+str(rho))
    plt.plot(ytn)
    a = r'\tilde{Y}_n'
    plt.xlabel("n")
    plt.ylabel(r"$%s$" %(a),fontsize=15)
    plt.title("tracking the random walk")
    plt.show()
    
    
    