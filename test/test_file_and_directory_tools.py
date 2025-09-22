import pytest
from dstools.file_and_directory_tools import windows_to_wsl_path


class TestFileAndDirectoryTools:

    @pytest.mark.parametrize("input_path, expected_output", [
        (r"C:\Users\John\Documents\file.txt", '/mnt/c/Users/AlanKerby/Audacia Consulting Limited/Audacia - Documents/Consultancy/Backlog Estimation/acceptance criteria')
    ])
    def test_windows_to_wsl_path(self, input_path, expected_output):
        wsl_path = windows_to_wsl_path(r"C:\Users\AlanKerby\Audacia Consulting Limited\Audacia - Documents\Consultancy\Backlog Estimation\acceptance criteria")
        assert wsl_path == expected_output
