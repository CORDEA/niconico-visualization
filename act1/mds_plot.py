#!/usr/bin/env python
# encoding:utf-8
#

__Author__ =  "Yoshihiro Tanaka"
__date__   =  "2014-11-22"

import csv, sys
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from matplotlib.font_manager import FontProperties

from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import PCA

def calcSNE(pcanc, lr, pp):
    if pcanc != 0:
        print("Calculating PCA-tSNE")
        clf = PCA(n_components=pcanc)
        Y = clf.fit_transform(X)
    else:
        print("Calculating tSNE")
        Y = X
    tsne = manifold.TSNE(n_components=2, learning_rate=lr, perplexity=pp)
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
    u"""ラベルの表示

    ref. http://baoilleach.blogspot.jp/2014/01/convert-distance-matrix-to-2d.html
    """
    if labelFlag == 1:
        for label, cx, cy in zip(y, Y[:, 0], Y[:, 1]):
            plt.annotate(
                label.decode('utf-8'),
                xy = (cx, cy),
                xytext = (-10, 10),
                fontproperties=font,
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.9))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')
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

    ax = plt.axes([0., 0., 1., 1.])
    u""" 日本語フォントの設定(Fedora 20)

    ref. http://symfoware.blog68.fc2.com/blog-entry-1417.html
    """
    font = FontProperties(fname='/usr/share/fonts/vlgothic/VL-Gothic-Regular.ttf')
    print "Start processing"

    fig = plt.figure(0)
    calcSNE(2, 1000, 10)
    
    plt.show()
