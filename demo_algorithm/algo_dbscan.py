import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import datasets

#create datasets
X,y = datasets.make_blobs(n_samples=50, centers=3, n_features=2, random_state= 20, cluster_std = 1.5)
#parameter setting
eps = 2
MinPts = 5
#DBSCAN method
model = DBSCAN(eps, MinPts)
model.fit(X)
labels = model.fit_predict(X)
#results visualization
def plot():
  plt.figure()
  plt.scatter(X[:,0], X[:,1], c = labels)
  plt.axis('equal')
  plt.title('Prediction')
  plt.show()

plot()

def mydbscan(eps, min_pts):
  pass
