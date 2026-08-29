# Ravelin

Phone security console by Kyle. Copyright (c) 2026 Kyle. All rights reserved.

Repo: https://github.com/xz64uj777/Ravelin

This Android project wraps the Ravelin console in a WebView so you can install it as a real app on an S24 FE (or any Android 8+ phone).

## Get the APK from your phone

1. Open this repo on GitHub: [xz64uj777/Ravelin](https://github.com/xz64uj777/Ravelin)
2. Tap **Actions**
3. Tap the workflow named **Build APK**
4. Open the latest run (green check = done)
5. Scroll to **Artifacts**
6. Download **ravelin-debug-apk**
7. Unzip it on the phone
8. Open `app-debug.apk`
9. If Android blocks it: Settings → Apps → special access → Install unknown apps → allow Chrome/Files for this one install
10. Open **Ravelin** from the app drawer

The first GitHub Actions run can take 3–6 minutes. If Actions is empty, tap the workflow, then **Run workflow**.

## What the APK can do

- Full Ravelin UI (Home, Honey pot, Threats, Settings)
- Honey pot decoys, Send to pot, in-app /24 blocks
- File fingerprint (SHA-256 stays on the phone)
- "Show me" buttons that try to open the matching Android Settings screen
- Auto-load updates from this repo when the phone is online

Hard limit: without root, Android will not let any Play-installable app silently kill other apps' processes. Ravelin automates everything Play allows. You still confirm Force stop / Uninstall.

## Build it yourself

```
./gradlew assembleDebug
```

APK output: `app/build/outputs/apk/debug/app-debug.apk`

Build ID: RAVELIN-KYLE-2026-V38
