import ext
import numpy as np
from scipy.sparse import csc_matrix 
from numpy.linalg import linalg

path = 'scores.csv'
dict_list = ext.getWinDict(path)
H = ext.getH(dict_list)
N = len(dict_list[0])

rowsumvector=H.dot(np.ones((N,1))).transpose()

zerorows=np.nonzero(rowsumvector == 0)
data = np.ones(len(zerorows[0]))
a= csc_matrix( (data, (zerorows[1],zerorows[0])), shape = (N,1))
                
residual=1;
epsilon=0.0001;
pi=np.ones((1,N))/N;
alpha=0.90;

while residual >= epsilon:
    prevpi = pi
    pi= alpha*(H.T.dot(pi.T)).T + (alpha*((a.T.dot(pi.T)).T)[0][0] + 1-alpha)*(1.0/N)*np.ones((1,N));
    residual=linalg.norm(pi-prevpi);

index = np.argsort(pi)
desc_index = index[0][::-1]

teamMap = dict_list[3]

for i in range(0, 25):
    print teamMap[desc_index[i]]
