import pickle
from sanic.response import text
from sanic.exceptions import NotFound
from spf import SanicPlugin


class TestPlugin(SanicPlugin):
    pass


instance = test_plugin = TestPlugin()

@test_plugin.route('/t1')
def t1(request):
    return text("t1")

@test_plugin.exception(NotFound)
def not_found(request):
    return text("404")

def test_plugin_pickle_unpickle(spf):
    app = spf._app
    p1 = pickle.dumps(test_plugin)
    p2 = pickle.loads(p1)
    spf.register_plugin(p2)
    client = app.test_client
    resp = client.get('/t1')
    assert resp[1].text == 't1'


