import importlib
from typing import Any

import httpx
import pytest

import speechify.client as client_module
from speechify.core.api_error import ApiError


@pytest.fixture
def imported_without_key(monkeypatch):
    monkeypatch.delenv("SPEECHIFY_API_KEY", raising=False)
    importlib.reload(client_module)
    yield client_module
    # Avoid leaving reloaded import-time defaults behind for other test files.
    monkeypatch.undo()
    importlib.reload(client_module)


@pytest.mark.parametrize("mode", ["sync", "async"])
@pytest.mark.parametrize("scenario", ["late", "rotated", "removed", "explicit", "callable", "missing"])
async def test_token_is_resolved_when_each_client_is_created(imported_without_key, monkeypatch, mode, scenario):
    module = imported_without_key
    if scenario in {"rotated", "removed"}:
        monkeypatch.setenv("SPEECHIFY_API_KEY", "old-key")
        importlib.reload(module)
    if scenario in {"removed", "missing"}:
        monkeypatch.delenv("SPEECHIFY_API_KEY", raising=False)
    else:
        monkeypatch.setenv("SPEECHIFY_API_KEY", "current-key")

    seen = []

    def respond(request):
        seen.append(request.headers["Authorization"])
        return httpx.Response(200, json={"models": [], "dialogue_models": []})

    kwargs: dict[str, Any] = {}
    if scenario == "explicit":
        kwargs["token"] = "explicit-key"
    elif scenario == "callable":
        kwargs["token"] = lambda: "callable-key"

    transport = httpx.MockTransport(respond)
    if mode == "sync":
        with httpx.Client(transport=transport) as http_client:
            if scenario in {"removed", "missing"}:
                with pytest.raises(ApiError):
                    module.Speechify(httpx_client=http_client, **kwargs)
                assert not seen
                return
            client = module.Speechify(httpx_client=http_client, **kwargs)
            client.models.list()
    else:
        async with httpx.AsyncClient(transport=transport) as http_client:
            if scenario in {"removed", "missing"}:
                with pytest.raises(ApiError):
                    module.AsyncSpeechify(httpx_client=http_client, **kwargs)
                assert not seen
                return
            client = module.AsyncSpeechify(httpx_client=http_client, **kwargs)
            await client.models.list()

    expected = {"explicit": "explicit-key", "callable": "callable-key"}.get(scenario, "current-key")
    assert seen == [f"Bearer {expected}"]
