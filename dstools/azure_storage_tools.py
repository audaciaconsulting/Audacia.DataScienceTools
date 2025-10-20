from azure.storage.blob import BlobServiceClient
from pathlib import Path
from dstools.variables import get_env_var

connection_string = get_env_var('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connection_string)


def upload_to_azure(local_path, container_name, blob_name=None, overwrite=True):
    """
    Upload a file to Azure Blob Storage

    Parameters:
    -----------
    local_path : str or Path
        Path to the local file to upload
    container_name : str
        Name of the Azure container (e.g., 'sim-anomaly-detection')
    blob_name : str, optional
        Name for the blob in Azure. If None, uses the filename from local_path
    overwrite : bool, default=True
        Whether to overwrite if blob already exists

    Returns:
    --------
    str : URL of the uploaded blob

    Example:
    --------
    >>> upload_to_azure('plots/123456_total_vol.png', 'sim-anomaly-detection')
    >>> upload_to_azure('plots/123456_total_vol.png', 'sim-anomaly-detection',
    ...                 blob_name='analysis/123456_total_vol.png')
    """
    # Convert to Path object for easier manipulation
    local_path = Path(local_path)

    # Use filename if blob_name not provided
    if blob_name is None:
        blob_name = local_path.name

    # Get container client
    container_client = blob_service_client.get_container_client(container_name)

    # Create container if it doesn't exist
    try:
        container_client.create_container()
        print(f"Created container: {container_name}")
    except Exception:
        pass  # Container already exists

    # Upload file
    try:
        with open(local_path, "rb") as data:
            container_client.upload_blob(
                name=blob_name,
                data=data,
                overwrite=overwrite
            )

        # Construct and return URL
        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}"
        print(f"✓ Uploaded: {blob_name} to {container_name}")
        return blob_url

    except FileNotFoundError:
        print(f"✗ Error: File not found: {local_path}")
        raise
    except Exception as e:
        print(f"✗ Upload failed: {e}")
        raise


def download_from_azure(blob_name, container_name, local_path):
    """
    Download a file from Azure Blob Storage

    Parameters:
    -----------
    blob_name : str
        Name of the blob in Azure
    container_name : str
        Name of the Azure container
    local_path : str or Path
        Where to save the downloaded file

    Example:
    --------
    >>> download_from_azure('123456_total_vol.png', 'sim-anomaly-detection',
    ...                     'downloaded_plots/123456.png')
    """
    local_path = Path(local_path)
    local_path.parent.mkdir(parents=True, exist_ok=True)

    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    try:
        with open(local_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        print(f"✓ Downloaded: {blob_name} to {local_path}")
        return local_path
    except Exception as e:
        print(f"✗ Download failed: {e}")
        raise