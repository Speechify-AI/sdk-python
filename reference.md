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

**model:** `typing.Optional[GetSpeechRequestModel]` 

Model used for audio synthesis. Defaults to `simba-3.0`, which is streaming-native and multilingual: it officially supports English plus `de-DE`, `es-ES`, `es-MX`, `fr-FR`, `it-IT` and `pt-BR`, and routes each request to its English or its multilingual training based on `language` (falling back to the voice's locale when `language` is omitted). `simba-3.2` is the streaming-native model with the lowest TTFB and richest expressivity, and the recommended Simba 3 model; it is English only, so a non-English voice returns 400.

The legacy Simba 1.6 models `simba-english` and `simba-multilingual` are retired from API version `2026-09-21`: naming one returns 400 `model_retired`. Pinning your API version to a date before `2026-09-21` keeps them on their Simba 1.6 training until **2026-11-21**; from then both ids are served by our current models on every API version that can still name them. Migrate to `simba-3.2` (English) or `simba-3.0` before then; call GET /v1/audio/models to see the set your workspace can select today.
    
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

**safety_identifier:** `typing.Optional[SafetyIdentifier]` — Optional. A stable, opaque identifier for the end user this request is made for: a hash of your own user id or an opaque id, never an email address or other personal data. It is recorded with the request even under zero data retention, and your workspace can be given per-end-user limits and a block list keyed on it. See https://docs.speechify.ai/build/guides/concepts/safety-identifiers.
    
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

Every model this route accepts produces speech marks here. The default
`simba-3.0` and `simba-3.2` stream marks word by word alongside the
audio. The legacy `simba-english` and `simba-multilingual` models,
still selectable on a workspace pinned before API version `2026-09-21`,
synthesize a sentence at a time, so their marks arrive a sentence at a
time with that sentence's audio; from that version on they return 400
`model_retired` on every synthesis route, and from 2026-11-21 both ids
are served by our current models.
For Base64-encoded audio and speech marks in one non-streamed JSON
response, use POST /v1/audio/speech.
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
catalog plus the cloned voices they can reach, whichever member or
service-account key created them. A clone filed under a project is
listed only for a caller who can reach that project; a clone no
project filed is shared with the whole workspace and is listed for
everyone in it. By default
the full catalogue is returned in one response. Pagination is
opt-in: pass `limit` (and then `cursor` from the previous
response) to page through the list while `has_more` is true. Max
page size is 200. Narrow the list with the `type` and `locale`
filters.

A page can come back with fewer than `limit` voices, and a short
page - an empty one included - is not the end of the list. Keep
following `next_cursor` while `has_more` is true.
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
    project_id="proj_01arz3ndektsv4rrffq69g5fav",
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

**project_id:** `typing.Optional[str]` 

Filter cloned voices by workspace project: omit for every voice you
can reach, pass the literal `shared` for the clones no project
filed, or a `proj_...` id for the clones filed under that project.
The shared catalog carries no project and is returned either way.

A clone is filed under a project when a project-pinned key created
it. A clone with no project is shared with the whole workspace
rather than sitting in a Default project, so the literal here is
`shared`, never `default` - passing `default` is a 400. Returns 404
project_not_found for a malformed id and for any project outside
your reach: a project-pinned key reaches only its pinned project,
and a member holding project grants reaches only the granted ones.
That 404 is the same in every case and does not reveal whether such
a project exists. `shared` is always inside your reach.
    
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

The clone belongs to the workspace rather than the member who created it, and access follows the caller's workspace role and API-key scopes exactly as for any other voice: voices scopes to list it, audio scopes to synthesize with it, and the content-management permission plus a write scope on the key to delete it. Cloned voices are usable self-serve on `simba-3.0` (and, on a workspace pinned before API version `2026-09-21`, on the retired `simba-english` and `simba-multilingual`, which from 2026-11-21 are served by our current models and still take cloned voices). `simba-3.2` also serves cloned voices.

The previous flow, a `consent` form field carrying the speaker's name and email as a JSON string, was switched off on 2026-09-23 for every API version: a create that sends `consent` and no `consent_challenge_id` returns 400 `consent_verification_required`.

Voice cloning is not available in some jurisdictions. A request from one returns 403 `voice_cloning_unavailable_in_region` before consent verification runs, so it does not spend the challenge. The location is read from the IP address that sends the request, which is your server's when your backend calls the API; a location header in the request is ignored.
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

A voice that is also a member's personal voice (one cloned
before workspaces owned voices and adopted into this workspace)
is removed from the workspace only; the person keeps it.
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

## projects
<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">list</a>(...) -> ListProjectsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List the workspace's projects, newest first. The implicit Default
project is not a row and is never listed; resources with no
`project_id` live in it. Archived projects are hidden unless
`include_archived=true`, and purged ones unless
`include_purged=true`. Cursor-paginated: omit `cursor` for the
first page; walk pages while `has_more` is true (default page size
50, max 200).
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

client.projects.list()

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

**include_archived:** `typing.Optional[bool]` 

Include archived projects. Defaults to `false`, so the list shows
only live projects; archived ones stay readable by id.
    
</dd>
</dl>

<dl>
<dd>

**include_purged:** `typing.Optional[bool]` 

Include purged projects that are still inside their 30-day restore
window, each carrying the `purged_at` stamp its deadline is
measured from. Defaults to `false`, so the list shows only projects
that still exist. This is the only read that returns a purged
project: the by-id read answers 404 for one, and a project past its
window is never listed, because it is awaiting permanent deletion
and a restore would refuse it. Independent of `include_archived`:
a purge runs only from the archived state, so asking for purged
projects never means asking for every archived one as well.
    
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

<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">create</a>(...) -> Project</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a project in the caller's workspace. Names are unique per
workspace (case-insensitive). A workspace holds at most 100 live
projects; at the cap the create refuses with
`409 project_limit_reached` until one is deleted.
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

client.projects.create(
    name="Production",
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

**name:** `str` 

Project name; unique per workspace (case-insensitive),
surrounding whitespace is trimmed.
    
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

<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">get</a>(...) -> Project</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetch one project by id, scoped to the caller's workspace. Returns
404 for missing or foreign-workspace projects — project existence
is never leaked across workspaces.
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

client.projects.get(
    project_id="proj_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**project_id:** `str` — Project id (prefixed external id, `proj_...`).
    
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

<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a project. With no body it deletes a project that holds
nothing, and refuses one that does; `mode` is how you say what
should happen to what it holds.

**Empty** (no body): the project is removed only while it holds no
resources. A project that holds any is refused with 409
`project_not_empty`, and the refusal enumerates what is inside:
`error.details.resource_count` is the total, and
`error.details.contents` names each kind with a count and up to five
names. Every project row also carries that total as
`resource_count`, so an application can find the projects it may
delete in one list call. Records of work never hold a project open
and are not counted.

**Detach** (`mode: detach`): only the grouping row is removed; every
resource in the project moves to the implicit Default project, where
it stays readable and is listed by `?project_id=default`. Refused
with 409 `project_has_scoped_credentials` while an API key, service
account, vault credential, webhook endpoint, member grant or pending
invite is scoped to the project, because detaching any of those
would silently widen it.

**Purge** (`mode: purge` with `confirm` equal to the project's
name): available only on an ARCHIVED project, because a teardown
needs a state you can sit in and reverse first; a live project is
refused with the coded `409 project_not_archived`. Archive the
project, confirm it is the one you mean, then purge. The project is
removed WITH its contents in one transaction: the resources it holds
and its scoped webhook endpoints and vault credentials are deleted,
API keys and service accounts pinned to the project are revoked, and
member grants and pending-invite scopes on the project are cleared.
Resources with a lifecycle and a delete of their own, such as
stores, hosted APIs and files, are not removed: they move to the
Default project, and because they do hold a project open, an
unqualified delete refuses while any of them is in the project.
Refused with 409 while a resource that must be released first is
still attached (the refusal names it), while a member's only project
grant is this one, or while a live invite carries only this project
(clearing either would widen that person to the whole workspace, the
invite one acceptance earlier).

**A purge is recoverable for 30 days.** The project disappears from
every list and read immediately, and its name is freed for reuse,
but the project and its resources are kept and permanently deleted
only once the window closes. `POST
/v1/projects/{project_id}/restore` brings the project and its
resources back inside that window; the credentials the purge revoked
and the grants it cleared stay that way.

The 409 carries the blockers under `error.details.blockers` (`kind`,
typed `id`, `name`, and the `blocks` modes each refuses), their
total under `error.details.blocker_count`, and, for existing
clients, the same rows under `error.details.credentials`. The lists
are capped at 50 rows; the counts are not, and the refusal is
decided on the count.
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

client.projects.delete(
    project_id="proj_01jqr8x9zg5k2m3n4p5q6r7s8t",
    mode="purge",
    confirm="Staging",
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

**project_id:** `str` — Project id (prefixed external id, `proj_...`).
    
</dd>
</dl>

<dl>
<dd>

**mode:** `typing.Optional[DeleteProjectRequestMode]` 

`detach` removes the grouping row only and moves every resource
to the Default project; `purge` removes the project with its
contents. Omitted, the delete removes only an empty project.
    
</dd>
</dl>

<dl>
<dd>

**confirm:** `typing.Optional[str]` 

Required for `purge`: the project's name, exactly as returned by
GET. A mismatch answers 400 `validation_failed` naming this field.
    
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

<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">update</a>(...) -> Project</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Edit a project in place - its name, its monthly spend limit, or its
capacity ceilings - keeping the same id so every grouped resource
follows the edit with no re-pointing. Names are unique per
workspace (case-insensitive). The limit fields require
`billing.manage`; a capacity ceiling above the workspace's own is
refused, since it could never apply.
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

client.projects.update(
    project_id="proj_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**project_id:** `str` — Project id (prefixed external id, `proj_...`).
    
</dd>
</dl>

<dl>
<dd>

**max_requests_per_minute:** `typing.Optional[int]` 

Sets the project's request-rate ceiling in requests per
minute; `null` removes it. Must be a positive integer at or
below the workspace's widest per-surface request rate over a
minute, otherwise the request is refused with
`400 validation_failed` naming the field and the ceiling.
Requires the `billing.manage` permission. Takes effect on the
next request from a credential pinned to the project.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 

New project name; unique per workspace (case-insensitive),
surrounding whitespace is trimmed.
    
</dd>
</dl>

<dl>
<dd>

**monthly_budget:** `typing.Optional[float]` 

Edits the project's MONTHLY spend limit in US dollars: omit to
leave it unchanged, send a positive value to set or change it, or
an explicit `0` to remove it. Amounts are whole cents written as a
plain decimal; a finer value, or exponent notation, is refused
rather than rounded. Requires the
`billing.manage`
permission (owners/admins), like the workspace budget — a
spend ceiling is a billing control, not a grouping edit. Once the
project's billed spend within the current calendar month (UTC)
reaches the limit, new billable work attributed to that project is
refused with the coded `402 project_spend_limit_exceeded` until
the month resets or the limit is raised.
    
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

<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">archive</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Archive a project. From then on nothing new starts or bills inside
it: requests on a credential pinned to the project, and every new
piece of work attributed to it, are refused with the coded `409
project_archived`. Work already in flight is left to finish.
Everything in the project stays readable and its configuration stays
editable, and the project still answers by id.

Idempotent: archiving an archived project is a no-op. Reverse it
with the unarchive operation.
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

client.projects.archive(
    project_id="proj_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**project_id:** `str` — Project id (prefixed external id, `proj_...`).
    
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

<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">unarchive</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lift a project's archive so work and spend resume inside it.
Idempotent: unarchiving a live project is a no-op.
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

client.projects.unarchive(
    project_id="proj_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**project_id:** `str` — Project id (prefixed external id, `proj_...`).
    
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

<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">restore</a>(...) -> ProjectRestore</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Walk back a purge. A purged project is recoverable for 30 days: its
row and its contents are kept, hidden from every list and read, and
permanently deleted only once the window expires.

**What comes back:** the project and exactly the resources the purge
removed. A resource you had deleted yourself before the purge stays
deleted.

**What does NOT come back, on purpose:** every credential the purge
revoked stays revoked, and every grant it cleared stays cleared. API
keys and service accounts pinned to the project are not re-issued,
vault credentials and webhook endpoints scoped to it are not
undeleted, and member grants and pending-invite scopes are not
restored. Bringing a credential or a grant back would re-grant
access somebody deliberately ended, so the restore reports them
under `still_revoked` instead. Re-create the credentials and
re-grant the members the project still needs.

The project returns ARCHIVED, the state it was purged from, so
nothing dispatches or bills inside it until you unarchive it.

Refused with `409 project_not_purged` when the project was never
purged, `409 project_restore_window_expired` once the 30 days have
passed, and `409 project_name_taken` when another project has taken
this one's name since the purge (a purge frees the name immediately
- rename the project holding it, then restore).
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

client.projects.restore(
    project_id="proj_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**project_id:** `str` — Project id (prefixed external id, `proj_...`).
    
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

<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">audit</a>(...) -> ProjectAuditResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Who changed this project's access or its lifecycle state, and when.
Newest first. Covers the last 90 days; paginate by passing `cursor`
from the previous response.

Each entry names the SUBJECT (whose access changed) and the ACTOR (who
changed it), with the role the actor held at the time. When a change
was made by Speechify support acting on the workspace's behalf, the
entry also carries that admin's email, so a support-initiated change
never reads as one a colleague made.

Requires `members.manage_project_scope` (owner or admin): who widened
a member's access is a stronger fact than who currently holds it.
Returns 404 for missing or foreign-workspace projects.
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

client.projects.audit(
    project_id="proj_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**project_id:** `str` — Project id (prefixed external id, `proj_...`).
    
</dd>
</dl>

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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">list_members</a>(...) -> ProjectMembersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List the workspace members granted access to this project, oldest
grant first. Paginate by passing `cursor` from the previous response.

A member with no grants anywhere is workspace-wide and does not appear
here: this lists people who have been narrowed to specific projects,
not everyone who can reach this one.
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

client.projects.list_members(
    project_id="proj_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**project_id:** `str` — Project ID.
    
</dd>
</dl>

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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">grant_member</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Grant a workspace member access to this project. Once a member holds
any grant, they see and touch only the projects they have been granted.

Requires `members.manage_project_scope` (owner or admin). An owner or
billing admin cannot be scoped: both already hold workspace-wide access
that a project scope would contradict without restricting anything.
Idempotent: granting a project the member already holds is a no-op.
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

client.projects.grant_member(
    project_id="proj_01jqr8x9zg5k2m3n4p5q6r7s8t",
    user_id="user_kb3fim3yjnyto3kxli4g4ysdmyzgiuttjrudswlkgbawk",
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

**project_id:** `str` — Project ID.
    
</dd>
</dl>

<dl>
<dd>

**user_id:** `str` — The prefixed user id of the workspace member to grant.
    
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

<details><summary><code>client.projects.<a href="src/speechify/projects/client.py">revoke_member</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Remove a member's access to this project.

A member who loses their last grant is not locked out - they return
to workspace-wide access, because holding no grants is the unrestricted
state. To restrict someone, grant them the projects they should keep
rather than revoking everything. Requires `members.manage_project_scope`.
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

client.projects.revoke_member(
    project_id="proj_01jqr8x9zg5k2m3n4p5q6r7s8t",
    user_id="user_kb3fim3yjnyto3kxli4g4ysdmyzgiuttjrudswlkgbawk",
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

**project_id:** `str` — Project ID.
    
</dd>
</dl>

<dl>
<dd>

**user_id:** `str` — The member's prefixed user id, as returned by the members list.
    
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

## workspaces
<details><summary><code>client.workspaces.<a href="src/speechify/workspaces/client.py">get_entitlements</a>() -> EntitlementsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

The per-tier entitlements catalog plus the caller's RESOLVED
entitlements for the current workspace (tier defaults composed with
any per-tenant override). Readable with an API key as well as a
console session: it is how an integration learns what it may use
before a feature endpoint answers `402`. Branch on
`current.voice_cloning` and `current.hosted_apis_access`, and size
traffic from
`current.tts_requests_per_second` and `current.tts_concurrency`. The
console renders quota affordances and upgrade-card limits from the
same single server-authoritative source instead of a hardcoded
mirror.
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

client.workspaces.get_entitlements()

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

## Audio Watermark
<details><summary><code>client.audio.watermark.<a href="src/speechify/audio/watermark/client.py">detect</a>(...) -> WatermarkDetectionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Check whether a clip carries the watermark Speechify seals into audio it
generates. Upload the audio as `audio`; nothing about it is stored, and
no voice is read or written.

Read the answer carefully in one direction. A `watermarked: true` is
positive evidence that the audio came from Speechify synthesis. A
`watermarked: false` is NOT proof that it did not: only models
redeployed since the watermark shipped mark their output, the detector
needs at least three seconds of clear speech to judge, and re-encoding
or changing the speed of a clip degrades the mark. Treat a negative as
the absence of evidence rather than as evidence of absence.

Checks are rate-limited well below the synthesis budget: this is a
forensic question, not a data-plane call.
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

client.audio.watermark.detect(
    audio="example_audio",
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

**audio:** `core.File` 

The clip to check, at most 25MB. Give the detector at least
three seconds of clear speech; below that its confidence is
not worth acting on, and below half a second it always
reports zero.
    
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

<details><summary><code>client.audio.watermark.<a href="src/speechify/audio/watermark/client.py">verify</a>(...) -> WatermarkVerificationResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

The public AI detection tool. Ask whether a clip carries the watermark
Speechify seals into audio it generates, with no account, no API key and
no credential of any kind.

`verify` answers; `detect` measures. This route returns a bare yes or no,
the way verifying a signature does. Its sibling
`POST /v1/audio/watermark/detect` takes an API key and returns the
detector's confidence alongside the verdict.

This is the programmatic half of the tool published at
<https://speechify.ai/detect>, and it exists so the tool can be invoked
without visiting our website, as California's AI Transparency Act
(BPC 22757.2) requires. Nothing about the clip is stored, and nothing
identifying about you is collected or retained.

The answer is a bare verdict. `watermarked: true` is positive evidence
that the audio came from Speechify synthesis. `watermarked: false` is
NOT proof that it did not: only models redeployed since the watermark
shipped mark their output, the detector needs at least three seconds of
clear speech to judge, and re-encoding or changing the speed of a clip
degrades the mark. Treat a negative as the absence of evidence rather
than as evidence of absence.

Because the tool takes no credential, it is rate-limited per client
address and shares a platform-wide budget: expect a 429 under sustained
automated use, and retry after the interval the response advertises.
Use `POST /v1/audio/watermark/detect` with an API key for the detector's
confidence score and a per-workspace allowance of its own.
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

client.audio.watermark.verify(
    audio="example_audio",
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

**audio:** `core.File` 

The clip to check, at most 25MB. Give the detector at least
three seconds of clear speech; below that its answer is not
worth acting on.
    
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

Like `POST /v1/voices`, a challenge requested from a jurisdiction where voice cloning is not available returns 403 `voice_cloning_unavailable_in_region` and issues no phrase. The location is read from the IP address that sends the request, which is your server's when your backend calls the API.
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

## Webhooks Endpoints
<details><summary><code>client.webhooks.endpoints.<a href="src/speechify/webhooks/endpoints/client.py">list</a>(...) -> ListWebhookEndpointsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

The caller's workspace's registered webhook endpoints. Cursor-paginated:
omit `cursor` for the first page; walk pages while `has_more` is true
(default page size 50, max 200). The signing `secret` is never returned
here — it is shown only when an endpoint is created or its secret is
rotated. Filter by delivery scope with `project_id`.
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

client.webhooks.endpoints.list(
    project_id="proj_01arz3ndektsv4rrffq69g5fav",
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

**project_id:** `typing.Optional[str]` 

Filter endpoints by project scope: omit for everything the caller
may see, pass the literal `shared` for workspace-wide endpoints
only, or a `proj_...` id for endpoints scoped to that project.
Endpoints have no Default project - a null `project_id` means
workspace-wide, so the literal here is `shared`, never `default`.
Returns 404 project_not_found for a malformed id and for any
project outside your reach: a project-pinned API key or
service-account key reaches only its pinned project, and a member
holding project grants reaches only the granted projects. That 404
is the same in every case and does not reveal whether such a
project exists - outside your reach a project is answered as
nonexistent, never as forbidden. `shared` is always inside your
reach. Inside it, a well-formed id that matches nothing yields an
empty page.
    
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

<details><summary><code>client.webhooks.endpoints.<a href="src/speechify/webhooks/endpoints/client.py">create</a>(...) -> WebhookEndpoint</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Register a webhook endpoint. Speechify mints an HMAC signing secret
and returns it in the response `secret` field — exactly once. Store it
then; subsequent reads omit it (rotate it with the rotate-secret action
if lost). Select events via `enabled_events`: a list of catalog event
names or `["*"]` for every event. Optionally scope delivery to one
project with `project_id`; omit it for a workspace-wide endpoint that
receives every project's events. Limited to 50 endpoints per workspace.
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

client.webhooks.endpoints.create(
    url="https://example.com/speechify/webhooks",
    enabled_events=[
        "project.spend_budget.warning"
    ],
    description="Example description.",
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

**url:** `str` 

HTTPS destination for event deliveries. Must be a publicly
reachable host: loopback, private, link-local, and cloud-metadata
addresses (and reserved hostnames like `localhost`) are rejected.
    
</dd>
</dl>

<dl>
<dd>

**enabled_events:** `typing.List[str]` — Catalog event names to subscribe to, or `["*"]` for all events.
    
</dd>
</dl>

<dl>
<dd>

**project_id:** `typing.Optional[str]` 

Optionally scope the endpoint to one project (prefixed
`proj_...` id): a scoped endpoint receives only that project's
events. Omit (or null) for workspace-wide - it receives every
project's events. An unknown id returns 404 project_not_found.
A project-pinned API key creates into its own project and
cannot name the workspace-wide tier.
    
</dd>
</dl>

<dl>
<dd>

**include:** `typing.Optional[typing.List[str]]` 

Optional payload-shaping keys (see `WebhookEndpoint.include`).
Omit for the lean default.
    
</dd>
</dl>

<dl>
<dd>

**api_version:** `typing.Optional[datetime.date]` 

Optionally pin the endpoint's payload shape to a dated version
(`YYYY-MM-DD`, see `WebhookEndpoint.api_version`). Omit to use the
workspace's current version. An unknown version is rejected.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 
    
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

<details><summary><code>client.webhooks.endpoints.<a href="src/speechify/webhooks/endpoints/client.py">get</a>(...) -> WebhookEndpoint</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetch a webhook endpoint by id. The signing secret is never returned.
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

client.webhooks.endpoints.get(
    webhook_endpoint_id="whe_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**webhook_endpoint_id:** `str` — Webhook endpoint id (prefixed `whe_…`).
    
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

<details><summary><code>client.webhooks.endpoints.<a href="src/speechify/webhooks/endpoints/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a webhook endpoint. In-flight deliveries stop; returns 204 on success.
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

client.webhooks.endpoints.delete(
    webhook_endpoint_id="whe_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**webhook_endpoint_id:** `str` — Webhook endpoint id (prefixed `whe_…`).
    
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

<details><summary><code>client.webhooks.endpoints.<a href="src/speechify/webhooks/endpoints/client.py">update</a>(...) -> WebhookEndpoint</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Partial update; omitted fields are left unchanged. Set `disabled` to pause delivery without deleting the endpoint.
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

client.webhooks.endpoints.update(
    webhook_endpoint_id="whe_01jqr8x9zg5k2m3n4p5q6r7s8t",
    url="https://example.com/webhook",
    enabled_events=[
        "example"
    ],
    description="Example description.",
    disabled=False,
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

**webhook_endpoint_id:** `str` — Webhook endpoint id (prefixed `whe_…`).
    
</dd>
</dl>

<dl>
<dd>

**url:** `typing.Optional[str]` 

HTTPS destination for event deliveries. Must be a publicly
reachable host: loopback, private, link-local, and cloud-metadata
addresses (and reserved hostnames like `localhost`) are rejected.
    
</dd>
</dl>

<dl>
<dd>

**project_id:** `typing.Optional[str]` 

Re-scope the endpoint: a `proj_...` id narrows it to that
project's events, an explicit null makes it workspace-wide
(every project's events), omitted leaves it unchanged. The
signing secret and delivery history are untouched, so
re-scoping never requires redeploying your receiver. An
unknown id returns 404 project_not_found. A project-pinned API
key may only scope an endpoint to its own project.
    
</dd>
</dl>

<dl>
<dd>

**enabled_events:** `typing.Optional[typing.List[str]]` 
    
</dd>
</dl>

<dl>
<dd>

**include:** `typing.Optional[typing.List[str]]` 

Payload-shaping keys (see `WebhookEndpoint.include`). Send `[]` to
clear back to the lean default.
    
</dd>
</dl>

<dl>
<dd>

**api_version:** `typing.Optional[datetime.date]` 

Opt the endpoint into a different (typically newer) payload shape
(`YYYY-MM-DD`, see `WebhookEndpoint.api_version`). Omit to leave it
unchanged. An unknown version is rejected.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**disabled:** `typing.Optional[bool]` 
    
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

<details><summary><code>client.webhooks.endpoints.<a href="src/speechify/webhooks/endpoints/client.py">rotate_secret</a>(...) -> WebhookEndpoint</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Mint a new HMAC signing secret for the endpoint and return it in the
response `secret` field (shown exactly once). The previous secret stops
signing immediately, so accept both during your cutover window.
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

client.webhooks.endpoints.rotate_secret(
    webhook_endpoint_id="whe_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**webhook_endpoint_id:** `str` — Webhook endpoint id (prefixed `whe_…`).
    
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

<details><summary><code>client.webhooks.endpoints.<a href="src/speechify/webhooks/endpoints/client.py">list_deliveries</a>(...) -> ListWebhookEndpointDeliveriesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delivery attempts for one webhook endpoint, newest first. One row per
(endpoint, event, resource), updated in place across retries. Each row
includes the exact request payload and signed headers Speechify sent
(`request_body`, `request_headers`) and the response your server returned
(`last_status_code`, `last_response_body`, `last_response_headers`), so
you can verify the signature and debug failures. Cursor-paginated: omit
`cursor` for the first page; walk pages while `has_more` is true (default
page size 50, max 200).

An endpoint that was not a target of an event has no row for it: a
project-scoped endpoint records nothing for another project's events.
An empty list therefore means either nothing matched or nothing
happened. To tell them apart, check the project's own activity first:
activity there with no delivery here is a defect to report; none there
means there was nothing to deliver.
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

client.webhooks.endpoints.list_deliveries(
    webhook_endpoint_id="whe_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**webhook_endpoint_id:** `str` — Webhook endpoint id (prefixed `whe_…`).
    
</dd>
</dl>

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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

