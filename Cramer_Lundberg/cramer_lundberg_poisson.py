import numpy as np
import matplotlib.pyplot as plt

#R is the fortune of the company, we will track it using the Cramér-Lundberg model.
#n is the number of days.
n=1000
#c is the premium.
c=100
t=np.arange(0,n+.1,.1)
R=c*t
# plt.plot(t,R)

#prepare poisson process
lamb = .02
N=len(t)
X_T= [np.random.poisson(lamb, N)]
S = [[np.sum(X[0:i]) for i in range(N)] for X in X_T]
X = np.linspace(0, N, N)
S=np.reshape(S,(N,))

#N is the number of sinisters
sinisters=0
N=np.zeros(len(t))
for i in range(len(t)-1):
    if i != 0:
        if S[i]<S[i+1]:
            X=X=np.random.uniform(0,600)
            R[i:]=R[i:]-X

fig, ax1 = plt.subplots()
g1=ax1.plot(t,R,label="Fortune (€)")
ax1.set_ylabel("Fortune (€)")
ax2 = ax1.twinx()
ax2.set_ylabel("Number of sinisters")
g2=ax2.plot(t,S,color='orange',label="Number of sinisters")
lns = g1+g2
labs = [l.get_label() for l in lns]
plt.legend(lns,labs)
plt.title("Tracking of the fortune using Cramér-Lundberg Model")