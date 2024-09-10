from ampf.local import FileStorage


class T(FileStorage):
    pass


def test_default_ext(tmp_path):
    FileStorage._root_dir_path = tmp_path
    t = T("test_bucket", default_ext="json")
    p = t._create_file_path("xxx")

    assert p == tmp_path.joinpath("test_bucket", "xxx.json")


def test_no_default_ext(tmp_path):
    FileStorage._root_dir_path = tmp_path
    t = T("test_bucket")
    p = t._create_file_path("xxx", "txt")

    assert p == tmp_path.joinpath("test_bucket", "xxx.txt")


def test_subfolder(tmp_path):
    FileStorage._root_dir_path = tmp_path
    t = T("test_bucket", subfolder_characters=2, default_ext="json")

    p = t._create_file_path("xxx")

    assert p == tmp_path.joinpath("test_bucket", "xx", "xxx.json")
