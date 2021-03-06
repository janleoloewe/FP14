from uncertainties import *
from uncertainties.umath import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy import stats

c = 2.99792458*10**8
B = 455*10**(-3)
me = 9.10938291*10**(-31)
def calc_m(m,N,n):
	epsilon_o = 8.854187817*10**(-12)
	e = 1.6021765656*10**(-19)
	return(np.sqrt(abs(e**3*N*B/(8*np.pi**2*epsilon_o*c**3*n*m))))

Da = 5.11*10**(-3)
Db = 1.296*10**(-3)
Dc = 1.36*10**(-3)

Nb = 2.8*10**18/10**(-6)
Nc = 1.2*10**18/10**(-6)

convert1 = np.pi/10800
convert2 = np.pi/180

d, thea1, thea1s, thea2, thea2s, theb1, theb1s, theb2, theb2s, thec1, thec1s, thec2, thec2s = np.loadtxt("b.txt", comments="%" ,unpack=True)
d2 = np.array([0.0 for i in range(len(thea1))])
thea = np.array([[0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))]])
theb = np.array([[0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))]])
thec = np.array([[0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))], [0.0 for i in range(len(thea1))]])

for i in range(len(thea1)):
	thea[0][i] = thea1[i]*convert2+thea1s[i]*convert1
	theb[0][i] = theb1[i]*convert2+theb1s[i]*convert1
	thec[0][i] = thec1[i]*convert2+thec1s[i]*convert1
	thea[1][i] = thea2[i]*convert2+thea2s[i]*convert1
	theb[1][i] = theb2[i]*convert2+theb2s[i]*convert1
	thec[1][i] = thec2[i]*convert2+thec2s[i]*convert1
	thea[2][i] = 1/2*abs(thea[1][i]-thea[0][i])
	theb[2][i] = 1/2*abs(theb[1][i]-theb[0][i])
	thec[2][i] = 1/2*abs(thec[1][i]-thec[0][i])
	thea[3][i] = thea[2][i]/Da
	theb[3][i] = theb[2][i]/Db
	thec[3][i] = thec[2][i]/Dc
	thea[4][i] = thea[3][i]-thea[3][i]
	theb[4][i] = theb[3][i]-thea[3][i]
	thec[4][i] = thec[3][i]-thea[3][i]
print("Winkel:")
print(thea[2])
print("\n")
print(theb[2])
print("\n")
print(thec[2])
print("\n")
print("Winkel normiert:")
print(thea[3])
print("\n")
print(theb[3])
print("\n")
print(thec[3])
print("\n")
print("Winkel abgezogen:")
print(thea[4])
print("\n")
print(theb[4])
print("\n")
print(thec[4])
print("\n")

for i in range(len(d)):
	d2[i] = (d[i]*10**-6)**2

mb, bb, lol1, lol2, lol3 = stats.linregress(d2, theb[4])
mc, bc, lol1, lol2, lol3 = stats.linregress(d2, thec[4])

n=3.4

m1 = calc_m(mb,Nb,n)
m2 = calc_m(mc,Nc,n)
print("Steigung duenn:" + str(mb))
print("Steigung dick:" + str(mc))
print("Masse duenn:" + str(m1))
print("Masse dick:" +str(m2))
print("Verhaeltnis duenn:" + str(m1/me))
print("Verhältnis dick:" + str(m2/me))
print(1-0.066/(m1/me))
print(1-0.066/(m2/me))
fig = plt.figure()
plt.plot(d,thea[3],"r-")
plt.plot(d,theb[3],"b-")
plt.plot(d,thec[3],"g-")
plt.plot(d,thea[3],"rx",label="Hochrein")
plt.plot(d,theb[3],"bx", label="n-dotiert duenn")
plt.plot(d,thec[3],"gx", label="n-dotiert dick")
plt.ylabel("$\Theta$/D[rad/m]")
plt.xlabel("$\lambda$[µm]")
plt.ylim([0,160])
plt.legend()
plt.savefig("theta.pdf")
#plt.show()
plt.close(fig)
fig = plt.figure()
plt.plot(d2, mb*d2+bb,"r-", label="Regression duenn")
plt.plot(d2, mc*d2+bc,"b-", label="Regression dick")
plt.plot(d2,theb[4],"rx", label="Messwerte duenn")
plt.plot(d2,thec[4],"bx",label="Messwerte dick")
plt.ylabel("$\Theta$/D[rad/m]")
plt.xlabel("$\lambda$²[µm²]")
plt.ylim([0,140])
plt.legend(loc=2)
plt.savefig("fit.pdf")
#plt.show()
plt.close(fig)

