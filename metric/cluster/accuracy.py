from scipy.optimize import linear_sum_assignment
from sklearn.metrics.cluster import contingency_matrix

import numpy as np

def check_clusterings(labels_true, labels_pred):
    """Check that the two clusterings matching 1D integer arrays"""
    labels_true = np.asarray(labels_true)
    labels_pred = np.asarray(labels_pred)

    # input checks
    if labels_true.ndim != 1:
        raise ValueError(
            "labels_true must be 1D: shape is %r" % (labels_true.shape,))
    if labels_pred.ndim != 1:
        raise ValueError(
            "labels_pred must be 1D: shape is %r" % (labels_pred.shape,))
    if labels_true.shape != labels_pred.shape:
        raise ValueError(
            "labels_true and labels_pred must have same size, got %d and %d"
            % (labels_true.shape[0], labels_pred.shape[0]))
    return labels_true, labels_pred


def clustering_accuracy(labels_true, labels_pred):
    """Clustering Accuracy between two clusterings.
    Clustering Accuracy is a measure of the similarity between two labels of
    the same data. Assume that both labels_true and labels_pred contain n 
    distinct labels. Clustering Accuracy is the maximum accuracy over all
    possible permutations of the labels, i.e.
    \max_{\sigma} \sum_i labels_true[i] == \sigma(labels_pred[i])
    where \sigma is a mapping from the set of unique labels of labels_pred to
    the set of unique labels of labels_true. Clustering accuracy is one if 
    and only if there is a permutation of the labels such that there is an
    exact match
    This metric is independent of the absolute values of the labels:
    a permutation of the class or cluster label values won't change the
    score value in any way.
    This metric is furthermore symmetric: switching ``label_true`` with
    ``label_pred`` will return the same score value. This can be useful to
    measure the agreement of two independent label assignments strategies
    on the same dataset when the real ground truth is not known.
    
    Parameters
    ----------
    labels_true : int array, shape = [n_samples]
    	A clustering of the data into disjoint subsets.
    labels_pred : array, shape = [n_samples]
    	A clustering of the data into disjoint subsets.
    
    Returns
    -------
    accuracy : float
       return clustering accuracy in the range of [0, 1]
    """
    labels_true, labels_pred = check_clusterings(labels_true, labels_pred)
    # value = supervised.contingency_matrix(labels_true, labels_pred, sparse=False)
    value = contingency_matrix(labels_true, labels_pred)
    [r, c] = linear_sum_assignment(-value)
    return value[r, c].sum() / len(labels_true)
  
 
def self_representation_loss(labels_true, representation_matrix):
    """Evaluation of self-representation error for self-expressive subspace clustering methods
    Parameters
    ----------
    labels_true : int array, shape = [n_samples]
    	A clustering of the data into disjoint subsets.
    representation_matrix : array, shape = [n_samples, n_samples]
    	Each row is a representation vector
    
    Returns
    -------
    loss : float
       return self_representation_loss in the range of [0, 1]
    """
    n_samples = labels_true.shape[0]
    loss = 0.0
    for i in range(n_samples):
        representation_vec = np.abs(representation_matrix[i, :])
