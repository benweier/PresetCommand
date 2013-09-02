import sublime, sublime_plugin

class PresetCommand():
	def list_presets(self, window, presets):

		def on_done(index):
			if index != -1:
				self.activate_preset(window, presets[index])
				sublime.status_message('Preset activated: '  + presets[index]['name'])

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
				if len(value) == 0 and preferences.has(setting):
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

PresetCommand = PresetCommand()

class PresetCommandListCommand(sublime_plugin.WindowCommand):
	def run(self):
		PresetCommand.list_presets(self.window, PresetCommand.get_enabled_presets())

	def is_enabled(self):
		return len(PresetCommand.get_enabled_presets()) > 0

class PresetCommandByNameCommand(sublime_plugin.WindowCommand):
	def run(self, name):
		PresetCommand.activate_preset(self.window, [preset for preset in PresetCommand.get_enabled_presets() if preset['name'] == name][0])

	def is_enabled(self, name):
		return len([preset for preset in PresetCommand.get_enabled_presets() if preset['name'] == name]) > 0

class PresetCommandEnableCommand(sublime_plugin.WindowCommand):
	def run(self):
		PresetCommand.enable_preset(self.window, PresetCommand.get_disabled_presets())

	def is_enabled(self):
		return len(PresetCommand.get_disabled_presets()) > 0

class PresetCommandDisableCommand(sublime_plugin.WindowCommand):
	def run(self):
		PresetCommand.disable_preset(self.window, PresetCommand.get_enabled_presets())

	def is_enabled(self):
		return len(PresetCommand.get_enabled_presets()) > 0
