import pytest

from ampf.local.ampf_local_factory import AmpfLocalFactory


@pytest.fixture
def factory(tmp_path):
    return AmpfLocalFactory(tmp_path)
