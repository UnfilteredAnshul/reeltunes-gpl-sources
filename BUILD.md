# How the bundled binaries are produced

ReelTunes does not build the engine itself. It consumes prebuilt artifacts and
packages them into the APK. This document records exactly which artifacts, so
the build is reproducible and the corresponding source can be identified.

## Artifact consumption

`pubspec.yaml` (app):

```yaml
dependencies:
  ytdlp_flutter: ^0.1.0
```

`ytdlp_flutter` declares, in its Android module:

```kotlin
implementation("io.github.junkfood02.youtubedl-android:library:0.18.1")
implementation("io.github.junkfood02.youtubedl-android:ffmpeg:0.18.1")
```

Those coordinates resolve to AARs on Maven Central:

* <https://repo1.maven.org/maven2/io/github/junkfood02/youtubedl-android/library/0.18.1/>
* <https://repo1.maven.org/maven2/io/github/junkfood02/youtubedl-android/ffmpeg/0.18.1/>

The AAR contents are merged into the APK by the Android Gradle Plugin. The
`ffmpeg` AAR contributes `libffmpeg.so`, `libffprobe.so` (JNI),
`libffmpeg.zip.so` (a zip holding the FFmpeg 7.1 binary and its shared
libraries), and the `library` AAR contributes `libpython.so`,
`libpython.zip.so` (CPython 3.12 + stdlib), `libqjs.so`, and
`res/raw/ytdlp` (the yt-dlp zipapp).

## Upstream build

The binaries are produced by the youtubedl-android project:
<https://github.com/JunkFood02/youtubedl-android>. Its `library` module runs a
Python build (CPython for Android) and its `ffmpeg` module runs an FFmpeg
build with `--enable-gpl --enable-version3` plus a set of third-party codec
libraries.

## Local change: no runtime engine downloads

Upstream `ytdlp_flutter` calls `YoutubeDL.updateYoutubeDL(...)` during
initialisation, which fetches a new yt-dlp zipapp from the network on first run.

ReelTunes vendors the bridge locally and removes that call, so the extractor
shipped in the APK is the only extractor that ever runs. New yt-dlp versions
reach users through a normal Google Play app update.

The bundled yt-dlp version is recorded in `manifest/components.json`
(`yt_dlp.version`). When it changes, regenerate the manifest:

```bash
python scripts/generate_manifest.py --gradle-cache ~/.gradle/caches
```

## Reproducing the app build

1. Install Flutter (stable) and the Android SDK, `compileSdk`/`targetSdk` 36.
2. `flutter pub get`
3. `flutter build appbundle --release` (or `--split-per-abi`)
4. `python scripts/verify_apk.py build/app/outputs/flutter-apk/app-arm64-v8a-release.apk`

Step 4 confirms the copyleft binaries match the published manifest.
