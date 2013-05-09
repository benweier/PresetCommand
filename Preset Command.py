import sublime, sublime_plugin
import os

class PresetCommandListCommand(sublime_plugin.WindowCommand):
	def run(self):
		preset_list = []

		if not os.path.exists(os.path.join(sublime.packages_path(), 'User', 'Presets.sublime-settings')):
			default_preset = [{"name": "Default", "description": "Default theme and color scheme", "settings": {"theme": "Default.sublime-theme", "color_scheme": "Packages/Color Scheme - Default/Monokai.tmTheme"}}]
			f = open(os.path.join(sublime.packages_path(), 'User', 'Presets.sublime-settings'), 'w')
			f.write(sublime.encode_value(default_preset, True))
			f.close()

		presets = sublime.decode_value(sublime.load_resource('Packages/User/Presets.sublime-settings'))

		for preset in presets:
			preset_list.append([preset['name'], preset['description']])

		def on_done(index):
			if index != -1:
				self.set_preset(presets[index])
				sublime.status_message('Preset: ' + presets[index]['name'])

		self.window.show_quick_panel(preset_list, on_done)

	def set_preset(self, preset):
		if 'file' in preset.keys():
			if os.path.exists(os.path.join(sublime.packages_path(), 'User', preset['file'])):
				preferences = sublime.load_settings(preset['file'])
			else:
				sublime.error_message('The settings file (' + preset['file'] + ') does not exist.\n\nCheck the preset properties and try again.')
		else:
			preferences = sublime.load_settings('Preferences.sublime-settings')

		for setting in preset['settings']:
			preferences.set(setting, preset['settings'][setting])

		sublime.save_settings(preferences)
