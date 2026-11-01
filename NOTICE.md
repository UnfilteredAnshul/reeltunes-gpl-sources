# Third-party notices

ReelTunes includes the components below. Full licence texts are in `LICENSES/`.

---

## youtubedl-android 0.18.1 — GPL-3.0

Copyright © the youtubedl-android contributors
(<https://github.com/JunkFood02/youtubedl-android>), originally by yausername.

ReelTunes uses the `library`, `ffmpeg`, and `common` artifacts from Maven Central
under the coordinates `io.github.junkfood02.youtubedl-android:*:0.18.1`.

The `library` artifact embeds:

* **CPython 3.12** — Copyright © Python Software Foundation, PSF-2.0.
  See `LICENSES/PSF-2.0.txt`.
* **QuickJS (`libqjs.so`)** — Copyright © Fabrice Bellard and contributors, MIT.
* **yt-dlp 2025.11.12** — released into the public domain (Unlicense).
  See `LICENSES/UNLICENSE.txt`. Upstream commit
  `335653be82d5ef999cfc2879d005397402eebec1`.

The `ffmpeg` artifact contains an **FFmpeg 7.1** build configured with
`--enable-gpl --enable-version3`. That build links GPL-licensed libraries
including x264, x265, xvid, vidstab, and rubberband, and LGPL-licensed libav*
libraries. FFmpeg is Copyright © the FFmpeg developers
(<https://ffmpeg.org>). See `LICENSES/GPL-3.0.txt`.

### Modifications

None. ReelTunes ships these artifacts byte-for-byte as published. The SHA-256
values in `manifest/components.json` are the hashes of the files inside the
shipped APK.

### Source

See `SOURCE_OFFER.md`.

---

## ytdlp_flutter 0.1.0 — MIT

Copyright © c statecs. Used as the Dart/Kotlin bridge that calls the engine.
See `LICENSES/MIT-ytdlp_flutter.txt`.

ReelTunes uses a locally vendored copy of this package with the automatic
engine-update call removed, so the app does not download executable code at
runtime. The change is confined to the bridge and is described in `BUILD.md`.

---

## Other dependencies

The remaining Flutter/Dart and Android dependencies (`just_audio`,
`audio_service`, `file_picker`, `path_provider`, `shared_preferences`,
`url_launcher`, `receive_intent`, `reorderable_grid_view`, `audio_session`, the
Flutter engine, and the AndroidX libraries) are licensed under MIT, BSD-3-Clause,
or Apache-2.0. Their notices are included in the app's
`assets/flutter_assets/NOTICES.Z` bundle, which Flutter generates from the
package licences at build time.
