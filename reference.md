# Reference
## audio
<details><summary><code>client.audio.<a href="src/speechify/audio/client.py">speech</a>(...) -> GetSpeechResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Synthesize speech audio from text or SSML. Returns the complete audio
file plus billing and speech-mark metadata in a single JSON response.
For low-latency playback or long-form text, use POST /v1/audio/stream.
Set `output_format` for explicit sample-rate/bitrate control (e.g.
`pcm_16000` or `ulaw_8000` for telephony).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from speechify import Speechify
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.audio.speech(
    audio_format="mp3",
    input="Hello! This is the Speechify text-to-speech API.",
    model="simba-3.2",
    voice_id="geffen_32",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**input:** `str` 

Plain text or SSML to be synthesized to speech.
Refer to https://docs.speechify.ai/docs/api-limits for the input size limits.
Emotion, Pitch and Speed Rate are configured in the ssml input, please refer to the ssml documentation for more information: https://docs.speechify.ai/docs/ssml#prosody
    
</dd>
</dl>

<dl>
<dd>

**voice_id:** `str` — Id of the voice to be used for synthesizing speech. Refer to /v1/voices endpoint for available voices
    
</dd>
</dl>

<dl>
<dd>

**audio_format:** `typing.Optional[GetSpeechRequestAudioFormat]` — The format for the output audio. Note, that the current default is "wav", but there's no guarantee it will not change in the future. We recommend always passing the specific param you expect.
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` 

Language of the input. Follow the format of an ISO 639-1 language code and an ISO 3166-1 region code, separated by a hyphen, e.g. en-US.
Please refer to the list of the supported languages and recommendations regarding this parameter: https://docs.speechify.ai/docs/language-support.
    
</dd>
</dl>

<dl>
<dd>

**model:** `typing.Optional[GetSpeechRequestModel]` — Model used for audio synthesis. Defaults to `simba-3.0`, which is streaming-native and multilingual: it officially supports English plus `de-DE`, `es-ES`, `es-MX`, `fr-FR`, `it-IT` and `pt-BR`, and routes each request to its English or its multilingual training based on `language` (falling back to the voice's locale when `language` is omitted). `simba-3.2` is the streaming-native model with the lowest TTFB and richest expressivity, and the recommended Simba 3 model; it is English only, so a non-English voice returns 400. `simba-english` and `simba-multilingual` are the legacy Simba 1.6 models, kept for compatibility.
    
</dd>
</dl>

<dl>
<dd>

**options:** `typing.Optional[GetSpeechOptionsRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[AudioOutputFormat]` — The output audio format as a `codec_sampleRate_bitrate` string. Takes precedence over `audio_format` when set.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.audio.<a href="src/speechify/audio/client.py">stream</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Synthesize speech and stream the audio back as it is generated, for
low-latency playback. Set `output_format` in the body for explicit
codec/sample-rate/bitrate control (e.g. `pcm_16000` or `ulaw_8000` for
telephony), or fall back to the Accept header for the container; the
response is raw audio bytes (HTTP chunked). For Base64-encoded audio
with speech-mark metadata in a single JSON response, use
POST /v1/audio/speech.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from speechify import Speechify
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.audio.stream(
    input="input",
    voice_id="voice_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `GetStreamRequest` 
    
</dd>
</dl>

<dl>
<dd>

**accept:** `typing.Optional[StreamAudioRequestAccept]` 

Selects the audio container/codec for the streamed response when
`output_format` is not set in the request body. The response
Content-Type echoes this value, except `audio/pcm` returns
`audio/L16` with rate and channels parameters (raw 16-bit linear
PCM, 24 kHz mono, little-endian). For explicit sample-rate/bitrate
control (e.g. `pcm_16000`, `ulaw_8000`), set `output_format` in the
body instead; it takes precedence over this header.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.audio.<a href="src/speechify/audio/client.py">stream_with_timestamps</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Synthesize speech and stream it back together with word-level speech
marks, for text highlighting, captions and audio-text synchronization
while the audio is still arriving.

The response is a Server-Sent Events stream. Each `speech.chunk` event
carries a Base64-encoded run of audio, the speech marks that became
final with it, or both - a chunk may carry only one of the two, and the
last chunk of a stream is often marks-only. A terminal `speech.done`
event ends the stream; there is no `[DONE]` sentinel. Ignore any event
type you do not recognize, so that new event types do not break your
integration.

Speech-mark times are absolute milliseconds from the start of the
synthesis, so concatenate the audio chunks into one stream and apply the
marks against that single timeline. Which chunk a mark arrives on is a
delivery detail and carries no meaning. Times stay correct for every
`output_format`: changing the codec or sample rate does not change the
duration.

Speech marks are produced by the streaming-native models. The default
`simba-3.0` and `simba-3.2` both serve this route; the legacy
`simba-english` and `simba-multilingual` models return 400
`speech_marks_unsupported` here.
For Base64-encoded audio and speech marks in one non-streamed JSON
response, on any model, use POST /v1/audio/speech.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from speechify import Speechify
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.audio.stream_with_timestamps(
    input="Streaming long-form audio with the Speechify API.",
    model="simba-3.2",
    voice_id="geffen_32",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `GetStreamRequest` 
    
</dd>
</dl>

<dl>
<dd>

**accept:** `typing.Optional[StreamWithTimestampsAudioRequestAccept]` 

Selects the audio container/codec carried inside the events when
`output_format` is not set in the request body. The selected media
type is echoed on the `Speechify-Audio-Content-Type` response
header, since the response's own Content-Type is `text/event-stream`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## models
<details><summary><code>client.models.<a href="src/speechify/models/client.py">list</a>() -> ModelsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List the text-to-speech models available for synthesis. Drive a model
picker from this response, then pass a model `id` as the `model`
parameter to POST /v1/audio/speech or /v1/audio/stream. The response
marks the default model (used when a request omits `model`), the
routes each model may be passed to, and which voices it accepts.
Multi-speaker models arrive in a separate `dialogue_models` array
because they are valid only on POST /v1/audio/dialogue. Returns
the full set in a single response: the model catalog is static
platform reference data, so it is intentionally not paginated.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from speechify import Speechify
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.models.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## voices
<details><summary><code>client.voices.<a href="src/speechify/voices/client.py">list</a>(...) -> ListVoicesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists the voices available to the caller - the shared voice
catalog plus the workspace's cloned voices, whichever member or
service-account key created them. By default
the full catalogue is returned in one response. Pagination is
opt-in: pass `limit` (and then `cursor` from the previous
response) to page through the list while `has_more` is true. Max
page size is 200. Narrow the list with the `type` and `locale`
filters (applied before pagination, so pages stay full).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from speechify import Speechify
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.voices.list(
    locale="en",
    model="simba-3.2",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**cursor:** `typing.Optional[str]` — Opaque pagination cursor from a previous response.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Max items per page (default 50, max 200).
    
</dd>
</dl>

<dl>
<dd>

**type:** `typing.Optional[ListVoicesRequestType]` 

Filter by voice type: `personal` (the workspace's cloned voices)
or `shared` (the public catalogue). Omit to return both.
    
</dd>
</dl>

<dl>
<dd>

**locale:** `typing.Optional[str]` 

Filter to voices whose locale matches this BCP-47 language range,
prefix-matched: `en` matches `en-US` and `en-GB`; `en-US` matches
only `en-US`. Case-insensitive. Omit to return all locales.
    
</dd>
</dl>

<dl>
<dd>

**gender:** `typing.Optional[ListVoicesRequestGender]` — Filter by voice gender. Omit to return all genders.
    
</dd>
</dl>

<dl>
<dd>

**model:** `typing.Optional[str]` 

Filter to voices that support this model (as listed in each voice's
`models[]`), e.g. `simba-3.2`. Omit to return voices for all models.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/speechify/voices/client.py">create</a>(...) -> GetVoice</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a cloned voice for the workspace from a 10-30 second audio sample, with verified consent from the speaker.

Cloning requires proof that the speaker agreed to it. Create a consent challenge with `POST /v1/voices/consent-challenges`, show the returned `phrase` to the speaker, record them reading it aloud, and send that recording here as `consent_recording` together with the challenge's `consent_challenge_id`. Speechify transcribes the recording, checks it against the phrase it issued, checks that its speaker is the speaker in your `sample`, and keeps it as the consent record for the voice. The person consenting therefore has to be the person being cloned. A challenge is single use and short-lived, so record and submit in one sitting.

The clone belongs to the workspace rather than the member who created it, and access follows the caller's workspace role and API-key scopes exactly as for any other voice: voices scopes to list it, audio scopes to synthesize with it, and the content-management permission plus a write scope on the key to delete it. Cloned voices are usable self-serve on `simba-3.0`, `simba-english` and `simba-multilingual`. `simba-3.2` also serves cloned voices, currently as a limited release enabled per workspace; contact Speechify to have it enabled for yours.

Callers pinned before `Speechify-Version: 2026-09-13` use the previous flow instead: no challenge, and a `consent` form field carrying the speaker's name and email as a JSON string. That flow is deprecated and will be removed after a sunset window announced in the changelog.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from speechify import Speechify
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.voices.create(
    idempotency_key="a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
    sample="example_sample",
    avatar="example_avatar",
    consent_recording="example_consent_recording",
    name="name",
    gender="male",
    consent_challenge_id="consent_challenge_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — Name of the personal voice
    
</dd>
</dl>

<dl>
<dd>

**gender:** `CreateVoicesRequestGender` 

Gender marker for the personal voice
male GenderMale
female GenderFemale
not_specified GenderNotSpecified
    
</dd>
</dl>

<dl>
<dd>

**sample:** `core.File` — Audio sample of the voice to clone, 10-30 seconds of clean speech.
    
</dd>
</dl>

<dl>
<dd>

**consent_challenge_id:** `str` 

The `id` of the consent challenge this create consumes, from
`POST /v1/voices/consent-challenges`. Single use: once a
create has consumed it, whether or not that create
succeeded, it cannot be used again.
    
</dd>
</dl>

<dl>
<dd>

**consent_recording:** `core.File` 

Recording of the speaker reading the challenge's `phrase`
aloud. This is the consent record for the voice, not a
second voice sample: it must be the same person as in
`sample`, and it is retained as evidence. 5-30 seconds, at
most 25 MB, in any common audio container.
    
</dd>
</dl>

<dl>
<dd>

**idempotency_key:** `typing.Optional[str]` 

A client-generated key (an opaque string, max 255 chars) that makes a
side-effect POST safe to retry: the server runs the operation exactly
once and replays the first response (its status and body) for 24 hours.
Reusing a key with a different request body, or while the first request
is still in flight, returns `409 idempotency_conflict`. A replayed
response carries the `Idempotent-Replayed: true` header.
    
</dd>
</dl>

<dl>
<dd>

**locale:** `typing.Optional[str]` — Native language (locale) of the personal voice (e.g. en-US, es-ES, etc.)
    
</dd>
</dl>

<dl>
<dd>

**avatar:** `typing.Optional[core.File]` — Avatar image file
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/speechify/voices/client.py">get</a>(...) -> GetVoice</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetch a single voice by id - a shared catalogue voice or one of
the workspace's cloned voices. A cloned voice that belongs to
another workspace returns 404, identical to an unknown id, so
voice inventory is never enumerable across tenants.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from speechify import Speechify
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.voices.get(
    voice_id="voice_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — The ID of the voice to fetch
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/speechify/voices/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete one of the workspace's cloned voices. Requires the
`content.manage` permission (owner, admin, or member); a
service-account key is authorized by its scopes instead.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from speechify import Speechify
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.voices.delete(
    voice_id="voice_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — The ID of the voice to delete
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/speechify/voices/client.py">download_sample</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Download a personal (cloned) voice sample
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from speechify import Speechify
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.voices.download_sample(
    voice_id="voice_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — The ID of the voice to download sample for
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Voices ConsentChallenges
<details><summary><code>client.voices.consent_challenges.<a href="src/speechify/voices/consent_challenges/client.py">create</a>(...) -> ConsentChallenge</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Start the consent check for a voice clone.

Returns a `phrase` for the speaker to read aloud and an `id` that identifies this challenge. Show the phrase to the speaker exactly as returned, record them reading it, then send the recording and the `id` to `POST /v1/voices`, which verifies the recording against the phrase and against the voice sample being cloned, then keeps it as the consent record.

A challenge is single use, is bound to the workspace that created it, and expires at `expires_at` - it is proof that a speaker was in front of a microphone just now, so create it when you are ready to record, not at the start of your flow. If it expires, create another one and record again.

Challenge creation is rate limited per workspace at a few dozen per hour, far more tightly than the rest of the voice surface, because each one precedes a person recording themselves - mint it when your speaker is ready, not speculatively. Read the live ceiling off `RateLimit-*` rather than hard-coding it. **On a `429`, always honour `Retry-After` rather than a fixed backoff of your own**: the wait is measured in minutes and can run to most of an hour. `RateLimit-*` are omitted rather than reporting a bucket that is not the one refusing.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from speechify import Speechify
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.voices.consent_challenges.create(
    idempotency_key="a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
    full_name="Jane Doe",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**full_name:** `str` 

Full name of the person consenting to have their voice cloned.
Speechify binds it to the challenge and stores it with the consent
record, so the create that consumes the challenge does not carry it
and cannot change it.

At most 120 bytes once UTF-8 encoded, which is 120 characters of
Latin script but around 40 of Chinese, Japanese or Korean. Stated in
bytes rather than as a `maxLength` because the two only agree on
single-byte scripts, and a character count that never over-accepts
would have to refuse Latin names at 30. A name over the limit comes
back as `validation_failed` reporting its measured length.
    
</dd>
</dl>

<dl>
<dd>

**idempotency_key:** `typing.Optional[str]` 

A client-generated key (an opaque string, max 255 chars) that makes a
side-effect POST safe to retry: the server runs the operation exactly
once and replays the first response (its status and body) for 24 hours.
Reusing a key with a different request body, or while the first request
is still in flight, returns `409 idempotency_conflict`. A replayed
response carries the `Idempotent-Replayed: true` header.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

