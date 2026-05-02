# Syncoloco Privacy Policy

## Overview

Syncoloco is an iOS app that syncs photos and videos from your Photos library to your own NAS or home server over your local network. Your privacy is important to us. This policy explains what data Syncoloco collects, stores, and transmits.

## Data Collection

**Syncoloco does not collect any personal data.**

We do not:
- Collect analytics or usage data
- Track your location
- Share any data with third parties
- Use advertising or ad tracking
- Upload your photos, videos, or metadata to any server operated by us

## Photo Library Access

Syncoloco requests access to your Photos library for one purpose only: to read photos and videos so they can be copied to the server you configure. Media is transferred directly from your device to your server — it does not pass through any Syncoloco-operated infrastructure.

## Data Storage

Syncoloco stores the following data **locally on your device only**:

- **Server settings**: Protocol choice (NFS / SMB / HTTP), hostname, share or export path, device name
- **Credentials**: SMB username and password, and the HTTP token if used, stored in the iOS Keychain
- **Sync manifest**: A record of which photos have already been synced, used to skip duplicates on subsequent runs
- **Logs**: Recent sync activity for troubleshooting, kept in memory and optionally shared by you via the Share Logs button

This data never leaves your device and is not transmitted to us or any third party.

## Network Connections

Syncoloco connects only to:

1. **Your NAS or server**: The NFS, SMB, or HTTP server you configure in the app. Photos and videos are transferred directly to this server over your local network.

2. **Local network discovery**: Syncoloco uses Bonjour / mDNS to discover SMB servers on your local network. This is a local-only protocol and does not transmit data over the internet.

3. **Apple App Store**: For subscription management and purchases through Apple's standard StoreKit framework.

Syncoloco is designed for trusted home networks only. It does not use TLS for NFS, SMB, or HTTP transport, and is not recommended on public Wi‑Fi or over the open internet.

## Subscriptions

Syncoloco offers subscription-based access. Subscription purchases and management are handled entirely by Apple through the App Store. We do not have access to your payment information.

## Data Deletion

All app data is stored locally on your device. To delete all Syncoloco data:
- Delete the app from your device

This removes all stored settings, sync manifests, cached logs, and credentials held in the Keychain scoped to the app.

## Children's Privacy

Syncoloco does not knowingly collect any information from children under 13. The app is a photo-sync utility with no social features or data collection.

## Changes to This Policy

We may update this privacy policy from time to time. Any changes will be reflected in the "Last Updated" date above.

## Contact

If you have questions about this privacy policy, please contact us at:

- GitHub: https://github.com/roiz-git/Syncoloco/issues

## Summary

- No data collection
- No analytics or tracking
- No advertising
- All data stored locally on your device
- Photos and videos sent only to servers you configure, over your local network
- Subscriptions handled by Apple
