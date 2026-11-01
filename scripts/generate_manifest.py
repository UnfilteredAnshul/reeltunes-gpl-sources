#!/usr/bin/env python3
"""Generate manifest/components.json.

Records, for every third-party component that carries a copyleft licence
obligation in the ReelTunes Android app, the exact artifact identity
(version + SHA-256) that was used to build the shipped package.

Run this before publishing a release:

    python scripts/generate_manifest.py --gradle-cache %USERPROFILE%/.gradle

The hashes are what makes the "corresponding source" claim checkable: a user
can hash the .so files inside a downloaded APK and compare them with
manifest/components.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import zipfile
from datetime import datetime, timezone

GROUP = "io.github.junkfood02.youtubedl-android"
VERSION = "0.18.1"

# artifact name -> files inside the AAR whose hashes we publish
AAR_PAYLOADS = {
    "library": [
        "jni/arm64-v8a/libpython.so",
        "jni/arm64-v8a/libpython.zip.so",
        "jni/arm64-v8a/libqjs.so",
        "res/raw/ytdlp",
    ],
    "ffmpeg": [
        "jni/arm64-v8a/libffmpeg.so",
        "jni/arm64-v8a/libffmpeg.zip.so",
        "jni/arm64-v8a/libffprobe.so",
    ],
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_aar(cache: str, artifact: str) -> str | None:
    root = os.path.join(
        cache, "modules-2", "files-2.1", GROUP, artifact, VERSION
    )
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".aar"):
                return os.path.join(dirpath, name)
    return None


def yt_dlp_meta(zipapp: bytes) -> dict:
    """Read the version metadata out of the bundled yt-dlp zipapp."""
    offset = zipapp.find(b"PK\x03\x04")
    if offset < 0:
        return {}
    import io

    with zipfile.ZipFile(io.BytesIO(zipapp[offset:])) as zf:
        raw = zf.read("yt_dlp/version.py").decode("utf-8", "replace")
    meta = {}
    for line in raw.splitlines():
        if "=" in line and not line.strip().startswith("#"):
            key, _, value = line.partition("=")
            meta[key.strip()] = value.strip().strip("'\"")
    return {
        "version": meta.get("__version__"),
        "git_head": meta.get("RELEASE_GIT_HEAD"),
        "channel": meta.get("CHANNEL"),
        "origin": meta.get("ORIGIN"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--gradle-cache",
        default=os.path.expanduser("~/.gradle"),
        help="Gradle user home (default: ~/.gradle)",
    )
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    out_path = args.out or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "manifest",
        "components.json",
    )

    components = []

    for artifact, payloads in AAR_PAYLOADS.items():
        aar = find_aar(args.gradle_cache, artifact)
        if not aar:
            print(f"missing AAR: {GROUP}:{artifact}:{VERSION}", file=sys.stderr)
            return 1
        entry = {
            "component": f"{GROUP}:{artifact}",
            "version": VERSION,
            "licence": "GPL-3.0-only",
            "artifact": os.path.basename(aar),
            "artifact_sha256": sha256_file(aar),
            "artifact_bytes": os.path.getsize(aar),
            "payload": [],
            "modified_by_reeltunes": False,
        }
        with zipfile.ZipFile(aar) as zf:
            for name in payloads:
                data = zf.read(name)
                item = {
                    "path": name,
                    "bytes": len(data),
                    "sha256": sha256_bytes(data),
                }
                if name == "res/raw/ytdlp":
                    item["yt_dlp"] = yt_dlp_meta(data)
                entry["payload"].append(item)
        components.append(entry)

    manifest = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "app": "ReelTunes (com.buildwithanshul.reeltunes)",
        "platform_abi_documented": "arm64-v8a",
        "note": (
            "Only components with copyleft obligations are listed. Files are "
            "shipped unmodified; the hashes above are the hashes of the bytes "
            "packaged into the APK."
        ),
        "components": components,
    }

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
