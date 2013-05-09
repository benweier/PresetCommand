import sublime, sublime_plugin
import os

class PresetCommandListCommand(sublime_plugin.WindowCommand):
	def run(self):
		presets = sublime.load_settings('Presets.sublime-settings')
		preset_list = []
		
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
