"""
=====================================
Blind source separation using FastICA
=====================================

An example of estimating sources from noisy data.

:ref:`ICA` is used to estimate sources given noisy measurements.
Imagine 3 instruments playing simultaneously and 3 microphones
recording the mixed signals. ICA is used to recover the sources
ie. what is played by each instrument. Importantly, PCA fails
at recovering our `instruments` since the related signals reflect
non-Gaussian processes.

"""
print(__doc__)


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from scipy import signal
import scipy.io.wavfile as wavf
import pyaudio
import wave

from sklearn.decomposition import FastICA, PCA
from playsound import playsound

from scipy.io.wavfile import read


a = read("output1.wav")
a_ = np.array(a[1],dtype=float)
#a_ = a_.ravel()
a_ = a_.T[:1,:400000]
a_ = a_.T
a_ /= a_.std(axis=0)
#print(len(a_))
#print(a_)

b = read("output2.wav")
b_ = np.array(b[1],dtype=float)
b_ = b_.T[:1,:400000]
b_ = b_.T
b_ /= b_.std(axis=0)

#print(b)

com = np.c_[a_,b_]
A = np.array([[0.7, 0.8], [0.3, 0.2]])  # Mixing matrix
com = np.dot(com, A.T)  # Generate observations
wavf.write("MIX.wav", 44100, np.array(com[:400000,0],dtype=float)*0.03)
#print(com)

# Compute ICA
ica = FastICA(n_components=2)
S_ = ica.fit_transform(com)  # Reconstruct signals
A_ = ica.mixing_  # Get estimated mixing matrix

# We can `prove` that the ICA model applies by reverting the unmixing.
assert np.allclose(com, np.dot(S_, A_.T) + ica.mean_)

#print(S_)

out1 = np.array(S_[:400000,0],dtype=float)
out2 = np.array(S_[:400000,1],dtype=float)

#print(out1)
#print(out2)
wavf.write("out1.wav", 44100, out1*8)
wavf.write("out2.wav", 44100, out2*8)

# #############################################################################



def play1(self):
	playsound('MIX.wav')

def play2(self):
	playsound('out1.wav')

def play3(self):
	playsound('out2.wav')



# #############################################################################
# Plot results

plt.figure()

#models = [S, X, S_, H]
models = [a_, b_, com, S_]
names = ['Observations 1',
         'Observations 2',
         'MIX', 
         'ICA recovered signals ']
colors = ['steelblue', 'red', 'orange']

for ii, (model, name) in enumerate(zip(models, names), 1):
    plt.subplot(4, 1, ii)
    plt.title(name)
    for sig, color in zip(model.T, colors):
        plt.plot(sig, color=color)

bt1 = plt.axes([0.1, 0.05, 0.15, 0.075])
bt2 = plt.axes([0.3, 0.05, 0.15, 0.075])
bt3 = plt.axes([0.5, 0.05, 0.15, 0.075])
b1 = Button(bt1, 'Mix Audio')
b1.on_clicked(play1)
b2 = Button(bt2, 'Output 1')
b2.on_clicked(play2)
b3 = Button(bt3, 'Output 2')
b3.on_clicked(play3)

plt.subplots_adjust(0.09, 0.04, 0.94, 0.94, 0.26, 0.46)
plt.subplots_adjust(bottom=0.2)
plt.show()


