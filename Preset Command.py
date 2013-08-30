import sublime, sublime_plugin

class PresetCommand():
	def list_presets(self, window, preset_list):
		presets = [[preset['name'], preset['description']] for preset in preset_list]

		def on_done(index):
			if index != -1:
				self.set_preset(window, preset_list[index])

		window.show_quick_panel(presets, on_done)

	def get_presets(self):
		return sublime.load_settings('Presets.sublime-settings').get('presets', [])

	def set_preset(self, window, preset):
		if 'file' in preset:
			pf = preset['file']
		else:
			pf = 'Preferences.sublime-settings'

		if 'settings' in preset:
			preferences = sublime.load_settings(pf)

			for setting in preset['settings']:
				value = preset['settings'][setting]
				preferences.set(setting, value)

			sublime.save_settings(pf)
			sublime.status_message('Preset: ' + preset['name'])

		if 'run' in preset:
			for cmd in (cmd for cmd in preset['run'] if len(preset['run']) > 0):
				window.run_command(cmd)

PresetCommand = PresetCommand()

class PresetCommandListCommand(sublime_plugin.WindowCommand):
	def run(self):
		PresetCommand.list_presets(self.window, PresetCommand.get_presets())

	def is_enabled(self):
		return len(PresetCommand.get_presets()) > 0

class PresetCommandByNameCommand(sublime_plugin.WindowCommand):
	def run(self, name):
		PresetCommand.set_preset(self.window, [preset for preset in PresetCommand.get_presets() if preset['name'] == name][0])

	def is_enabled(self, name):
		return len([preset for preset in PresetCommand.get_presets() if preset['name'] == name]) > 0
