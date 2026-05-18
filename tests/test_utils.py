
import pytest
from dateutil.relativedelta import relativedelta

from src.utils.utils import force_list, get_files_path, relativedelta_str


def test_relativedelta_str():
    assert relativedelta_str("1mo") == relativedelta(months=1)
    assert relativedelta_str("3mo") == relativedelta(months=3)
    assert relativedelta_str("6mo") == relativedelta(months=6)
    assert relativedelta_str("1y") == relativedelta(years=1)
    assert relativedelta_str("2y") == relativedelta(years=2)
    assert relativedelta_str("4y") == relativedelta(years=4)


def test_force_list():
    @force_list("a", "b")
    def test_func(a, b, c=None):
        return a, b, c

    # Test with single values
    assert test_func(1, 2) == ([1], [2], None)
    assert test_func(1, 2, c=3) == ([1], [2], 3)

    # Test with lists
    assert test_func([1], [2]) == ([1], [2], None)
    assert test_func([1], [2], c=[3]) == ([1], [2], [3])

    # Test with mixed types
    assert test_func(1, [2]) == ([1], [2], None)
    assert test_func(1, [2], c=3) == ([1], [2], 3)


def test_force_list_error():
    @force_list("d")
    def test_func(a, b):
        return a, b
        
    with pytest.raises(ValueError, match="is not a valid argument for"):
        test_func(1, 2)


def test_get_files_path(tmp_path):
    # Create some dummy files
    (tmp_path / "test1.csv").touch()
    (tmp_path / "test2.csv").touch()
    (tmp_path / "test3.txt").touch()

    # Test finding specific extension
    csv_files = get_files_path(tmp_path, "csv")
    assert len(csv_files) == 2
    assert all(f.suffix == ".csv" for f in csv_files)

    # Test finding all files
    all_files = get_files_path(tmp_path, None)
    assert len(all_files) == 3

    # Test no files found
    with pytest.raises(FileNotFoundError, match="No JSON files found."):
        get_files_path(tmp_path, "json")
