# Speechify Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2FSpeechify-AI%2Fsdk-python)
[![pypi](https://img.shields.io/pypi/v/speechify-api)](https://pypi.python.org/pypi/speechify-api)

The Speechify Python library provides convenient access to the Speechify APIs from Python.

## Table of Contents

- [Documentation](#documentation)
- [Installation](#installation)
- [Reference](#reference)
- [Usage](#usage)
- [Environments](#environments)
- [Async Client](#async-client)
- [Exception Handling](#exception-handling)
- [Streaming](#streaming)
- [Pagination](#pagination)
- [Advanced](#advanced)
  - [Access Raw Response Data](#access-raw-response-data)
  - [Retries](#retries)
  - [Timeouts](#timeouts)
  - [Custom Client](#custom-client)
- [Contributing](#contributing)

## Documentation

API reference documentation is available [here](https://docs.speechify.ai/api-reference).

## Installation

```sh
pip install speechify-api
```

## Reference

A full reference for this library is available [here](https://github.com/Speechify-AI/sdk-python/blob/HEAD/./reference.md).

## Usage

Instantiate and use the client with the following:

```python
from speechify import Speechify

client = Speechify(
    token="<token>",
)

client.audio.speech(
    audio_format="mp3",
    input="Hello! This is the Speechify text-to-speech API.",
    model="simba-3.2",
    voice_id="geffen_32",
)
```

## Environments

This SDK allows you to configure different environments for API requests.

```python
from speechify import Speechify
from speechify.environment import SpeechifyEnvironment

client = Speechify(
    environment=SpeechifyEnvironment.DEFAULT,
)
```

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API. Note that if you are constructing an Async httpx client class to pass into this client, use `httpx.AsyncClient()` instead of `httpx.Client()` (e.g. for the `httpx_client` parameter of this client).

```python
import asyncio

from speechify import AsyncSpeechify

client = AsyncSpeechify(
    token="<token>",
)


async def main() -> None:
    await client.audio.speech(
        audio_format="mp3",
        input="Hello! This is the Speechify text-to-speech API.",
        model="simba-3.2",
        voice_id="geffen_32",
    )


asyncio.run(main())
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```python
from speechify.core.api_error import ApiError

try:
    client.audio.speech(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

## Streaming

The SDK supports streaming responses, as well, the response will be a generator that you can loop over.

```python
from speechify import Speechify

client = Speechify(
    token="<token>",
)

client.audio.stream_with_timestamps(
    input="Streaming long-form audio with the Speechify API.",
    model="simba-3.2",
    voice_id="geffen_32",
)
```

## Pagination

Paginated requests will return a `SyncPager` or `AsyncPager`, which can be used as generators for the underlying object.

```python
from speechify import Speechify

client = Speechify(
    token="<token>",
)

client.voices.list(
    locale="en",
    model="simba-3.2",
)
```

```python
# You can also iterate through pages and access the typed response per page
pager = client.voices.list(...)
for page in pager.iter_pages():
    print(page.response)  # access the typed response for each page
    for item in page:
        print(item)
```

## Advanced

### Access Raw Response Data

The SDK provides access to raw response data, including headers, through the `.with_raw_response` property.
The `.with_raw_response` property returns a "raw" client that can be used to access the `.headers` and `.data` attributes.

```python
from speechify import Speechify

client = Speechify(...)
response = client.audio.with_raw_response.speech(...)
print(response.headers)  # access the response headers
print(response.status_code)  # access the response status code
print(response.data)  # access the underlying object
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retryable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

Which status codes are retried depends on the `retryStatusCodes` generator configuration:

**`legacy`** (current default): retries on
- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [409](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/409) (Conflict)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses) (All server errors, including 500)

**`recommended`**: retries on
- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [409](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/409) (Conflict)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [502](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/502) (Bad Gateway)
- [503](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/503) (Service Unavailable)
- [504](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/504) (Gateway Timeout)

Use the `max_retries` request option to configure this behavior.

```python
client.audio.speech(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python
from speechify import Speechify

client = Speechify(..., timeout=20.0)

# Override timeout for a specific method
client.audio.speech(..., request_options={
    "timeout_in_seconds": 1
})
```

### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.

```python
import httpx
from speechify import Speechify

client = Speechify(
    ...,
    httpx_client=httpx.Client(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
