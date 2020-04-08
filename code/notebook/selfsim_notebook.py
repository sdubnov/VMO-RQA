# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import vmo
import vmo.analysis as van

# <markdowncell>

# ## Build a VMO / Oracle on Laughter

# <codecell>

import librosa
import matplotlib.pyplot as plt

filename = '/usr/labri/pmouawad/Documents/MATLAB/MAV-SV/MAV/Man_Voice/Happiness/6_happiness.wav'
#filename = './audio_files/ohm_scale.wav'
# filename = '../audioTestFiles/hmmtesttoneNoise.wav'
fft_size = 2048 #8192 #8192
hop_size = 256
samplerate = 22050

y, sr = librosa.load(filename, sr=samplerate)
# y_harm, y_perc = librosa.effects.hpss(y)
chroma = librosa.feature.chroma_cqt(y, samplerate, hop_length = hop_size)
features = chroma.T

plt.figure(figsize = (9,3))
plt.imshow(chroma, interpolation = 'nearest', aspect='auto')
plt.title('Chroma', fontsize=18)
plt.xlabel('Analysis Frame', fontsize=14)
plt.ylabel('Chroma', fontsize=14)
plt.tight_layout()

# <markdowncell>

# ### VMO - Variable Markov Oracle

# <codecell>

r = (0., 0.8, 0.02)
ideal_t = vmo.find_threshold(features, r = r, flag = 'a', dfunc = 'euclidean', dim=features.shape[1])

x_a = [i[1] for i in ideal_t[1]]
y_a = [i[0] for i in ideal_t[1]]
plt.figure()
plt.plot(x_a, y_a, linewidth = 2)
plt.title('IR vs. Threshold Value', fontsize = 18)
plt.grid(b = 'on')
plt.xlabel('Threshold', fontsize = 14)
plt.ylabel('IR', fontsize = 14)

# <markdowncell>

# Build the best oracle by choosing the ideal threshold (one that gives most informative oracle). 

# <codecell>

best_oracle = vmo.build_oracle(features, flag = 'a',
                          threshold = ideal_t[0][1],
                          feature = 'chroma', dfunc = 'euclidean', dim=features.shape[1])

#best_oracle = vmo.build_oracle(stock_data, flag='a', threshold=ideal_t[0][1], dim=stock_data.shape[1])

# <markdowncell>

# # Self-similarity matrix using reverse suffix links

# <codecell>

rs = van.create_selfsim(best_oracle, method = 'rsfx')
print rs
fig = plt.figure()
#ax = fig.add_subplot(111)
ax.imshow(rs)

# <codecell>

#OLD STUFF FOR PLOTTING STOCKS
ax.imshow(rs, origin = 'lower', cmap = 'Greys', interpolation = 'nearest', extent = [dates[0], dates[-1], dates[0], dates[-1]])
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)
ax.yaxis.set_major_locator(years)
ax.yaxis.set_major_formatter(yearsFmt)
ax.yaxis.set_minor_locator(months)
ax.autoscale_view()

# format the coords message box
ax.fmt_xdata = DateFormatter('%Y-%m-%d')
ax.fmt_ydata = DateFormatter('%Y-%m-%d')
fig.autofmt_xdate()
plt.tight_layout()

# <codecell>


