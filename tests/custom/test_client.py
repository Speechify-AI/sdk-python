# Hand-kept (listed in .fernignore). Generated tests always pass an explicit
# base URL, so nothing else exercises the client a user builds with defaults.
import typing

import httpx
import pytest

from speechify import AsyncSpeechify, ContentTooLargeError, Speechify, SpeechifyEnvironment
from speechify.types.speech_stream_event import SpeechStreamEvent_SpeechChunk, SpeechStreamEvent_SpeechDone

_RESPONSES: typing.Dict[str, typing.Dict[str, typing.Any]] = {
    "/v1/audio/speech": {
        "audio_data": "",
        "audio_format": "mp3",
        "billable_characters_count": 5,
        "speech_marks": {"chunks": [], "end": 5, "end_time": 0, "start": 0, "start_time": 0, "type": "sentence"},
    },
    "/v1/audio/models": {"models": [], "dialogue_models": []},
    "/v1/voices": {"voices": [], "has_more": False},
}

# Framed exactly as the API writes it: a named event, one data line, a blank line.
_SSE = (
    'event: speech.chunk\ndata: {"type":"speech.chunk","audio":"AAAA"}\n\n'
    'event: speech.done\ndata: {"type":"speech.done","billable_characters_count":5,"audio_duration_ms":120}\n\n'
)


def _transport(seen: typing.List[httpx.Request], status: int = 200) -> httpx.MockTransport:
    def respond(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if status != 200:
            return httpx.Response(status, json={"error": {"code": "payload_too_large", "message": "too large"}})
        if request.url.path == "/v1/audio/stream/with-timestamps":
            return httpx.Response(200, content=_SSE.encode(), headers={"Content-Type": "text/event-stream"})
        return httpx.Response(200, json=_RESPONSES[request.url.path])

    return httpx.MockTransport(respond)


def test_the_environment_names_its_urls_base_and_websocket() -> None:
    assert SpeechifyEnvironment.DEFAULT.base == "https://api.speechify.ai"
    assert SpeechifyEnvironment.DEFAULT.websocket == "wss://api.speechify.ai"


def test_speech_goes_to_api_speechify_ai() -> None:
    seen: typing.List[httpx.Request] = []
    client = Speechify(token="test-token", httpx_client=httpx.Client(transport=_transport(seen)))

    client.audio.speech(input="Hello", voice_id="geffen_32", model="simba-3.5")

    assert [str(request.url) for request in seen] == ["https://api.speechify.ai/v1/audio/speech"]
    assert seen[0].headers["Authorization"] == "Bearer test-token"


def test_every_resource_client_sends_the_same_version() -> None:
    seen: typing.List[httpx.Request] = []
    client = Speechify(token="test-token", httpx_client=httpx.Client(transport=_transport(seen)))

    client.audio.speech(input="Hello", voice_id="geffen_32")
    client.models.list()
    list(client.voices.list())

    versions = {request.headers.get("Speechify-Version") for request in seen}
    assert len(versions) == 1
    assert None not in versions


def test_a_with_timestamps_stream_yields_every_event_the_final_done_included() -> None:
    client = Speechify(token="test-token", httpx_client=httpx.Client(transport=_transport([])))

    events = list(client.audio.stream_with_timestamps(input="Hello", voice_id="geffen_32"))

    assert [type(event) for event in events] == [SpeechStreamEvent_SpeechChunk, SpeechStreamEvent_SpeechDone]
    done = events[1]
    assert isinstance(done, SpeechStreamEvent_SpeechDone) and done.billable_characters_count == 5


def test_an_oversized_body_raises_content_too_large() -> None:
    client = Speechify(token="test-token", httpx_client=httpx.Client(transport=_transport([], status=413)))

    with pytest.raises(ContentTooLargeError):
        client.audio.speech(input="Hello", voice_id="geffen_32")


async def test_async_speech_goes_to_api_speechify_ai() -> None:
    seen: typing.List[httpx.Request] = []
    client = AsyncSpeechify(token="test-token", httpx_client=httpx.AsyncClient(transport=_transport(seen)))

    await client.audio.speech(input="Hello", voice_id="geffen_32", model="simba-3.5")

    assert [str(request.url) for request in seen] == ["https://api.speechify.ai/v1/audio/speech"]


# A keyless client is legitimate: POST /v1/audio/watermark/verify takes no
# credentials. Authenticated calls then fail with the API's 401.
def test_a_client_without_a_key_sends_no_authorization(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SPEECHIFY_API_KEY", raising=False)
    seen: typing.List[httpx.Request] = []
    client = Speechify(token=None, httpx_client=httpx.Client(transport=_transport(seen)))

    client.models.list()

    assert "Authorization" not in seen[0].headers
