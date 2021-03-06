# Import twiddle_env to set up system path and tweak socket protocol
import twiddle_env
import pprint
import cherrypy

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()


START_ACTIVITY_KEYS = [
    "uri", "action", "data", "mimetype", "categories", "extras", "component",
    "flags"]


class Root(object):
    def key_event_type(self, kind):
        if kind is None:
            kind = "DOWN_AND_UP"
        return {
            "UP": MonkeyDevice.UP,
            "DOWN": MonkeyDevice.DOWN,
            "DOWN_AND_UP": MonkeyDevice.DOWN_AND_UP
        }[kind.upper()]

    @cherrypy.expose
    def index(self):
        return "Hello World!"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def broadcastIntent(self):
        request = cherrypy.request.json
        args = dict(
            (k, request[k]) for k in START_ACTIVITY_KEYS if k in request)
        kind = self.key_event_type(request.get("type"))
        device.broadcastIntent(**args)
        return "OK"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def drag(self):
        request = cherrypy.request.json
        device.drag((request["start"]["x"], request["start"]["y"]),
                    (request["end"]["x"], request["end"]["y"]),
                    request.get("duration", 1.0),
                    request.get("steps", 10))
        return "OK"

    @cherrypy.expose
    @cherrypy.tools.json_in(force=False)
    def getProperty(self, prop=None):
        if prop is None:
            prop = cherrypy.request.json["prop"]
        return device.getProperty(prop)

    @cherrypy.expose
    @cherrypy.tools.json_in(force=False)
    def getSystemProperty(self, prop=None):
        if prop is None:
            prop = cherrypy.request.json["prop"]
        return device.getSystemProperty(prop)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def press(self):
        request = cherrypy.request.json
        kind = self.key_event_type(request.get("type"))
        device.press(request["name"], kind)
        return "OK"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def startActivity(self):
        request = cherrypy.request.json
        args = dict(
            (k, request[k]) for k in START_ACTIVITY_KEYS if k in request)
        kind = self.key_event_type(request.get("type"))
        device.startActivity(**args)
        return "OK"

    @cherrypy.expose
    @cherrypy.tools.json_in(force=False)
    def screenshot(self, x=None, y=None, h=None, w=None):
        snapshot = device.takeSnapshot()

        request = {}
        if hasattr(cherrypy.request, "json"):
            request = cherrypy.request.json

        x = x or request.get("x")
        y = y or request.get("y")
        w = w or request.get("w")
        h = h or request.get("h")

        if x is not None and y is not None and h is not None and w is not None:
            snapshot = snapshot.getSubImage((int(x), int(y), int(h), int(w)))

        cherrypy.response.headers['Content-Type'] = 'image/png'
        # Need to call tostring to convert from Java array to something
        # descending from basestring (so cherrypy knows what to do)
        return snapshot.convertToBytes("png").tostring()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def touch(self):
        request = cherrypy.request.json
        kind = self.key_event_type(request.get("type"))
        device.touch(request["x"], request["y"], kind)
        return "OK"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def type(self):
        request = cherrypy.request.json
        device.type(request["message"])
        return "OK"

    @cherrypy.expose
    def wake(self):
        device.wake()
        return "OK"

cherrypy.config.update({'engine.autoreload.on': False})
cherrypy.server.nodelay = False
cherrypy.quickstart(Root())
