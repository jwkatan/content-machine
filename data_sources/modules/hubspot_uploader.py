"""
HubSpot Image Uploader

Uploads images to HubSpot File Manager and returns public URLs.
Used for hosting LinkedIn post images so they display in Slack.

Setup:
1. Create a HubSpot private app at Settings > Integrations > Private Apps
2. Grant 'files' scope
3. Add HUBSPOT_ACCESS_TOKEN to .env
"""

import os
import json
from typing import Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path
import mimetypes


def upload_image(
    file_path: str,
    folder_path: str = "/linkedin-images",
    access_token: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Upload an image to HubSpot and return the public URL.

    Args:
        file_path: Local path to the image file
        folder_path: HubSpot folder path (created if doesn't exist)
        access_token: HubSpot private app token (optional, uses env if not provided)

    Returns:
        Tuple of (success: bool, url_or_error: str)
    """
    token = access_token or os.getenv('HUBSPOT_ACCESS_TOKEN')

    if not token:
        return False, "HUBSPOT_ACCESS_TOKEN not configured in .env"

    path = Path(file_path)
    if not path.exists():
        return False, f"File not found: {file_path}"

    # Determine content type
    content_type, _ = mimetypes.guess_type(str(path))
    if not content_type:
        content_type = 'image/png'

    try:
        # Read file
        with open(path, 'rb') as f:
            file_data = f.read()

        # Build multipart form data
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'

        # Build multipart body with separate fields
        parts = []

        # File part
        parts.append(f'--{boundary}\r\n'.encode('utf-8'))
        parts.append(f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'.encode('utf-8'))
        parts.append(f'Content-Type: {content_type}\r\n\r\n'.encode('utf-8'))
        parts.append(file_data)
        parts.append(b'\r\n')

        # folderPath part (required by HubSpot)
        parts.append(f'--{boundary}\r\n'.encode('utf-8'))
        parts.append(b'Content-Disposition: form-data; name="folderPath"\r\n\r\n')
        parts.append(folder_path.encode('utf-8'))
        parts.append(b'\r\n')

        # access part
        parts.append(f'--{boundary}\r\n'.encode('utf-8'))
        parts.append(b'Content-Disposition: form-data; name="options"\r\n')
        parts.append(b'Content-Type: application/json\r\n\r\n')
        parts.append(json.dumps({"access": "PUBLIC_NOT_INDEXABLE"}).encode('utf-8'))
        parts.append(b'\r\n')

        # End boundary
        parts.append(f'--{boundary}--\r\n'.encode('utf-8'))

        body = b''.join(parts)

        # Upload to HubSpot
        request = Request(
            'https://api.hubapi.com/files/v3/files',
            data=body,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': f'multipart/form-data; boundary={boundary}'
            }
        )

        with urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            public_url = result.get('url')

            if public_url:
                return True, public_url
            else:
                return False, "Upload succeeded but no URL returned"

    except HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        return False, f"HubSpot API error {e.code}: {error_body}"
    except URLError as e:
        return False, f"Network error: {e.reason}"
    except Exception as e:
        return False, f"Upload error: {str(e)}"


def upload_and_get_url(file_path: str) -> Optional[str]:
    """
    Simple wrapper - uploads image and returns URL or None.

    Args:
        file_path: Local path to image

    Returns:
        Public URL string, or None if upload failed
    """
    success, result = upload_image(file_path)
    if success:
        return result
    else:
        print(f"HubSpot upload failed: {result}")
        return None


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        print(f"Uploading {image_path} to HubSpot...")
        success, result = upload_image(image_path)
        if success:
            print(f"Success! URL: {result}")
        else:
            print(f"Failed: {result}")
    else:
        print("Usage: python hubspot_uploader.py <image_path>")
        print("Requires HUBSPOT_ACCESS_TOKEN environment variable")
