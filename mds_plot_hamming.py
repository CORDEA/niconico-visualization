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
from matplotlib.ticker import NullFormatter
from matplotlib.font_manager import FontProperties

from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.neighbors import DistanceMetric
from sklearn.decomposition import PCA, TruncatedSVD

def calcMDS(pltnum, flag, dmetric):
    if flag == 1:
        clf = PCA(n_components=5)
        Y = clf.fit_transform(X)
        title  = 'PCA-MDS'
    elif flag == 2:
        clf = TruncatedSVD(n_components=5)
        Y = clf.fit_transform(X)
    else:
        Y = X
        title = 'MDS DistanceMetric: ' + str(dmetric)
    dist = DistanceMetric.get_metric(dmetric)
    Y    = dist.pairwise(Y)
    # Y = euclidean_distances(Y)
    mds = manifold.MDS(n_components=2, dissimilarity='precomputed')#, init='pca', random_state=0)
    Y = mds.fit_transform(Y)
    for i in range(1, 3):
        mdsPlot(int(str(pltnum) + str(i)), i, Y, title)

def mdsPlot(i, labelFlag, Y, title):
    if len(str(i)) == 1:
        fig = plt.figure(i)
    else:
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

def calcSNE(pcanc, lr, pp):
    if pcanc != 0:
        print("Calculating PCA-tSNE")
        clf = PCA(n_components=pcanc)
        Y = clf.fit_transform(X)
    else:
        print("Calculating tSNE")
        Y = X
    tsne = manifold.TSNE(n_components=2, learning_rate=lr, perplexity=pp)#, init='pca', random_state=0)
    Y = tsne.fit_transform(Y)
    for i in range(1, 3):
        plot(int("21" + str(i)), pcanc, lr, pp, i, Y)

def plot(i, pcanc, lr, pp, labelFlag, Y):
    if len(str(i)) == 1:
        fig = plt.figure(i)
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

if __name__ == '__main__':
    # with open(sys.argv[2]) as f:
        # tagList = [line.split("\t")[0] for line in f.readlines()]

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
            # for i in range(len(items)):
                # if items[i] in tagList:
                    # index.append(i)
            header = False
        else:
            tmp = []
            y.append(items[0])
            # tmp = [items[i] for i in range(len(items)) if i in index]
            X.append(items[1:])
        per = (j+1)/float(len(lines)) * 100
        sys.stdout.write("%.2f %%\r\b" % per)
        sys.stdout.flush()

    X = np.array(X)
    colors = np.random.rand(len(y))

    ax = plt.axes([0., 0., 1., 1.])
    # for Fedora
    # font = FontProperties(fname='/usr/share/fonts/vlgothic/VL-Gothic-Regular.ttf')
    # for Debian
    font = FontProperties(fname='/usr/share/fonts/truetype/vlgothic/VL-Gothic-Regular.ttf')
    print "Starting processing"

    # fig = plt.figure(2)
    calcMDS(21, 0, 'hamming')
    
    plt.show()
