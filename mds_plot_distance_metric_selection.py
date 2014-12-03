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

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import NullFormatter
from matplotlib.font_manager import FontProperties
from matplotlib.colors import Normalize

from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.neighbors import DistanceMetric
from sklearn.decomposition import PCA, TruncatedSVD

def calcMDS(pltnum, flag, dmetric):
    if flag == 1:
        clf = PCA(n_components=2)
        Y = clf.fit_transform(X)
        title  = 'PCA-MDS DistanceMetric: ' + str(dmetric)
    elif flag == 2:
        clf = TruncatedSVD(n_components=2)
        Y = clf.fit_transform(X)
        title  = 'SVD-MDS DistanceMetric: ' + str(dmetric)
    else:
        Y = X
        title = 'MDS DistanceMetric: ' + str(dmetric)
    dist = DistanceMetric.get_metric(dmetric)
    Y    = dist.pairwise(Y)
    # Y = euclidean_distances(Y)
    mds = manifold.MDS(n_components=2, dissimilarity='precomputed', metric=False)#, init='pca', random_state=0)
    Y = mds.fit_transform(Y)
    # for i in range(1, 3):
    mdsPlot(pltnum, 0, Y, title)

def mdsPlot(i, labelFlag, Y, title):
    fig = plt.subplot(i)
    plt.title(title)
    print("Computing tSNE")
    plt.scatter(Y[:, 0], Y[:, 1], c=colors)
    if labelFlag == 1:
        for label, cx, cy in zip(y, Y[:, 0], Y[:, 1]):
            plt.annotate(
                label.decode('utf-8'),
                xy = (cx, cy),
                xytext = (-10, 10),
                fontproperties=font,
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.9))
                #arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')
    print("Done.")

def calcSNE(n, pcanc, lr, pp):
    if pcanc != 0:
        print("Calculating PCA-tSNE")
        clf = PCA(n_components=pcanc)
        Y = clf.fit_transform(X)
    else:
        print("Calculating tSNE")
        Y = X
    tsne = manifold.TSNE(n_components=3, learning_rate=lr, perplexity=pp)#, init='pca', random_state=0)
    Y = tsne.fit_transform(Y)
    for i in range(0, 3):
        # if i == 0:
        if i == 0:
            coords = (0, 1, 2)
        elif i == 1:
            coords = (0, 2, 1)
        else:
            coords = (1, 2, 0)
        plot(i+n, pcanc, lr, pp, 1, Y, coords)
        # else:
            # plot(int("21" + str(i)), pcanc, lr, pp, i, Y)

def calcISO(n):
    iso = manifold.Isomap(n_neighbors=10, n_components=3)
    Y = iso.fit_transform(X)
    for i in range(0, 3):
        if i == 0:
            coords = (0, 1, 2)
        elif i == 1:
            coords = (0, 2, 1)
        else:
            coords = (1, 2, 0)
        plot(i+n, 0, 0, 0, 1, Y, coords)
        # else:
            # plot(int("21" + str(i)), 0, 0, 0, i, Y)

def plot(i, pcanc, lr, pp, labelFlag, Y, coords):
    if len(str(i)) == 1:
        fig = plt.figure(i, figsize=(33.11, 33.11), frameon=False)
        plt.axis('off')
    else:
        fig = plt.subplot(i)
    if pcanc == 0:
        plt.title(
                  ' learning_rate: ' + str(lr)
                + ' perplexity: ' + str(pp))
        print("Plotting tSNE")
    else:
        plt.title(
                  'PCA-n_components: ' + str(pcanc)
                + ' learning_rate: ' + str(lr)
                + ' perplexity: ' + str(pp))
        print("Plotting PCA-tSNE")

    norm = Normalize(vmin=0.0, vmax=1.0)
    cmap = cm.ScalarMappable(cmap=cm.winter, norm=norm)
    colors = [
            cmap.to_rgba(
                str(
                        (np.abs(min(Y[:, coords[2]]))+r) / 
                        float(max(Y[:, coords[2]])+np.abs(min(Y[:, coords[2]])))
                    )
                ) for r in Y[:, coords[2]]
            ]
    print max(colors)
    if len(str(i)) == 1:
        plt.scatter(Y[:, coords[0]], Y[:, coords[1]], c=colors, visible=False)
        xyt = (-0, 0)
    else:
        plt.scatter(Y[:, coords[0]], Y[:, coords[1]], c=colors)
        xyt = (-10, 10)
    if labelFlag == 1:
        for label, cx, cy, cc in zip(y, Y[:, coords[0]], Y[:, coords[1]], colors):
            plt.annotate(
                label.decode('utf-8'),
                xy = (cx, cy),
                xytext = xyt,
                fontproperties=font,
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = cc, alpha = 0.9))
                #arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')
    if len(str(i)) == 1:
        fig.savefig("result" + str(i) + ".png", bbox_inches='tight', dpi=300, pad_inches=0)
    print("Done.")

if __name__ == '__main__':

    with open(sys.argv[1]) as f:
        lines = f.readlines()

    index = []
    X     = []
    y     = []
    header = True
    for j in range(len(lines)):
        line = lines[j]
        items = line.rstrip().split("\t")
        if header:
            header = False
        else:
            tmp = []
            y.append(items[0])
            X.append(items[1:])
        per = (j+1)/float(len(lines)) * 100
        sys.stdout.write("%.2f %%\r\b" % per)
        sys.stdout.flush()


    X = np.array(X)
    colors = np.random.rand(len(y))

    ax = plt.axes([0., 0., 1., 1.])
    ax.set_axis_off()
    # font = FontProperties(fname='/usr/share/fonts/vlgothic/VL-Gothic-Regular.ttf')
    # for Debian
    font = FontProperties(fname='/usr/share/fonts/truetype/vlgothic/VL-Gothic-Regular.ttf', size=7)
    print "Starting processing"

    fig = plt.figure(0)
    calcSNE(5, 2, 1000, 50)
    fig =plt.figure(4)
    calcISO(7)

    fig = plt.figure(0)
    calcMDS(331, 0, 'euclidean')
    calcMDS(332, 1, 'euclidean')
    calcMDS(333, 2, 'euclidean')
    calcMDS(334, 0, 'manhattan')
    calcMDS(335, 1, 'manhattan')
    calcMDS(336, 2, 'manhattan')
    calcMDS(337, 0, 'hamming')
    calcMDS(338, 1, 'hamming')
    calcMDS(339, 2, 'hamming')
    # calcMDS(336, 0, 'canberra')
    # calcMDS(337, 0, 'braycurtis')
    # calcMDS(338, 0, 'jaccard')
    # calcMDS(339, 0, 'dice')
    
    plt.show()
