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

The legacy Simba 1.6 models `simba-english` and `simba-multilingual` are retired from API version `2026-09-21`: naming one returns 400 `model_retired`. Pinning your API version to a date before `2026-09-21` keeps them working until **2026-11-21**, when both are switched off for every API version. Migrate to `simba-3.2` (English) or `simba-3.0` before then; call GET /v1/audio/models to see the set your workspace can select today.
    
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
`simba-3.0` and `simba-3.2` both serve this route. The legacy
`simba-english` and `simba-multilingual` models never could: on a
workspace pinned before API version `2026-09-21` they return 400
`speech_marks_unsupported` here, and from that version on they return
400 `model_retired` on every synthesis route. Both are switched off
entirely on 2026-11-21.
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

The clone belongs to the workspace rather than the member who created it, and access follows the caller's workspace role and API-key scopes exactly as for any other voice: voices scopes to list it, audio scopes to synthesize with it, and the content-management permission plus a write scope on the key to delete it. Cloned voices are usable self-serve on `simba-3.0` (and, on a workspace pinned before API version `2026-09-21`, on the retired `simba-english` and `simba-multilingual` until they are switched off on 2026-11-21). `simba-3.2` also serves cloned voices.

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

## HostedApis
<details><summary><code>client.hosted_apis.<a href="src/speechify/hosted_apis/client.py">list</a>(...) -> ListHostedApIsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List the hosted APIs in the caller's workspace, most recently updated
first. A hosted API is the API you assemble: a slug that becomes
`https://<slug>.<hosted-api domain>`, the routes it answers, and the
consumer keys your own callers present.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.list(
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

Filter by workspace project: omit for every project you can reach,
pass the literal `default` for resources in the implicit Default
project only, or a `proj_...` id for that project's resources.
Returns 404 project_not_found for a malformed id and for any filter
outside your reach: a project-pinned API key or service-account key
reaches only its pinned project, and a member holding project grants
reaches only the granted projects, so neither can name `default`.
That 404 is the same in every case and does not reveal whether such
a project exists - outside your reach a project is answered as
nonexistent, never as forbidden. Inside it, a well-formed id that
matches no project yields an empty page.
    
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

<details><summary><code>client.hosted_apis.<a href="src/speechify/hosted_apis/client.py">create</a>(...) -> HostedApi</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a hosted API. The slug is a DNS label, globally unique on the
shared domain (409 `hosted_api_slug_taken`) and immutable afterwards.
`auth_mode` names the audience, narrowest first: `owner`, `workspace`
(the platform's own credentials), `user_token` (a JWT your backend
signs per user), `consumer_key` (a `ck_` key you mint) or `public`
(anyone, reads only). A workspace can refuse `public` as policy (403
`hosted_api_public_refused`). Reads, runs and writes are each bounded
per UTC day (`daily_read_cap`, `daily_run_cap`, `daily_write_cap`),
and an API holds only a share of a server's requests open at once, so
a slow upstream behind one API cannot take the capacity others need:
past it, a request answers 429 `hosted_api_busy` with `Retry-After`.

`mcp_enabled: true` also serves the API's routes as an MCP server at
`POST <base_url>/mcp`, so an MCP client (Claude Code, Cursor) attaches
to one address and gets them as tools, under the same audience, keys
and caps. It is refused with `auth_mode: public`. On that face the
API's `name` is the server's title and its `description` is the
instructions the client's model reads, so describe what the tools are
for.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.create(
    idempotency_key="a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
    slug="acme-news",
    name="Acme News",
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

**slug:** `str` — 3-40 lowercase letters, digits or hyphens; a DNS label, unique on the shared domain; immutable.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
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

**description:** `typing.Optional[str]` — What the API is for; also the instructions an MCP client hands its model when `mcp_enabled` is on.
    
</dd>
</dl>

<dl>
<dd>

**auth_mode:** `typing.Optional[CreateHostedApiRequestAuthMode]` — consumer_key when omitted. `public` is refused with 403 `hosted_api_public_refused` where the workspace's policy does not allow internet-facing APIs.
    
</dd>
</dl>

<dl>
<dd>

**cors_origins:** `typing.Optional[typing.List[str]]` 
    
</dd>
</dl>

<dl>
<dd>

**daily_run_cap:** `typing.Optional[int]` — Runs the API may start per UTC day through its run routes; 1000 when omitted.
    
</dd>
</dl>

<dl>
<dd>

**daily_read_cap:** `typing.Optional[int]` — Reads the API's store, file, run_latest and tool routes may serve per UTC day; 100000 when omitted.
    
</dd>
</dl>

<dl>
<dd>

**daily_write_cap:** `typing.Optional[int]` — Documents the API's write routes may land per UTC day; 10000 when omitted.
    
</dd>
</dl>

<dl>
<dd>

**mcp_enabled:** `typing.Optional[bool]` 

Serve the routes as an MCP server at `POST <base_url>/mcp` too;
false when omitted. Refused with `auth_mode: public` (400
`validation_failed` naming `mcp_enabled`).
    
</dd>
</dl>

<dl>
<dd>

**project_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**user_token_jwks_url:** `typing.Optional[str]` — Register the key set end-user tokens are verified against (an `https` URL on a public host).
    
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

<details><summary><code>client.hosted_apis.<a href="src/speechify/hosted_apis/client.py">get</a>(...) -> HostedApi</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve one hosted API.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.get(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
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

<details><summary><code>client.hosted_apis.<a href="src/speechify/hosted_apis/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a hosted API; its host stops answering at once.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.delete(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
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

<details><summary><code>client.hosted_apis.<a href="src/speechify/hosted_apis/client.py">update</a>(...) -> HostedApi</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update a hosted API (merge-patch). Switching to `public` is refused
while a `run` or `store_write` route exists: an anonymous caller must
not start runs that spend the workspace's budget or write to a store,
and it is refused outright where the workspace's policy does not allow
internet-facing APIs (403 `hosted_api_public_refused`). Switching to a
mode that names no caller (`consumer_key`, `public`) is refused while
a route binds `{{user.*}}`: only `user_token`, `workspace` and `owner`
supply a person. Switching to `public` is also refused while a `tool`
route exists (a vendor call spends the workspace's vendor budget) and
while `mcp_enabled` is on, and switching the MCP face on is refused on
a `public` API (400 `validation_failed` naming `mcp_enabled`).
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.update(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — What the API is for; also the instructions an MCP client hands its model when `mcp_enabled` is on.
    
</dd>
</dl>

<dl>
<dd>

**auth_mode:** `typing.Optional[UpdateHostedApiRequestAuthMode]` 
    
</dd>
</dl>

<dl>
<dd>

**cors_origins:** `typing.Optional[typing.List[str]]` 
    
</dd>
</dl>

<dl>
<dd>

**enabled:** `typing.Optional[bool]` — A paused API answers 503 to every consumer request.
    
</dd>
</dl>

<dl>
<dd>

**daily_run_cap:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**daily_read_cap:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**daily_write_cap:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**mcp_enabled:** `typing.Optional[bool]` 

Switch the MCP face at `POST <base_url>/mcp` on or off. Refused with
400 `validation_failed` naming `mcp_enabled` when the API is, or is
being made, `public`. Allow up to 15 seconds for the switch, like
any route change, to reach every server.
    
</dd>
</dl>

<dl>
<dd>

**user_token_jwks_url:** `typing.Optional[str]` — Replace the registered key set; an empty string removes it, after which the signing secret verifies tokens again.
    
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

<details><summary><code>client.hosted_apis.<a href="src/speechify/hosted_apis/client.py">get_open_api</a>(...) -> typing.Dict[str, typing.Any]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

The OpenAPI 3.1 document describing the hosted API's routes - the same
document the API serves to its consumers at `/openapi.json`. A `tool`
route's request body is the operation's own argument schema. When
`mcp_enabled` is on, the document carries an `x-speechify-mcp` object
(`url`, `transport: streamable-http`, `description`) naming where an
MCP client attaches; the face speaks JSON-RPC, so it is an extension
rather than a path.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.get_open_api(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
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

<details><summary><code>client.hosted_apis.<a href="src/speechify/hosted_apis/client.py">get_usage</a>(...) -> HostedApiUsage</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Today's reads, runs and writes against the API's daily caps, with each
route's share of the reads and writes. A read is a request a store,
file or run_latest route answered from storage; a response served from
the cache is not one. A write is a document a `store_write` route
landed; a replayed Idempotency-Key is not one. `counters_available` is false where nothing counts (no Redis), so
a zero is never mistaken for a quiet day.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.get_usage(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
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

<details><summary><code>client.hosted_apis.<a href="src/speechify/hosted_apis/client.py">get_analytics</a>(...) -> RequestAnalyticsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Requests the API served over time: volume split by status, success
rate, and p50/p95/p99 latency per time bucket, plus one `top_paths`
row per route, busiest first, naming the route by `route_id`. Every
request its host answered counts, including refusals such as a
missing key (401) or an exhausted rate limit (429); `top_paths` counts
only the requests that matched a route, including a route an MCP
client called by tool name.
The window defaults to the last 7 days and is capped at 30.

History starts at `history_starts_at`, the first request in the last
30 days attributed to this API: requests before it cannot be
attributed, so a bucket before it is missing data, not a quiet period.
When `history_starts_at` is absent, no request to this API has been
attributed in the last 30 days, and no bucket is known to be complete.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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
import datetime

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.hosted_apis.get_analytics(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
    start=datetime.datetime.fromisoformat("2026-06-23T00:00:00+00:00"),
    end=datetime.datetime.fromisoformat("2026-06-30T00:00:00+00:00"),
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
</dd>
</dl>

<dl>
<dd>

**start:** `typing.Optional[datetime.datetime]` — Inclusive start of the window (RFC-3339). Defaults to 7 days ago; the window is capped at 30 days.
    
</dd>
</dl>

<dl>
<dd>

**end:** `typing.Optional[datetime.datetime]` — Exclusive end of the window (RFC-3339). Defaults to now.
    
</dd>
</dl>

<dl>
<dd>

**granularity:** `typing.Optional[GetAnalyticsHostedApisRequestGranularity]` — Time-bucket size for the analytics series.
    
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

<details><summary><code>client.hosted_apis.<a href="src/speechify/hosted_apis/client.py">rotate_user_token_secret</a>(...) -> HostedApiUserTokenSecret</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Mint the signing secret end-user tokens are verified against, replacing
any previous one at once: every token signed with the old secret stops
verifying. The plaintext is in this response and nowhere else; later
reads show `user_token_secret_hint`. Your backend signs a JWT with it
(HS256) carrying `sub` (the user, at most 256 characters) and `exp`
(within 24 hours), and the consumer presents it as
`Authorization: Bearer <token>`. Register `user_token_jwks_url`
instead to verify with your own keys.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.rotate_user_token_secret(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
    idempotency_key="a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
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

## HostedApis Routes
<details><summary><code>client.hosted_apis.routes.<a href="src/speechify/hosted_apis/routes/client.py">list_routes</a>(...) -> ListHostedApiRoutesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List a hosted API's routes in creation order.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.routes.list_routes(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
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

<details><summary><code>client.hosted_apis.routes.<a href="src/speechify/hosted_apis/routes/client.py">create_route</a>(...) -> HostedApiRoute</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add a route: a method + path answered by a resolver. `store_query`,
`store_document` and `store_aggregate` serve a store; `store_write`
lands the POST body as a document (`write_mode` create / replace /
merge; POST only, never on a public API, counted against
`daily_write_cap`, deduplicated on `Idempotency-Key`); `run_latest`
serves the newest structured output of a schedule trigger's runs;
`run` starts a run through a webhook trigger per request (POST only,
never on a public API) and waits up to `wait_seconds` before answering
202 with a handle to poll at `/_runs/{run_id}`; `file` serves one
published file, or a whole published tree when the path ends in `*`
(`/app/*` with `file_root` and `file_index`); `tool` calls one read
operation of an `openapi` tool definition, or one tool of an `mcp`
tool definition's server, in the API's project whose `approval` is
null or `auto` (POST only, never on a public API, counted against
`daily_read_cap`): the consumer's JSON body is the arguments and the
connector's answer, after the tool's response mapping, is the
response. An `mcp` route pins the tool's input schema as
`resolver.input_schema` when it is written.
Where-clause values and
the document id may be `{{query.x}}`, `{{path.x}}` or `{{body.x}}`
templates bound from the consumer's request, or `{{user.x}}` claims of
the verified caller on a `user_token`, `workspace` or `owner` API; a
clause whose template is absent is skipped. On those three modes a
written document is stamped `user_identity` as the caller and only
they can replace or merge it. Two bindings are refused at write time:
`{{user.*}}` on an API that names no caller, and a clause on
`user_identity` bound from a request template, which would let any
caller read any user's rows.

On an API with `mcp_enabled`, every enabled route except a `file`
route is also an MCP tool. The tool's name comes from the route's
`name`: every run of characters outside letters, digits, `_` and `-`
becomes `_`, leading and trailing `_` are dropped, and the result is
cut to 64 characters. A route with no name is listed under a name
built from its method and path (`post_issues_open`), and a name two
routes would share takes `_2`, `_3` in route order, so read the names
from the face's `tools/list` rather than deriving them. The route's
`description` is what the client's model reads to choose the tool,
falling back to the operation's summary on a `tool` route. Name and
describe a route for that reader.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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
from speechify import Speechify, HostedApiResolver, HostedApiResolverOrderBy
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    token="<token>",
    environment=SpeechifyEnvironment.DEFAULT,
)

client.hosted_apis.routes.create_route(
    api_id="api_01kc4q3r9s6t8v0w2x4y6z8a0b",
    method="GET",
    path="/leads",
    name="list_leads",
    description="List leads, highest value first.",
    resolver=HostedApiResolver(
        type="store_query",
        store_id="store_01kc4q5t1v3w5x7y9z1a3b5c7d",
        collection="leads",
        order_by=HostedApiResolverOrderBy(
            field="value",
            direction="desc",
        ),
    ),
    cache_ttl_seconds=30,
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
</dd>
</dl>

<dl>
<dd>

**method:** `CreateHostedApiRouteRequestMethod` 
    
</dd>
</dl>

<dl>
<dd>

**path:** `str` — Lowercase segments of letters, digits, `. _ -` or a `{param}`; `/openapi.json`, `/_runs` and `/mcp` are reserved.
    
</dd>
</dl>

<dl>
<dd>

**resolver:** `HostedApiResolver` 
    
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

**name:** `typing.Optional[str]` 

The route's name, 1-128 letters, digits, spaces, `.`, `_` or `-`.
On an API with `mcp_enabled` the MCP tool's name comes from it:
each run of other characters (a space included) becomes `_`,
leading and trailing `_` are dropped, and the result is cut to 64
characters. A route with no name is listed under a name built from
its method and path, and a name two routes would share takes `_2`,
`_3` in route order; the face's `tools/list` is the authority. Pick
a verb-first name a model can choose by.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 

What the route does. On an API with `mcp_enabled` it is the MCP
tool description a client's model reads to choose the tool, so say
what it returns and when to call it; a `tool` route with none falls
back to the operation's summary.
    
</dd>
</dl>

<dl>
<dd>

**response_schema:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**cache_ttl_seconds:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**enabled:** `typing.Optional[bool]` — Enabled when omitted.
    
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

<details><summary><code>client.hosted_apis.routes.<a href="src/speechify/hosted_apis/routes/client.py">mount_routes</a>(...) -> HostedApiMount</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Publish a connector's operations onto the API in one call: one `tool`
route per operation of an `openapi` tool definition, or per tool its
`mcp` server lists, named `<name_prefix>__<operation>` at
`<path_prefix>/<operation>`, so two connectors' tools stay apart on
the MCP face and inside its 64-character tool names.

Send `dry_run: true` first. The answer lists every operation with
its effective `action_class` and `approval`, whether a route can serve
it, and the `action` a mount takes: `create`, `update` (an MCP tool
whose input schema changed since its route was written; `changes`
names what), `unchanged`, `skip` (with the `reason`: not selected, not
a read, not auto-approved, a name or path already taken, or the route
cap) or `stale` (a route whose operation the connector no longer
offers, or can no longer serve; it is reported and never deleted,
since a consumer may still call it). The same call without `dry_run`
writes every create and update in one transaction and returns the
written `route` on each.

Every answer carries a `plan_digest`. Send the preview's digest with
the apply: the apply plans again inside its transaction and writes
only when that plan still has the digest, so a tool the server changed
or a route edited after you reviewed is never written unseen. When it
differs the apply writes nothing and answers 409 `mount_plan_changed`
with the current plan, as a dry run answers it, in
`error.details.plan`; review that and apply again with its digest,
under a new `Idempotency-Key` if you sent one, since a key replays its
first answer, this 409 included. The digest covers every operation the
connector offers and every route the API holds for it whatever
`operations` selects, so a preview of everything and an apply of a
selection share one. An apply without it writes whatever the mount
plans at that moment.

Mounting again is the refresh. Every route the API holds for the
connector is compared with what it offers now, whatever its name,
path or the selection, so an upstream change is seen as a diff before
anyone's client sees it. `operations` selects what to create; omit it
to create a route for every operation a route can serve. A route an
owner renamed or moved keeps its name and path on refresh.

The route write's rules apply to every operation: the connector must
be in the API's project (409 `cross_project_reference`), an MCP server
must be reachable with its credential to be listed (400
`validation_failed` on `tool_id` with the server's reason), and a
public API mounts nothing. An API holds at most 200 routes; a mount
that would pass the cap skips what does not fit. Without a
`plan_digest`, a route changed while the mount was being planned
answers 409 `api_route_conflict`; mount again.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.routes.mount_routes(
    api_id="api_01kc4q3r9s6t8v0w2x4y6z8a0b",
    tool_id="tool_01kc4n9s3v7w0y4a6c8e2g4j6m",
    name_prefix="linear",
    dry_run=True,
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
</dd>
</dl>

<dl>
<dd>

**tool_id:** `str` — The `openapi` or `mcp` tool definition to mount, in the API's project.
    
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

**operations:** `typing.Optional[typing.List[str]]` 

The operations to create routes for: openapi operation ids or the
MCP server's tool names. Omit to create a route for every operation
a route can serve. Naming one the connector does not offer is 400
`validation_failed` on `operations[i]`. Existing routes are compared
whatever the selection.
    
</dd>
</dl>

<dl>
<dd>

**name_prefix:** `typing.Optional[str]` — Prefix of each created route's name, `<name_prefix>__<operation>`. Defaults to the tool's name with other characters as `_`.
    
</dd>
</dl>

<dl>
<dd>

**path_prefix:** `typing.Optional[str]` — Path each created route sits under, `<path_prefix>/<operation>`; lowercase segments of letters, digits, `.`, `_` or `-`, with no `{param}` or `*`, and not under `/mcp`, `/openapi.json` or `/_runs`. Defaults to `/<name_prefix>` in lowercase.
    
</dd>
</dl>

<dl>
<dd>

**dry_run:** `typing.Optional[bool]` — Answer what the mount would do and write nothing.
    
</dd>
</dl>

<dl>
<dd>

**include_writes:** `typing.Optional[bool]` 

Create routes for operations that are not reads too, each with
`allow_write: true`. Only an API whose `auth_mode` names a person
takes them; the operation's `approval` must still be `auto`.
Without it a write is a `skip` that says so.
    
</dd>
</dl>

<dl>
<dd>

**plan_digest:** `typing.Optional[str]` 

The `plan_digest` of the preview you reviewed. The apply writes
only while the plan it computes inside its transaction still has
this digest, and otherwise writes nothing and answers 409
`mount_plan_changed` with the current plan. Omit it to apply what
the mount plans now. Refused with `dry_run`.
    
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

<details><summary><code>client.hosted_apis.routes.<a href="src/speechify/hosted_apis/routes/client.py">get_route</a>(...) -> HostedApiRoute</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve one route.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.routes.get_route(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
    route_id="route_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
</dd>
</dl>

<dl>
<dd>

**route_id:** `str` — Route id (prefixed external id, `route_...`).
    
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

<details><summary><code>client.hosted_apis.routes.<a href="src/speechify/hosted_apis/routes/client.py">delete_route</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a route.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.routes.delete_route(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
    route_id="route_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
</dd>
</dl>

<dl>
<dd>

**route_id:** `str` — Route id (prefixed external id, `route_...`).
    
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

<details><summary><code>client.hosted_apis.routes.<a href="src/speechify/hosted_apis/routes/client.py">update_route</a>(...) -> HostedApiRoute</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update a route (merge-patch); a changed method or resolver is re-validated.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.routes.update_route(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
    route_id="route_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
</dd>
</dl>

<dl>
<dd>

**route_id:** `str` — Route id (prefixed external id, `route_...`).
    
</dd>
</dl>

<dl>
<dd>

**method:** `typing.Optional[UpdateHostedApiRouteRequestMethod]` 
    
</dd>
</dl>

<dl>
<dd>

**path:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 

The route's name, 1-128 letters, digits, spaces, `.`, `_` or `-`.
On an API with `mcp_enabled` the MCP tool's name comes from it:
each run of other characters (a space included) becomes `_`,
leading and trailing `_` are dropped, and the result is cut to 64
characters. A route with no name is listed under a name built from
its method and path, and a name two routes would share takes `_2`,
`_3` in route order; the face's `tools/list` is the authority. Pick
a verb-first name a model can choose by.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 

What the route does. On an API with `mcp_enabled` it is the MCP
tool description a client's model reads to choose the tool, so say
what it returns and when to call it; a `tool` route with none falls
back to the operation's summary.
    
</dd>
</dl>

<dl>
<dd>

**resolver:** `typing.Optional[HostedApiResolver]` 
    
</dd>
</dl>

<dl>
<dd>

**response_schema:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**cache_ttl_seconds:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**enabled:** `typing.Optional[bool]` 
    
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

## HostedApis Keys
<details><summary><code>client.hosted_apis.keys.<a href="src/speechify/hosted_apis/keys/client.py">list_keys</a>(...) -> ListHostedApiKeysResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List a hosted API's consumer keys, newest first, revoked ones included.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.keys.list_keys(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
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

<details><summary><code>client.hosted_apis.keys.<a href="src/speechify/hosted_apis/keys/client.py">create_key</a>(...) -> HostedApiKey</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Mint a consumer key (`ck_...`) for the API's own callers. The plaintext
`secret` is present in this response only; every later read shows the
masked `key_hint`.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.keys.create_key(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
    idempotency_key="a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
    name="name",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
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

**rate_per_minute:** `typing.Optional[int]` — Requests per minute; 60 when omitted, 0 for unlimited.
    
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

<details><summary><code>client.hosted_apis.keys.<a href="src/speechify/hosted_apis/keys/client.py">revoke_key</a>(...) -> HostedApiKey</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Revoke a consumer key; idempotent. Requests carrying it are refused from now on.
Dark launch: requires the `hosted_apis_access` entitlement (402 `hosted_apis_not_in_plan` otherwise).
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

client.hosted_apis.keys.revoke_key(
    api_id="api_01jqr8x9zg5k2m3n4p5q6r7s8t",
    consumer_key_id="ckey_01jqr8x9zg5k2m3n4p5q6r7s8t",
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

**api_id:** `str` — Hosted API id (prefixed external id, `api_...`).
    
</dd>
</dl>

<dl>
<dd>

**consumer_key_id:** `str` — Consumer key id (prefixed external id, `ckey_...`).
    
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

