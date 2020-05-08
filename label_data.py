import numpy as np
import pandas as pd
from __future__ import division
import matplotlib.pyplot as plt


from myutils import savePkl




df_mPower = pd.read_csv('/Users/andrevauvelle/Documents/Oxford/4YP/SynapseData/data750.csv',index_col=0)

df = df_mPower
df = df.reset_index(drop=True)


df['time'] = np.linspace(start=0,stop=df_mPower.shape[0]/100,num=df_mPower.shape[0])




windowtime = 1.28
overlap = 64/128



nperseg = windowtime*fs #Length of each segment - N in pape
noverlap = nperseg * overlap
shift = nperseg - noverlap

df = df.iloc[:(df.shape[0]//64)*64,:]

steps = (df.shape[0]-64)/shift

plt.ion()

# Lets play Score the Data
guessStore = []


time = df.time.as_matrix()
x = df.globalx.as_matrix()
y = df.globaly.as_matrix()
z = df.globalz.as_matrix()

'''
x = rescale(x)
y = rescale(y)
z = rescale(z)
'''


for i in range(len(guessStore),int(steps)):
    w = np.random.randint(steps)
    # Lets get the data from our window
    index = np.arange(int(w*shift), int(w*shift + nperseg))

    tp = time[index]
    xp = x[index]
    yp = y[index]
    zp = z[index]


    # Let's plot
    plt.figure(figsize=(8, 6))
    linex = plt.plot(tp, xp, label='x-axis')
    plt.setp(linex, linewidth=0.5, color='b',linestyle='-')
    liney = plt.plot(tp, yp, label='y-axis')
    plt.setp(liney, linewidth=2, color='b', linestyle=':')
    linez = plt.plot(tp, zp, label='z-axis')
    plt.setp(linez, linewidth=2, color='b', linestyle='-')
    axes = plt.gca()
    axes.set_xlim()
    axes.set_ylim([-1,1])
    axes.set_xlabel("Time (s)")
    axes.set_ylabel("Acceleration (normalized)")
    plt.legend()
    plt.grid()
    plt.draw()
    plt.show()
    plt.pause(0.001)
    guess = input('Gait = 1, Standing = 2, Buzz = 3, Unknown = 4 \nYour guess ...')
    print(len(guessStore))

    if tp.shape[0] <= 90:
        print('Less than 90 points')
        guess = 7
        guessStore.append([guess, w])
    elif guess == 9:
        plt.close()
        break
    elif guess not in [1,2,3,4]:
        guess = input('Gait = 1, Standing = 2, Buzz = 3, Unknown = 4 \nYour guess ...')
        guessStore.append([guess, w])
    else:
        guessStore.append([guess, w])
    print('Total Labeled: {}'.format(i))
    plt.close()
guessStore = np.array(guessStore)

savePkl(guessStore,'data750guessStore.pkl')


