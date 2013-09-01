# About
Preset Command is a Sublime Text plugin to manage collections of presets, by quickly and easily applying application or plugin settings from the command palette or with keyboard shortcuts.

Preset Command is non-persistent insofar that it does not track which preset is active or the state of your settings, allowing you to set up chains of presets that can be used in conjunction with other presets. For example, a Theme and Color Scheme preset may be used with a Proxy preset without interfering with each other.

# Installation
Install Preset Command through [Package Control](http://wbond.net/sublime_packages/package_control) or download and extract into your Packages folder.

# Getting Started
To get started with Preset Command, run `Manage Presets` from the Command Palette. This will open an empty file to begin adding presets.

```json
{
    "presets":
    [
        {
            "name": "Default",
            "description": "Default theme and color scheme",
            "settings":
            {
                "color_scheme": "Packages/Color Scheme - Default/Monokai.tmTheme",
                "theme": "Default.sublime-theme"
            }
        }
    ]
}
```

This won't do much if you're already using the default settings but it gives you a simple template to follow to begin using Preset Command. It can do more than just themes and color schemes too! Anything you can set through a Sublime Text `.sublime-settings` file, even plugins like Package Control, Emmet, or Soda Theme can be set through Preset Command. Advanced presets can even run commands like `toggle_side_bar` and `toggle_minimap` in a single preset.

# Usage

`Preset Command: List Presets` from the command palette will list your currently enabled presets. Select one to activate or press <kbd>Esc</kbd> to cancel.
Default shortcut: <kbd>ctrl+f4</kbd> (Windows/Linux) <kbd>super+f4</kbd> (OSX). This command is only available if at least 1 preset is enabled.

`Preset Command: Manage Presets` from the command palette will open your `Presets.sublime-settings` file for editing. This file contains an array of JSON objects as detailed below.

`Preset Command: Enable Preset` from the command palette will list your currently *disabled* presets. Select one to enable it for use in the `List Presets` command. This command is only available if at least 1 preset is already disabled.

`Preset Command: Disable Preset` from the command palette will list your currently *enabled* presets. Select one to disable it from the `List Presets` command. This command is only available if at least 1 preset is enabled.

# Preset Structure

Preset objects have the following properties:

`name`: **String**. *Required*. The name of your preset shown in the command palette, and also can be passed to the `preset_command_by_name` command in order to run it directly. It is recommended, but not enforced, that each preset be assigned a unique name.

`description`: **String**. *Required*. A short description of the preset, shown in the command palette for your own organisation.

`settings`: **Object**. *Optional*. Contains one or more `key: value` pairs that the preset will save when activated.

`run`: **Array**. *Optional*. Contains one or more Sublime Text commands (packaged or plugin) to execute. Arguments not supported.

`file`: **String**. *Optional*. Defaults to `Preferences.sublime-settings`. Specify a filename to target a settings file such as `Package Control.sublime-settings`, `Emmet.sublime-settings`, or any `.sublime-settings` file in your `User/` directory. Only one file can be acted on at a time.

# Settings Examples

The following are examples of using `settings` in a preset.

#### Going into a presentation and need to make your text easier to read on the projector?

```json
{
    "presets":
    [
        {
            "name": "Projector Mode",
            "description": "Bigger is better",
            "settings":
            {
                "font_size": 30,
                "line_numbers": false,
                "draw_indent_guides": false
            }
        }
    ]
}
```

#### Do you like to customise Sublime Text's appearance depending on where you are or the time of day?
(This example works if you have [Soda Theme](https://github.com/buymeasoda/soda-theme) and [Colour Schemes](http://buymeasoda.github.com/soda-theme/extras/colour-schemes.zip))

```json
{
    "presets":
    [
        {
            "name": "Dark",
            "description": "Like a smooth cup of coffee...",
            "settings":
            {
                "theme": "Soda Dark.sublime-theme",
                "color_scheme": "Packages/User/Monokai Soda.tmTheme",
                "soda_classic_tabs": true,
                "soda_folder_icons": true
            }
        },
        {
            "name": "Light",
            "description": "Classic Soda. Refreshing!",
            "settings":
            {
                "theme": "Soda Light.sublime-theme",
                "color_scheme": "Packages/User/Espresso Soda.tmTheme",
                "soda_classic_tabs": false,
                "soda_folder_icons": false
            }
        }
    ]
}
```

#### Using Package Control with a proxy at work but not at home?

When assigning an empty setting value (e.g. `"http_proxy": ""`) through Preset Command, Sublime Text will remove the named setting from the file which will revert back to its default value.

```json
{
    "presets":
    [
        {
            "name": "Home",
            "description": "No proxy",
            "settings": {
                "http_proxy": "",
                "https_proxy": ""
            },
            "file": "Package Control.sublime-settings"
        },
        {
            "name": "Work",
            "description": "Proxy",
            "settings": {
                "http_proxy": "example.proxy:1234",
                "https_proxy": "example.proxy:1234"
            },
            "file": "Package Control.sublime-settings"
        }
    ]
}
```

# Run Examples

Preset Command can also run commands just like you would from a shortcut or menu item, and can be used together with a `settings` object in the same preset. Passing command arguments is not supported.

Commands are executed in Sublime Text's `Window` scope so commands that perform actions in open files (such as text manipulation) will not work. This is outside the intended design of Preset Command and it is recommended to use Sublime Text's built-in Macro feature to order to achieve this goal.

#### Want nothing but the code?

```json
{
    "presets":
    [
        {
            "name": "Code Mode",
            "description": "From the 'I hate fullscreen' department",
            "run": ["toggle_menu", "toggle_side_bar", "toggle_minimap"]
        }
    ]
}
```

This will toggle the menu, sidebar, and minimap from their current state but won't set a specific state.
