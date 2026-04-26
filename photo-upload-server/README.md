# Photo Upload Server for Syncoloco

HTTP server that receives photos from Syncoloco and saves them to local filesystem.

## Requirements

- Python 3.6+
- No external dependencies

## Usage

```bash
python3 photo_server.py --upload-dir /path/to/photos [options]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--upload-dir` | (required) | Directory to save uploaded photos |
| `--port` | 8443 | Port to listen on |
| `--host` | 0.0.0.0 | Host to bind to |
| `--token` | (none) | API token for authentication |
| `--max-size` | 100 | Max upload size in MB |

### Example

```bash
python3 photo_server.py --upload-dir /mnt/photos/originals --token mysecrettoken
```

## Installation on Arch Linux ARM

1. Copy files to server:
```bash
sudo mkdir -p /opt/photo-upload-server
sudo cp photo_server.py /opt/photo-upload-server/
sudo chmod +x /opt/photo-upload-server/photo_server.py
```

2. Edit the systemd service file:
```bash
sudo cp photo_server.service /etc/systemd/system/
sudo nano /etc/systemd/system/photo_server.service
```

Update:
- `--upload-dir` to your photos directory
- `--token` to a secure random string
- `User` and `Group` to appropriate values for file permissions

3. Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable photo_server
sudo systemctl start photo_server
```

4. Check status:
```bash
sudo systemctl status photo_server
journalctl -u photo_server -f
```

## API

### Health Check

```
GET /health
```

Response:
```json
{"status": "ok", "timestamp": "2024-01-15T10:30:00"}
```

### Upload Photo

```
POST /upload
Authorization: Bearer <token>
Content-Type: application/octet-stream
X-Filename: IMG_1234.HEIC
X-Date-Path: 2024/01
X-Device: iPhone
X-Photo-ID: abc123
```

Response:
```json
{"status": "ok", "path": "/photos/iPhone/2024/01/IMG_1234.HEIC", "size": 1234567, "photo_id": "abc123"}
```

## Directory Structure

Photos are saved as:
```
{upload_dir}/{device}/{YYYY}/{MM}/{filename}
```

Example:
```
/mnt/photos/originals/iPhone/2024/01/IMG_1234.HEIC
```

## Security

- Run on local network only (don't expose to internet)
- Use a strong random token
- Set appropriate file permissions on upload directory
