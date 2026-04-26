#!/usr/bin/env python3
"""
Photo Upload Server for Syncoloco
Receives photos via HTTP and saves to local filesystem.
"""

import argparse
import os
import json
import hashlib
import logging
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Global config (set by argparse)
config = {}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


class PhotoUploadHandler(BaseHTTPRequestHandler):
    """HTTP handler for photo uploads."""

    def log_message(self, format, *args):
        """Override to use our logger."""
        logger.info("%s - %s", self.address_string(), format % args)

    def send_json_response(self, status_code: int, data: dict):
        """Send a JSON response."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def check_auth(self) -> bool:
        """Verify API token if configured."""
        if not config["token"]:
            return True

        auth_header = self.headers.get("Authorization", "")
        expected = f"Bearer {config['token']}"
        return auth_header == expected

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/health":
            self.send_json_response(200, {
                "status": "ok",
                "timestamp": datetime.now().isoformat()
            })
        elif path == "/list":
            self._handle_list(query)
        else:
            self.send_json_response(404, {"error": "Not found"})

    def _handle_list(self, query: dict):
        """Return list of files already uploaded for a device with path and size."""
        if not self.check_auth():
            self.send_json_response(401, {"error": "Unauthorized"})
            return

        device = query.get("device", [""])[0]
        if not device:
            self.send_json_response(400, {"error": "Missing device parameter"})
            return

        device = device.replace("..", "").replace("/", "_")
        device_dir = os.path.join(config["upload_dir"], device)

        files = []

        if os.path.isdir(device_dir):
            for root, dirs, filenames in os.walk(device_dir):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    rel_path = os.path.relpath(filepath, device_dir)
                    size = os.path.getsize(filepath)
                    files.append({"path": rel_path, "size": size})

        logger.info("Listed %d files for device %s", len(files), device)

        self.send_json_response(200, {
            "device": device,
            "files": files,
            "count": len(files)
        })

    def do_POST(self):
        """Handle photo upload."""
        if self.path != "/upload":
            self.send_json_response(404, {"error": "Not found"})
            return

        if not self.check_auth():
            logger.warning("Unauthorized upload attempt from %s", self.address_string())
            self.send_json_response(401, {"error": "Unauthorized"})
            return

        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self.send_json_response(400, {"error": "No content"})
            return

        if content_length > config["max_size"]:
            self.send_json_response(413, {"error": "File too large"})
            return

        # Get metadata from headers
        filename = self.headers.get("X-Filename", "unknown.jpg")
        date_path = self.headers.get("X-Date-Path", datetime.now().strftime("%Y/%m"))
        device = self.headers.get("X-Device", "iPhone")

        # Sanitize inputs
        filename = os.path.basename(filename)
        date_path = date_path.replace("..", "").strip("/")
        device = device.replace("..", "").replace("/", "_")

        # Build destination path: upload_dir/device/YYYY/MM/filename
        dest_dir = os.path.join(config["upload_dir"], device, date_path)
        dest_path = os.path.join(dest_dir, filename)

        try:
            os.makedirs(dest_dir, exist_ok=True)

            photo_data = self.rfile.read(content_length)

            # Check for duplicate
            if os.path.exists(dest_path):
                existing_hash = self._file_hash(dest_path)
                incoming_hash = hashlib.sha256(photo_data).hexdigest()

                if existing_hash == incoming_hash:
                    logger.info("Duplicate skipped: %s", dest_path)
                    self.send_json_response(200, {
                        "status": "duplicate",
                        "path": dest_path
                    })
                    return
                else:
                    logger.warning("Overwriting changed file: %s", dest_path)

            with open(dest_path, "wb") as f:
                f.write(photo_data)

            logger.info("Saved: %s (%d bytes)", dest_path, content_length)

            self.send_json_response(200, {
                "status": "ok",
                "path": dest_path,
                "size": content_length
            })

        except PermissionError:
            logger.error("Permission denied writing to %s", dest_path)
            self.send_json_response(500, {"error": "Permission denied"})
        except OSError as e:
            logger.error("OS error saving %s: %s", dest_path, str(e))
            self.send_json_response(500, {"error": str(e)})

    def _file_hash(self, filepath: str) -> str:
        """Calculate SHA256 hash of a file."""
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Photo Upload Server for Syncoloco")
    parser.add_argument("--port", type=int, default=8443, help="Port to listen on (default: 8443)")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--upload-dir", required=True, help="Directory to save uploaded photos")
    parser.add_argument("--token", default="", help="API token for authentication (optional)")
    parser.add_argument("--max-size", type=int, default=100, help="Max upload size in MB (default: 100)")

    args = parser.parse_args()

    if not os.path.isdir(args.upload_dir):
        logger.error("Upload directory does not exist: %s", args.upload_dir)
        return 1

    global config
    config = {
        "upload_dir": args.upload_dir,
        "token": args.token,
        "max_size": args.max_size * 1024 * 1024,
    }

    server_address = (args.host, args.port)
    httpd = HTTPServer(server_address, PhotoUploadHandler)

    logger.info("Photo upload server running on http://%s:%d", args.host, args.port)
    logger.info("Upload directory: %s", args.upload_dir)
    logger.info("Authentication: %s", "enabled" if args.token else "disabled")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        httpd.shutdown()

    return 0


if __name__ == "__main__":
    exit(main())
