import warnings

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as linalg

def GMRes(A, b, x0, nmax_iter):
    t1 = A.dot(x0)
    r = b - t1

    x = []
    q = sp.csr_matrix((nmax_iter, A.shape[0]), dtype=float)
    x.append(r)
    q[0] = r / np.linalg.norm(r)

    h = sp.csr_matrix((nmax_iter + 1, nmax_iter), dtype=float)

    for k in range(min(nmax_iter, A.shape[0])):
        y = A.dot(q[k].transpose())

        for j in range(k + 1):
            h[j, k] = q[j].dot(y)[0,0]
            y = y - h[j, k] * q[j].transpose()
        h[k + 1, k] = linalg.norm(y)
        if h[k + 1, k] != 0 and k != nmax_iter - 1:
            q[k + 1] = (y / h[k + 1, k]).transpose()

        b = [0] * (nmax_iter + 1)
        b[0] = np.linalg.norm(r)

        result = linalg.lsqr(h, b)[0]

        x.append(q.transpose().dot(result) + x0)

    return x