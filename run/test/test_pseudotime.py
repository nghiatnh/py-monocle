import os
import pytest
import h5py
import numpy as np
from py_monocle3 import pseudotime
from scipy.stats import kendalltau

from . import _constants as constants


@pytest.mark.parametrize("data_id", constants.DATASET)
def test_pseudotime(data_id: str):
  with h5py.File(os.path.join(constants.DATA_FOLDER, f"{data_id}.hdf5")) as f:
    clusters = f["monocle3/k_means_clustering"][()]
    expected_pseudotime = f["monocle3/pseudotime"][()]
    matrix = f["umap"][()]
  ptime = pseudotime(
    matrix=matrix,
    clusters=clusters,
    use_clusters_as_kmeans=True,
    root_cells=0,
  )
  score = kendalltau(ptime, expected_pseudotime)[0]
  assert score > 0.95, f"The similarity is {score}."
