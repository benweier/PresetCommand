import sublime, sublime_plugin
import os

class PresetCommandListCommand(sublime_plugin.WindowCommand):
	def run(self):
		try:
			resource = sublime.load_resource('Packages/User/Presets.sublime-settings')
			presets = sublime.decode_value(resource)

			if len(presets) == 0:
				print('No presets found. Get one from the readme!')
			else:
				preset_list = []
				index = 0
				while index < len(presets):
					preset_list.append([presets[index]['name'], presets[index]['description']])
					index += 1

		except:
			print('Unable to load presets. Is there a presets file?')

		def on_done(index):
			if index != -1:
				self.set_preset(presets[index])

		self.window.show_quick_panel(preset_list, on_done)

	def set_preset(self, preset):
		if 'file' in preset.keys():
			if os.path.exists(os.path.join(sublime.packages_path(), 'User', preset['file'])):
				preferences = sublime.load_settings(preset['file'])
			else:
				sublime.error_message('The settings file (' + preset['file'] + ') does not exist.\n\nCheck the preset properties and try again.')
		else:
			preferences = sublime.load_settings('Preferences.sublime-settings')

		if 'settings' in preset.keys():
			for setting in preset['settings']:
				preferences.set(setting, preset['settings'][setting])

			sublime.save_settings(preferences)
			sublime.status_message('Preset: ' + presets[index]['name'])

		if 'run' in preset.keys():
			for cmd in preset['run']:
				self.window.run_command(cmd)
