from urllib.parse import urlparse
from sanic import Sanic
from sanic.response import text
from sanic import testing
from spf import SanicPluginsFramework, SanicPlugin
import pytest


class TestPlugin(SanicPlugin):
    pass


# The following tests are taken directly from Sanic source @ v0.6.0
# and modified to test the SanicPluginsFramework, rather than Sanic

@pytest.mark.parametrize(
    'path,query,expected_url', [
        ('/foo', '', 'http://{}:{}/foo'),
        ('/bar/baz', '', 'http://{}:{}/bar/baz'),
        ('/moo/boo', 'arg1=val1', 'http://{}:{}/moo/boo?arg1=val1')
    ])
def test_plugin_ws_url_attributes(spf, path, query, expected_url):
    """Note, this doesn't _really_ test websocket functionality very well."""
    app = spf._app
    test_plugin = TestPlugin()

    async def handler(request):
        return text('OK')

    test_plugin.websocket(path)(handler)
    spf.register_plugin(test_plugin)
    test_client = app.test_client
    request, response = test_client.get(path + '?{}'.format(query))
    try:
        # Sanic 20.3.0 and above
        p = test_client.port
    except AttributeError:
        p = testing.PORT or 0
    assert request.url == expected_url.format(testing.HOST, str(p))
    parsed = urlparse(request.url)
    assert parsed.scheme == request.scheme
    assert parsed.path == request.path
    assert parsed.query == request.query_string
    assert parsed.netloc == request.host

