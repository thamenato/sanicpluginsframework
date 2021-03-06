from sanic import Sanic
from sanic.response import text, redirect
from spf import SanicPlugin, SanicPluginsFramework
from functools import partial
import logging

class TestPlugin(SanicPlugin):
    pass


instance = test_plugin = TestPlugin()

@test_plugin.route('/t1', with_context=True)
def t1(request, context):
    log = context.log
    log(logging.INFO, "hello world")
    debug = partial(log, logging.DEBUG)
    debug("hello debug")
    return text("t1")


def test_plugin_log1(spf):
    app = spf._app
    plugin = spf.register_plugin(test_plugin)
    client = app.test_client
    exceptions = None
    try:
        resp = client.get('/t1')
    except Exception as e:
        exceptions = e
    assert exceptions is None


