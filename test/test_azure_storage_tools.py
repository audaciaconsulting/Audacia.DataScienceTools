import pytest
from dstools.azure_storage_tools import upload_to_azure, download_from_azure


class TestFileAndDirectoryTools:

    @pytest.fixture
    def test_file(self, tmp_path):
        """Create a temporary test file."""
        test_file = tmp_path / "test_file.txt"
        test_file.write_text("This is test content for Azure upload")
        return test_file

    def test_upload_to_azure(self, test_file):
        """Test uploading a single file to Azure."""
        output = upload_to_azure(test_file, container_name='test')

        assert output is not None
        assert 'test_file.txt' in output

    def test_download_from_azure(self, test_file, tmp_path):
        upload_to_azure(test_file, container_name='test')

        download_path = tmp_path / "downloaded_file.txt"
        download_from_azure(
            container_name='test',
            blob_name='test_file.txt',
            local_path=download_path
        )

        assert download_path.exists()
        assert download_path.read_text() == test_file.read_text()