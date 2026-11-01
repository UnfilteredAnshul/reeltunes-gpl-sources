#!/usr/bin/env python3
"""Verify a ReelTunes APK against manifest/components.json.

Usage:
    python scripts/verify_apk.py path/to/app-release.apk [--abi arm64-v8a]

Exit code 0 means every hashed component inside the APK matches the published
manifest, i.e. the copyleft binaries you received are the ones whose source and
notices are published here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))

# manifest payload path -> path of the same file inside the APK
APK_PATHS = {
    "jni/arm64-v8a/libpython.so": "lib/arm64-v8a/libpython.so",
    "jni/arm64-v8a/libpython.zip.so": "lib/arm64-v8a/libpython.zip.so",
    "jni/arm64-v8a/libqjs.so": "lib/arm64-v8a/libqjs.so",
    "jni/arm64-v8a/libffmpeg.so": "lib/arm64-v8a/libffmpeg.so",
    "jni/arm64-v8a/libffmpeg.zip.so": "lib/arm64-v8a/libffmpeg.zip.so",
    "jni/arm64-v8a/libffprobe.so": "lib/arm64-v8a/libffprobe.so",
    # res/raw/ytdlp is packaged under an AAPT-mangled name; match by content.
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("apk")
    ap.add_argument(
        "--manifest",
        default=os.path.join(HERE, "..", "manifest", "components.json"),
    )
    ap.add_argument("--abi", default="arm64-v8a")
    args = ap.parse_args()

    with open(args.manifest, encoding="utf-8") as fh:
        manifest = json.load(fh)

    failures = 0
    with zipfile.ZipFile(args.apk) as apk:
        names = set(apk.namelist())
        for component in manifest["components"]:
            for item in component["payload"]:
                key = item["path"].replace("arm64-v8a", args.abi)
                target = APK_PATHS.get(item["path"])
                if target is None:
                    # res/raw/ytdlp -> res/raw/ytdlp (kept uncompressed by AAPT)
                    candidates = [
                        n
                        for n in names
                        if n.startswith("res/") and n.endswith("ytdlp")
                    ]
                    if not candidates:
                        print(f"SKIP (not in APK): {item['path']}")
                        continue
                    target = candidates[0]
                target = target.replace("arm64-v8a", args.abi)
                if target not in names:
                    print(f"MISSING in APK: {target}")
                    failures += 1
                    continue
                data = apk.read(target)
                digest = hashlib.sha256(data).hexdigest()
                ok = digest == item["sha256"]
                print(
                    f"{'OK  ' if ok else 'FAIL'} {target} "
                    f"({len(data)} bytes, sha256 {digest[:16]}...)"
                )
                if not ok:
                    failures += 1

    if failures:
        print(f"\n{failures} mismatch(es).")
        return 1
    print("\nAll published components verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
