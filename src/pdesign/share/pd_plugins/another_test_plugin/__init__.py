
from pdesign.app_plugins import RS_Plugin

from pdesign.widgets import Label, CENTER

def get_plugin(app):
	return Test_Plugin(app)

class Test_Plugin(RS_Plugin):

	pid = 'AnotherTestPlugin'
	name = 'Another Test Plugin'

	def build_ui(self):
		label = Label(self.panel, self.name, True, 2, (255, 0, 0))
		self.panel.add(label, 0, CENTER, 5)

