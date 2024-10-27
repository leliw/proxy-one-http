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


def test_normalize_filename(tmp_path):
    FileStorage._root_dir_path = tmp_path
    t = T("test_bucket")
    f = "2024-09-16_09:50:36.781105_GET__alfaRecordingsViewer_WebResource.axd?d=8Tf5eXXqwKl6OYcShqoO_6ybqGLekG3-PmWsSCafy9sEHQYWpHegyw9dSLsQ7SB8UTfc4-ZLbN2rE9ol7MbrFSqr2SXbiua5sNsFXtJ5TJ4nd4Uh5XfYzDrDZayXx0e-NoowiVIxRYlJ3J6t6I8DCgSY0x1bT1I5T2xyvykAlNQ1&t=637207635802849584_200.json"
    n = t._normalize_filename(f)

    assert n == "2024-09-16_09_50_36.781105_GET__alfaRecordingsViewer_WebResource.axd_d=8Tf5eXXqwKl6OYcShqoO_6ybqGLekG3-PmWsSCafy9sEHQYWpHegyw9dSLsQ7SB8UTfc4-ZLbN2rE9ol7MbrFSqr2SXbiua5sNsFXtJ5TJ4nd4Uh5XfYzDrDZayXx0e-NoowiVIxRYlJ3J6t6I8DCgSY0x1bT1I5T2xyvykAlNQ1&t=6372.json"
