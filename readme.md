# About
Preset Command is a Sublime Text plugin to manage collections of presets, by quickly and easily applying application or plugin settings from the command palette. Compatible with Sublime Text 3.

Preset Command is non-persistent insofar that it does not track which preset is active or the state of your settings, allowing you to set up chains of presets that can be used in conjunction with other presets. For example, a Theme and Color Scheme preset may be used with a Proxy preset without interfering with each other.

# Installation
Install Preset Command through [Package Control](http://wbond.net/sublime_packages/package_control) or download and extract into your Packages folder.

# Getting Started
To get started with Preset Command, run `Manage Presets` from the Command Palette. This will open an empty file to begin adding your desired presets.

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
Use "Preset Command: List Presets" from the command palette to list your current presets and select one to activate. Default shortcut: <kbd>ctrl+shift+f10</kbd> (Windows/Linux) <kbd>super+shift+f10</kbd> (OSX)

"Preset Command: Manage Presets" from the command palette will open your `Presets.sublime-settings` file for editing. This file contains an array of JSON objects with the following properties:

`name`: *Required*. The name of your preset shown in the command palette, and also can be passed to the `preset_command_name` command in order to run it directly. It is recommended, but not enforced, that each preset be assigned a unique name.

`description`: *Required*. A short description of the preset, shown in the command palette for your own organisation.

`settings`: *Optional*. An object containing one or more `key: value` pairs that the preset will save when activated.

`run`: *Optional*. An array containing one or more Sublime Text commands (packaged or plugin) to execute. Arguments not yet supported.

`file`: *Optional*. Defaults to `Preferences.sublime-settings`. Specify a filename to target a settings file such as `Package Control.sublime-settings`, `Emmet.sublime-settings`, or any `.sublime-settings` file in your `User/` directory. Only one file can be acted on at a time.

# Settings Examples

The following are examples of using `settings` in a preset.

### Going into a presentation and need to make your text easier to read on the projector?

```json
{
    "presets":
    [
        {
            "name": "Projector Mode",
            "description": "Bigger is better",
            "settings":
            {
                "font_size": 20
            }
        }
    ]
}
```

### Do you like to customise Sublime Text's appearance depending on where you are or the time of day?
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
                "soda_classic_tabs": false,
                "soda_folder_icons": false
            }
        },
        {
            "name": "Light",
            "description": "Classic Soda. Refreshing!",
            "settings":
            {
                "theme": "Soda Light.sublime-theme",
                "color_scheme": "Packages/User/Espresso Soda.tmTheme",
                "soda_classic_tabs": true,
                "soda_folder_icons": true
            }
        }
    ]
}
```

### Using Package Control with a proxy at work but not at home?

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

Preset Command can also run commands just like you would from a shortcut or menu item, and can also be used with a `settings` object in the same preset. Passing command arguments is not yet supported.

### Want nothing but the code?

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

This will toggle the menu, sidebar, and minimap from their current state but can't set a specific state.
