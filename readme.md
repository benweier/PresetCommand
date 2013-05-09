# About
Preset Command is a Sublime Text plugin to manage collections of presets, by quickly and easily applying program or plugin settings from the command palette. Compatible with Sublime Text 2 and 3.

Preset Command is non-persistant insofar that it does not track which preset is active or the state of your settings, allowing you to set up chains of presets that can be used in conjunction with other presets. For example, a Theme and Color Scheme preset may be used with a Proxy preset without overriding each other.

# Installation
Install Preset Command through [Package Control](http://wbond.net/sublime_packages/package_control) or download and extract into your Packages folder.

# Usage
Use "Preset Command: Presets" from the command palette to list your current presets and select one to activate. Default shortcut: `ctrl+shift+f10` (Windows/Linux) `super+shift+f10` (OSX)

"Preset Command: Manage" from the command palette will open your `Presets.sublime-settings` file for editing. This file is an array of JSON objects with the following properties:

`name`: *Required*. The name of your preset that is used in the command palette.

`description`: *Required*. A short description of the preset for your own organisation.

`settings`: *Required*. An object containing one or more `key: value` pairs that the preset will save when activated.

`file`: *Optional*. Defaults to `Preferences.sublime-settings`. Specify a filename to target a plugin settings file such as `Package Control.sublime-settings`, `Emmet.sublime-settings`, or any `.sublime-settings` file in your `User/` directory.

# Examples
Preset Command includes a pretty simple default preset to get you started.

```json
[
    {
        "name": "Default",
        "description": "Default theme and color scheme",
        "settings":
        {
            "color_scheme": "Packages/Color Scheme - Default/Monokai Soda.tmTheme",
            "theme": "Soda Dark.sublime-theme"
        }
    }
]
```

This won't do much if you're already using the default settings but Preset Command can do more than just themes and color schemes! Anything you can set through a Sublime Text `.sublime-settings` file, even package settings such as Package Control, Emmet, or Soda Theme can be set through Preset Command.

#### Going into a presentation and need to make your text easier to read on the projector?

```json
[
    {
        "name": "Projector Mode",
        "description": "Bigger is better",
        "settings":
        {
            "font_size": 14
        }
    }
]
```

#### Do you like to customise Sublime Text's appearance depending on where you are or the time of day?
(This example works if you have [Soda Theme](https://github.com/buymeasoda/soda-theme) and [Colour Schemes](http://buymeasoda.github.com/soda-theme/extras/colour-schemes.zip))

```json
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
```

#### Using Package Control with a proxy at work but not at home?

```json
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
```
