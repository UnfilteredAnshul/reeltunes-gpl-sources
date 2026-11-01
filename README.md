# ReelTunes — third-party engine sources and notices

This repository is the licence-compliance home for the **copyleft components that
ship inside the ReelTunes Android app** (`com.buildwithanshul.reeltunes`).

It exists so that anyone who receives a ReelTunes build can obtain the
corresponding source, the licence texts, and the exact identity of the binaries
that were bundled.

## What is bundled

ReelTunes embeds a Python-based media extractor so audio can be saved on the
device. Three upstream projects are involved:

| Component | Version | Licence | Role in the app |
|---|---|---|---|
| [youtubedl-android](https://github.com/JunkFood02/youtubedl-android) `library` | 0.18.1 | GPL-3.0 | JNI wrapper, embedded CPython 3.12, bundled yt-dlp |
| [youtubedl-android](https://github.com/JunkFood02/youtubedl-android) `ffmpeg` | 0.18.1 | GPL-3.0 | FFmpeg 7.1 "full" build (`--enable-gpl --enable-version3`) |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | 2025.11.12 | Unlicense | extractor, shipped as the bundled zipapp |
| [CPython](https://github.com/python/cpython) | 3.12 | PSF-2.0 | interpreter inside `libpython.zip.so` |
| [ytdlp_flutter](https://pub.dev/packages/ytdlp_flutter) | 0.1.0 | MIT | Dart/Kotlin bridge used by the app |

The engine binaries are **unmodified** upstream artifacts. ReelTunes does not
patch, rebuild, or re-sign them; it consumes them from Maven Central and pub.dev
at build time.

## Where the corresponding source is

* `SOURCE_OFFER.md` — the written offer required by GPLv3 §6, with a contact
  address. This is the reliable route for the FFmpeg and youtubedl-android
  sources.
* `manifest/components.json` — SHA-256 of every copyleft file that is packaged
  into the APK, plus the version/commit of the bundled yt-dlp zipapp.
* `BUILD.md` — how the binaries are produced upstream and how the app consumes
  them.
* `LICENSES/` — full licence texts.

## Verifying a build

```bash
python scripts/verify_apk.py path/to/app-release.apk
```

Every listed component is hashed and compared against
`manifest/components.json`. A match means the binaries in your copy are the ones
described here.

## Scope

This repository intentionally does **not** contain the ReelTunes application
code. It contains only what is required to satisfy the licences of the bundled
third-party components.

Contact: **contact.unfiltered.anshul@gmail.com**
