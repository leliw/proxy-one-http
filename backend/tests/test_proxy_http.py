from app.features.proxy.proxy_server_manager import ProxyServerManager


def test_init(tmp_path):
    t = ProxyServerManager(str(tmp_path.joinpath("data/proxy")))

    assert t is not None


def test_start_status_stop(tmp_path):
    t = ProxyServerManager(str(tmp_path.joinpath("data/proxy")))

    assert t.start() is not None
    s = t.get_status()
    assert s.status == "working"
    assert t.stop() is not None
    s = t.get_status()
    assert s.status == "stopped"
