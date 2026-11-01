# Written offer of corresponding source (GPLv3 §6)

ReelTunes (`com.buildwithanshul.reeltunes`) is distributed as an Android
application package that contains object code from the following GPL-3.0
projects:

* **youtubedl-android 0.18.1** — `library`, `ffmpeg`, `common`
  (io.github.junkfood02.youtubedl-android), GPL-3.0
* **FFmpeg 7.1** — the "full" build with `--enable-gpl --enable-version3`,
  as packaged by youtubedl-android 0.18.1, GPL-3.0

In accordance with section 6 of the GNU General Public License version 3, the
distributor of ReelTunes hereby offers, to any third party, the **complete
corresponding source code** for the GPL-licensed object code contained in any
ReelTunes release, for a period of **three (3) years** from the date that
release was distributed.

## How to request

Email **contact.unfiltered.anshul@gmail.com** with the subject line
`GPL source request` and state which ReelTunes version you received
(for example `ReelTunes 1.0.0 (versionCode 1)`).

Include the SHA-256 values you see in `manifest/components.json` if you want the
response tied to a specific build.

## What you receive

* The source of the youtubedl-android modules at the released version, including
  the Gradle build scripts and the FFmpeg build configuration used to produce
  the bundled binaries.
* The FFmpeg 7.1 source tree with the configuration and patches used for that
  build, plus the sources of the third-party libraries linked into it.
* The build scripts needed to reproduce the binaries.
* A copy of `LICENSES/GPL-3.0.txt`.

Delivery is by download link (no charge) or, on request, on physical media for a
fee covering only the cost of the media and shipping, as permitted by GPLv3 §6.

## Source already published

The distributed components are unmodified upstream artifacts, so the
majority of the source is also directly available:

* youtubedl-android — <https://github.com/JunkFood02/youtubedl-android>
  (Maven Central coordinates `io.github.junkfood02.youtubedl-android:{library,ffmpeg,common}:0.18.1`).
  Note: the 0.18.1 artifacts are published to Maven Central; upstream's git
  tags currently stop at 0.17.2, which is why this written offer exists as the
  authoritative route for 0.18.1.
* FFmpeg 7.1 — <https://ffmpeg.org/releases/ffmpeg-7.1.tar.xz>
* yt-dlp 2025.11.12 — <https://github.com/yt-dlp/yt-dlp/tree/335653be82d5ef999cfc2879d005397402eebec1>
  (commit recorded in the bundled zipapp's `yt_dlp/version.py`)

## No warranty

The source is provided without warranty of any kind, to the extent permitted by
applicable law.
