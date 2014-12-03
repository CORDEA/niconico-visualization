#!/usr/bin/env python
# encoding:utf-8
#
# Copyright [2014] [Yoshihiro Tanaka]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__Author__ =  "Yoshihiro Tanaka"
__date__   =  "2014-11-19"

import csv, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.collections import LineCollection
from matplotlib.ticker import NullFormatter
from matplotlib.font_manager import FontProperties
from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import PCA
from sklearn import (manifold, datasets, decomposition, ensemble, lda, random_projection)
import pickle

def calcPCASNE(pcanc, lr, pp):
    print("Calculating PCA-tSNE")
    clf = PCA(n_components=pcanc)
    Y = clf.fit_transform(X)
    tsne = manifold.TSNE(n_components=2, learning_rate=lr, perplexity=pp)
    Y = tsne.fit_transform(Y)
    # for i in range(1, 3):
        # plotPCASNE(int("21" + str(i)), pcanc, lr, pp, i, Y)
    for i in range(2):
        plotPCASNE(0, pcanc, lr, pp, 1, Y)

def plotPCASNE(i, pcanc, lr, pp, labelFlag, Y):
    if len(str(i)) == 1:
        fig = plt.figure(i, figsize=(33.11, 33.11), frameon=False)
        if i == 1:
            plt.axis('off')
    else:
        fig = plt.subplot(i)
    # plt.title(
              # 'PCA-n_components: ' + str(pcanc)
            # + ' learning_rate: ' + str(lr)
            # + ' perplexity: ' + str(pp))
    print("Plotting PCA-tSNE")
    plt.scatter(Y[:, 0], Y[:, 1], c=colors, visible=False)
    if labelFlag == 1:
        for label, cx, cy in zip(y, Y[:, 0], Y[:, 1]):
            plt.annotate(
                label.decode('utf-8'),
                xy = (cx, cy),
                xytext = (-0, 0),
                fontproperties=font,
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.8))
    plt.grid()
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')
    if i == 1:
        fig.savefig('pcasne_sq.png', bbox_inches='tight', dpi=250, pad_inches=0)
    else:
        fig.savefig('pcasne_sq_grid.png', bbox_inches='tight', dpi=250, pad_inches=0)
    print("Done.")

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    X = []
    y = []
    header = True
    for line in lines:
        if header:
            header = False
        else:
            tmp = line.split("\t")
            y.append(tmp[0])
            X.append(tmp[1:])

    X = np.array(X)
    colors = np.random.rand(len(y))


    n_points = len(X)
    n_neighbors = 10
    n_components = 2

    ax = plt.axes([0., 0., 1., 1.])
    ax.set_axis_off()
    font = FontProperties(fname='/usr/share/fonts/vlgothic/VL-Gothic-Regular.ttf', size=6)
    print "Starting processing"

    calcPCASNE(10, 1000, 50)
    
