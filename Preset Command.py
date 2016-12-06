import sublime, sublime_plugin
from operator import itemgetter

is_ST2 = int(sublime.version()) < 3000
PRESETS = 'Presets.sublime-settings'

class PresetCommand(object):
	_instance = None

	@classmethod
	def instance(cls):
		if not cls._instance:
			cls._instance = cls()
		return cls._instance

	def list_presets(self, window, presets):
		def on_done(index):
			if index != -1:
				self.activate_preset(window, presets[index])
				sublime.status_message('Preset activated: ' + presets[index]['name'])

		window.show_quick_panel([[preset['name'], preset['description']] for preset in presets], on_done)

	def activate_preset(self, window, preset):
		if 'file' in preset:
			pf = preset['file']
		else:
			pf = 'Preferences.sublime-settings'

		if 'settings' in preset:
			preferences = sublime.load_settings(pf)

			for setting in preset['settings']:
				value = preset['settings'][setting]
				if value == '' and preferences.has(setting):
					preferences.erase(setting)
				else:
					preferences.set(setting, value)

			sublime.save_settings(pf)
			sublime.status_message('Preset: ' + preset['name'])

		if 'run' in preset:
			for cmd in (cmd for cmd in preset['run'] if len(preset['run']) > 0):
				window.run_command(cmd)

	def enable_preset(self, window, presets):
		def on_done(index):
			if index != -1:
				enabled_presets = self.get_presets('presets')
				disabled_presets = self.get_presets('disabled')

				preset = disabled_presets.pop(index)
				enabled_presets.append(preset)

				self.set_presets(enabled_presets, disabled_presets)
				sublime.status_message('Preset enabled: ' + preset['name'])

		window.show_quick_panel([[preset['name'], preset['description']] for preset in presets], on_done)

	def disable_preset(self, window, presets):
		def on_done(index):
			if index != -1:
				enabled_presets = self.get_presets('presets')
				disabled_presets = self.get_presets('disabled')

				preset = enabled_presets.pop(index)
				disabled_presets.append(preset)

				self.set_presets(enabled_presets, disabled_presets)
				sublime.status_message('Preset disabled: ' + preset['name'])

		window.show_quick_panel([[preset['name'], preset['description']] for preset in presets], on_done)

	def get_presets(self, preset_key):
		presets = sublime.load_settings(PRESETS).get(preset_key, [])
		presets.sort(key=itemgetter('name'))
		return presets

	def set_presets(self, enabled_presets, disabled_presets):
		presets = sublime.load_settings(PRESETS)
		presets.set('presets', enabled_presets)
		presets.set('disabled', disabled_presets)
		sublime.save_settings(PRESETS)

def plugin_loaded():
	PresetCommand.instance()

class PresetCommandListCommand(sublime_plugin.WindowCommand):
	def run(self):
		PresetCommand.instance().list_presets(self.window, PresetCommand.instance().get_presets('presets'))

	def is_enabled(self):
		return len(PresetCommand.instance().get_presets('presets')) > 0

class PresetCommandByNameCommand(sublime_plugin.WindowCommand):
	def run(self, name):
		PresetCommand.instance().activate_preset(self.window, [preset for preset in PresetCommand.instance().get_presets('presets') if preset['name'] == name][0])

	def is_enabled(self, name):
		return len([preset for preset in PresetCommand.instance().get_presets('presets') if preset['name'] == name]) > 0

class PresetCommandEnableCommand(sublime_plugin.WindowCommand):
	def run(self):
		PresetCommand.instance().enable_preset(self.window, PresetCommand.instance().get_presets('disabled'))

	def is_enabled(self):
		return len(PresetCommand.instance().get_presets('disabled')) > 0

class PresetCommandDisableCommand(sublime_plugin.WindowCommand):
	def run(self):
		PresetCommand.instance().disable_preset(self.window, PresetCommand.instance().get_presets('presets'))

	def is_enabled(self):
		return len(PresetCommand.instance().get_presets('presets')) > 0

if is_ST2: plugin_loaded()
