
from pdesign.app_plugins import RS_Plugin

def get_plugin(app):
	return Test_Plugin(app)

class Test_Plugin(RS_Plugin):

	id = 'TestPlugin'
	name = 'Test Plugin'

	def __init__(self, app):
		RS_Plugin.__init__(self, app)
