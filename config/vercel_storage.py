import os
import uuid
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.deconstruct import deconstructible
import requests
import json


@deconstructible
class VercelBlobStorage(Storage):
    def __init__(self):
        self.token = getattr(settings, 'BLOB_READ_WRITE_TOKEN', None)
        if not self.token:
            raise ValueError(
                "BLOB_READ_WRITE_TOKEN is required for VercelBlobStorage")

        # Vercel Blob API endpoint
        self.base_url = "https://blob.vercel-storage.com"

    def _save(self, name, content):
        """Save file to Vercel Blob Storage"""
        try:
            # Generate unique filename
            file_extension = os.path.splitext(name)[1]
            unique_name = f"uploads/{uuid.uuid4()}{file_extension}"

            # Read content
            if hasattr(content, 'read'):
                content.seek(0)  # Reset file pointer
                file_content = content.read()
            else:
                file_content = content

            # First, get upload URL from Vercel Blob
            upload_url = f"{self.base_url}/put"

            params = {
                'filename': unique_name
            }

            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/octet-stream'
            }

            # Upload file using PUT method
            response = requests.put(
                upload_url,
                params=params,
                headers=headers,
                data=file_content
            )

            if response.status_code in [200, 201]:
                result = response.json()
                blob_url = result.get('url')
                if blob_url:
                    print(f"✓ File uploaded successfully: {blob_url}")
                    return blob_url
                else:
                    print(f"No URL in response: {result}")
                    return self._save_locally(name, content)
            else:
                print(
                    f"Upload failed: {response.status_code} - {response.text}")
                return self._save_locally(name, content)

        except Exception as e:
            print(f"Error uploading to Vercel Blob: {e}")
            import traceback
            traceback.print_exc()
            return self._save_locally(name, content)

    def _save_locally(self, name, content):
        """Fallback to local storage"""
        try:
            from django.core.files.storage import default_storage
            print(f"Falling back to local storage for: {name}")
            return default_storage.save(name, content)
        except Exception as e:
            print(f"Local storage fallback failed: {e}")
            return name

    def delete(self, name):
        """Delete file from Vercel Blob Storage"""
        try:
            if not name.startswith('http'):
                return True  # Not a blob URL, consider it deleted

            # Extract filename from URL for deletion
            delete_url = f"{self.base_url}/delete"

            # Get the blob key from the URL
            if 'blob.vercel-storage.com' in name:
                blob_key = name.split('/')[-1]
            else:
                return True

            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }

            data = {
                'urls': [name]
            }

            response = requests.post(delete_url, headers=headers, json=data)
            return response.status_code == 200

        except Exception as e:
            print(f"Error deleting from Vercel Blob: {e}")
            return False

    def exists(self, name):
        """Check if file exists"""
        if name.startswith('http'):
            try:
                response = requests.head(name, timeout=10)
                return response.status_code == 200
            except:
                return False
        return False

    def url(self, name):
        """Return file URL"""
        if name.startswith('http'):
            return name
        # If it's not a full URL, it might be a local fallback
        return name

    def size(self, name):
        """Return file size"""
        if name.startswith('http'):
            try:
                response = requests.head(name, timeout=10)
                return int(response.headers.get('content-length', 0))
            except:
                return 0
        return 0

    def get_available_name(self, name, max_length=None):
        """Return a filename that's available"""
        return name

    def listdir(self, path):
        """List directory contents (not implemented for blob storage)"""
        return [], []
