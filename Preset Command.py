import sublime, sublime_plugin
from operator import itemgetter

is_ST2 = int(sublime.version()) < 3000

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

		presets.sort(key=itemgetter('name'))
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
				enabled_presets = self.get_enabled_presets()
				disabled_presets = self.get_disabled_presets()

				preset = disabled_presets.pop(index)
				enabled_presets.append(preset)

				self.set_enabled_presets(enabled_presets)
				self.set_disabled_presets(disabled_presets)
				sublime.status_message('Preset enabled: '  + preset['name'])

		presets.sort(key=itemgetter('name'))
		window.show_quick_panel([[preset['name'], preset['description']] for preset in presets], on_done)

	def disable_preset(self, window, presets):
		def on_done(index):
			if index != -1:
				enabled_presets = self.get_enabled_presets()
				disabled_presets = self.get_disabled_presets()

				preset = enabled_presets.pop(index)
				disabled_presets.append(preset)

				self.set_enabled_presets(enabled_presets)
				self.set_disabled_presets(disabled_presets)
				sublime.status_message('Preset disabled: '  + preset['name'])

		presets.sort(key=itemgetter('name'))
		window.show_quick_panel([[preset['name'], preset['description']] for preset in presets], on_done)

	def set_enabled_presets(set, presets):
		sublime.load_settings('Presets.sublime-settings').set('presets', presets)
		sublime.save_settings('Presets.sublime-settings')

	def set_disabled_presets(self, presets):
		sublime.load_settings('Presets.sublime-settings').set('disabled', presets)
		sublime.save_settings('Presets.sublime-settings')

	def get_enabled_presets(self):
		return sublime.load_settings('Presets.sublime-settings').get('presets', [])

	def get_disabled_presets(self):
		return sublime.load_settings('Presets.sublime-settings').get('disabled', [])

def plugin_loaded():
    PresetCommand.instance()

class PresetCommandListCommand(sublime_plugin.WindowCommand):
	def run(self):
		PresetCommand.instance().list_presets(self.window, PresetCommand.instance().get_enabled_presets())

	def is_enabled(self):
		return len(PresetCommand.instance().get_enabled_presets()) > 0

class PresetCommandByNameCommand(sublime_plugin.WindowCommand):
	def run(self, name):
		PresetCommand.instance().activate_preset(self.window, [preset for preset in PresetCommand.instance().get_enabled_presets() if preset['name'] == name][0])

	def is_enabled(self, name):
		return len([preset for preset in PresetCommand.instance().get_enabled_presets() if preset['name'] == name]) > 0

class PresetCommandEnableCommand(sublime_plugin.WindowCommand):
	def run(self):
		PresetCommand.instance().enable_preset(self.window, PresetCommand.instance().get_disabled_presets())

	def is_enabled(self):
		return len(PresetCommand.instance().get_disabled_presets()) > 0

class PresetCommandDisableCommand(sublime_plugin.WindowCommand):
	def run(self):
		PresetCommand.instance().disable_preset(self.window, PresetCommand.instance().get_enabled_presets())

	def is_enabled(self):
		return len(PresetCommand.instance().get_enabled_presets()) > 0

if is_ST2: plugin_loaded()
