#!/usr/bin/env python
#coding:utf-8
#@Time: 2017/11/17下午10:35
#@Author: wangximei
#@File: tsne.py
#@describtion: TSNE

from sklearn.manifold import TSNE

def tsne(X):
    RS = 20171119
    proj_x = TSNE(random_state=RS).fit_transform(X)
    return proj_x