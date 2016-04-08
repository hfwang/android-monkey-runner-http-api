import sys
sys.path.append('lib')

import socket
socket.IPPROTO_TCP = 6

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
        args = {}
        for k in START_ACTIVITY_KEYS:
            if k in request:
                args[k] = request[k]
        kind = self.key_event_type(request.get("type"))
        device.startActivity(**args)
        return "OK"

    @cherrypy.expose
    def screenshot(self):
        cherrypy.response.headers['Content-Type'] = 'image/png'
        # Cast Java array.array to string
        # device.takeSnapshot().writeToFile("/Users/darkwulf/Code/monkey-runner-api/screenshot.png")
        # return open("screenshot.png")
        return device.takeSnapshot().convertToBytes("png").tostring()

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
