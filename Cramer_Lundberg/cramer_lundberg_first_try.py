import numpy as np
import matplotlib.pyplot as plt
#the risk process model

#R is the fortune of the company.
R=0
#u is the initial fortune of the company.
u=1000
#P is the premium income. It is constant.
P=1000
#S is the total claim amount. It is random.
N=0


#Let's track the fortune
n=50
r_tracking=np.zeros(n)
s_tracking=np.zeros(n)
t=np.arange(0,n)
r_tracking[0]=u
for i in range(1,len(t)):
    r_tracking[i]=r_tracking[i-1]+P
    #let's say that some unfortunate event happens.
    if np.random.uniform()<.3:
        N+=1
        X=np.random.uniform(0,2000)
        s_tracking[i]=X+s_tracking[i-1]
        r_tracking[i]=r_tracking[i-1]-X
    else:
        s_tracking[i]=s_tracking[i-1]
plt.step(t,r_tracking,label='fortune')
plt.step(t,s_tracking,label='total claim amount')
plt.show()
print(N)
if r_tracking[0]<=r_tracking[-1]:
    print("The company's fortune has increased over "+str(n)+" days.")
    print("The gain equals "+str(int(abs(r_tracking[0]-r_tracking[-1])))+"€")
else:
    print("The company's fortune has decreased over "+str(n)+" days.")
    print("The loss equals "+str(int(abs(r_tracking[0]-r_tracking[-1])))+"€")
