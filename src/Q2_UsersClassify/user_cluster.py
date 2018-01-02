#!/usr/bin/env python
#coding:utf-8
#@Time: 2018/1/2下午10:31
#@Author: wangximei
#@File: user_cluster.py
#@describtion:

print(__doc__)

import os
import T_SNE
from sklearn.datasets import load_svmlight_file
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs


def mean_shift(X):
    # #############################################################################
    # Compute clustering with MeanShift

    # The following bandwidth can be automatically detected using
    bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    print("number of estimated clusters : %d" % n_clusters_)

    # #############################################################################
    # Plot result
    import matplotlib.pyplot as plt
    from itertools import cycle

    plt.figure(1)
    plt.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
# #############################################################################

def tsne(X):
    proj_x = T_SNE.tsne(X)
    out_path = 'result/digits-tsne.png'
    return proj_x


if __name__ == "__main__":
    pre_path = os.path.dirname(os.getcwd())
    ##  prepare data
    in_path = pre_path + "/../data/features.csv"
    print "Loading feature file ..."
    X, y = load_svmlight_file(in_path)
    # Generate sample data
    centers = [[1, 1], [-1, -1], [1, -1]]
    X, _ = make_blobs(n_samples=10000, centers=centers, cluster_std=0.6)
    print X[:5,:]
    proj_x = tsne(X)
    mean_shift(proj_x)



