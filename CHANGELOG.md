# Changelog

## [4.0.0](https://github.com/Speechify-AI/sdk-python/compare/3.0.1...4.0.0) (2026-08-18)


### ⚠ BREAKING CHANGES

* the default API version is now 2026-09-13.

### Features

* regenerate SDK for API 2026-09-13 with consent-challenge voice cloning ([#27](https://github.com/Speechify-AI/sdk-python/issues/27)) ([f3f323d](https://github.com/Speechify-AI/sdk-python/commit/f3f323dcba6f9aa9290be47ef8bbcaff06987d18))

## [3.0.1](https://github.com/SpeechifyInc/speechify-api-sdk-python/compare/3.0.0...3.0.1) (2026-07-10)


### Bug Fixes

* correct SDK version strings and release 3.0.1 ([#24](https://github.com/SpeechifyInc/speechify-api-sdk-python/issues/24)) ([cdb080e](https://github.com/SpeechifyInc/speechify-api-sdk-python/commit/cdb080e3253b1bedb07827b7cd8fe80904102d82))


### Documentation

* add AGENTS.md with release/publish safeguards ([#22](https://github.com/SpeechifyInc/speechify-api-sdk-python/issues/22)) ([c4e1ad3](https://github.com/SpeechifyInc/speechify-api-sdk-python/commit/c4e1ad3ffa096543efa2cdd9195764cb5e9d346f))

## [3.0.0](https://github.com/SpeechifyInc/speechify-api-sdk-python/compare/2.0.0...3.0.0) (2026-07-10)


### ⚠ BREAKING CHANGES

* removed voice types `CreatedVoice`, `CreateVoiceModel`, `CreateVoiceLanguage`, `CreateVoiceModelName`, `CreatedVoiceGender`, `CreatedVoiceType`; `GetSpeechResponse.audio_format` redocumented as the audio codec. Additive: new `ErrorCode` values, `output_format` field, `PaginationMeta` / `ListVoicesResponse`, `ConflictError`.

### Features

* regenerate SDK on fern-python-sdk@5.14.20 (TTS surface) ([#18](https://github.com/SpeechifyInc/speechify-api-sdk-python/issues/18)) ([02b6449](https://github.com/SpeechifyInc/speechify-api-sdk-python/commit/02b6449520da46ebcfa05bc5a82d63e482fc12df))

## [2.0.0](https://github.com/SpeechifyInc/speechify-api-sdk-python/compare/1.2.3...2.0.0) (2026-06-22)


### ⚠ BREAKING CHANGES

* `Speechify(token=...)` is now `Speechify(api_key=...)`. The `tts.` namespace has been removed — call sites move from `client.tts.audio.speech(...)` to `client.audio.speech(...)` and from `client.tts.voices.X` to `client.voices.X`. The `livekit` extra-dependency has been removed; if you were importing it transitively through `speechify-api`, install it explicitly. Generator-line crossed `4.x` → `5.x`, so internal/private code paths have moved.

### Features

* regenerate SDK on fern-python-sdk@5.14.20 with TTS-only surface ([#16](https://github.com/SpeechifyInc/speechify-api-sdk-python/issues/16)) ([2ebb0a5](https://github.com/SpeechifyInc/speechify-api-sdk-python/commit/2ebb0a5e81ec11eab11215f932fb3f529edaf890))
