[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

This integration provides information about allergens available in the [TK Husteblume](https://www.tk.de/techniker/magazin/digitale-gesundheit/apps/husteblume-allergie-app-2025388) app.
For each allergen (e.g., Birch, Alder, etc.), an entity is created with its current level on the scale from 0 to 4.
The forecast for tomorrow and the day after tomorrow is provided via attributes.
The tracked allergens can be disabled via options.
All of them are turned into entities by default.

The app asks a user to enter some statistical information about them (an age group, a gender, and a birth month).
The integration mimics this behavior as the API requires this data.
Additionally, one needs to provide a tracking station.
Choosing the one closest to the user's location is recommended.
As there's no limit in the number of integration instances, one can create as many combinations of the user data as needed.

**This component will set up the following platforms.**

| Platform | Description                       |
| -------- | --------------------------------- |
| `sensor` | Show info from TK Husteblume API. |

{% if not installed %}

## Installation

1. Click install.
2. In the HA UI, go to "Configuration" -> "Integrations" click "+" and search for "TK Husteblume."

{% endif %}

## Configuration is done in the UI

<!---->

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[commits-shield]: https://img.shields.io/github/commit-activity/y/artspb/homeassistant-tk-husteblume.svg?style=for-the-badge
[commits]: https://github.com/artspb/homeassistant-tk-husteblume/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license]: https://github.com/artspb/homeassistant-tk-husteblume/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/artspb/homeassistant-tk-husteblume.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40artspb-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/artspb/homeassistant-tk-husteblume.svg?style=for-the-badge
[releases]: https://github.com/artspb/homeassistant-tk-husteblume/releases
[user_profile]: https://github.com/artspb
