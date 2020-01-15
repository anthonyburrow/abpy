from itertools import repeat
from sklearn.cluster import DBSCAN
import numpy as np


def process_data(data, eps, min_samples):
    # Scale data sent to model
    scaled_data = data.copy()
    x_range = abs(max(data[:, 0]) - min(data[:, 0]))
    y_range = abs(max(data[:, 1]) - min(data[:, 1]))
    scaled_data[:, 1] *= x_range / y_range

    # Determine clusters
    model = DBSCAN(eps=eps, min_samples=min_samples).fit(X=scaled_data)
    core_samples_mask = np.zeros_like(model.labels_, dtype=bool)
    core_samples_mask[model.core_sample_indices_] = True
    labels = model.labels_

    return labels, core_samples_mask


def get_clusters(data, eps, min_samples, n_iterations=1):
    # Check parameters
    assert isinstance(eps, (int, float, list)), \
        '"eps" must be int, float, or list'
    assert isinstance(min_samples, (int, float, list)), \
        '"min_samples" must be int, float, or list'

    if isinstance(eps, list) and isinstance(min_samples, list):
        assert len(eps) == len(min_samples), \
            '"eps" and "min_samples" must be same dimension'

    if isinstance(eps, list):
        assert len(eps) == n_iterations, \
            'Dimension of "eps" must equal "n_iterations"'
        eps_iter = eps
    else:
        eps_iter = repeat(eps)

    if isinstance(min_samples, list):
        assert len(min_samples) == n_iterations, \
            'Dimension of "min_samples" must equal "n_iterations"'
        min_samples_iter = min_samples
    else:
        min_samples_iter = repeat(min_samples)

    clusters = []
    noise = None

    data = data[~np.isnan(data).any(axis=1)]

    # Find clusters of each iteration
    for i, e, m in zip(range(n_iterations), eps_iter, min_samples_iter):
        labels, core_samples_mask = process_data(data, e, m)
        for k in (x for x in set(labels) if x != -1):
            class_member_mask = (labels == k)
            cluster_core = data[class_member_mask & core_samples_mask]
            cluster_boundary = data[class_member_mask & ~core_samples_mask]
            clusters.append((cluster_core, cluster_boundary))

        noise_mask = (labels == -1)
        data = data[noise_mask]

    noise = data

    return clusters, noise
