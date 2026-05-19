# Syncoloco

iOS app that syncs your photos and videos from the Photos library to your own NAS or home server — no cloud, no subscription, no third parties.

Your media stays on your local network. Originals only, with EXIF and embedded tags preserved.

> **Designed for trusted home networks only. Not recommended on public Wi‑Fi, and never over the open internet.**
>

## Syncoloco Support

  For help, questions, or to report a bug, please [email us](mailto:support.roiz@icloud.com)

  You can also report issues on [GitHub](https://github.com/roiz-git/Syncoloco/issues).


## Features

- Sync to a NAS over **NFS**, **SMB**, or **HTTP** (companion server)
- Background sync via iOS BackgroundTasks
- Live Activity shows progress on the Lock Screen and Dynamic Island
- Duplicate detection (skips already-uploaded photos by hash / size)
- Supports photos (HEIC, JPEG, PNG) and videos (MOV, MP4)
- Per-device folders — files organized as `{device}/{YYYY}/{MM}/{filename}`
- Optional "keep screen on while syncing" for long runs
- Credentials stored in the iOS Keychain

## Requirements

- iOS 26 or later
- A NAS or any machine on your LAN reachable over NFS, SMB, or HTTP

## Sync protocols

### NFS

Point Syncoloco at your NFS server and export path (e.g. `/srv/nfs/photos`). Anonymous mounts are supported.

### SMB

Works with guest shares and authenticated shares. Enter the server address, share name, and credentials (stored in Keychain).

### HTTP (companion server)

A small Python server is provided for users who prefer not to run NFS/SMB. It's a single-file HTTP server that receives uploads and writes them to disk with the same folder layout as the other protocols.

Companion server: [photo-upload-server](https://github.com/roiz-git/Syncoloco/tree/main/photo-upload-server)

Quick setup on a Linux box:

```bash
python3 photo_server.py --upload-dir /mnt/photos --token your-secret-token
```

Then in Syncoloco, set HTTP protocol, server `http://<host>:8443`, and paste the token.

The server's README covers systemd installation and the full API.

## Privacy

- Syncoloco talks only to the server you configure. No analytics, no cloud, no third-party services.
- HTTP and SMB credentials are stored in the iOS Keychain.
- The `NSAllowsLocalNetworking` entitlement restricts networking to your LAN.
