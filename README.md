# HelixGenerator
Fusion 360 addin to generate helical curves

Note this curve is an approximation of a helix and not a true mathematical helix.

![Helix Cover](./resources/cover_image.png)

# Installation
[Click here to download the Add-in](https://github.com/tapnair/HelixGenerator/archive/master.zip)

After downloading the zip file follow the [installation instructions here](https://tapnair.github.io/installation.html) for your particular OS version of Fusion 360 

## Usage:
Select a plane or planar face and let it generate a helix from the origin of that plane or face

NOTE: The command was moved to the "Create" dropdown in the solid environment

There are three options that can be set by opening and editing the HelixCommand.py file:

 * __USE_DEFAULT_PLANE__: Set this to True to automatically populate the initial selection field, default is False
 * __DEFAULT_PLANE__: If the above value is true this will be the default selection (in the active component)
 * __SHOW_COMPONENT_ORIGIN_FOLDER__: Whether the default construction entities will be shown for the active component

## License
Samples are licensed under the terms of the [MIT License](http://opensource.org/licenses/MIT). Please see the [LICENSE](LICENSE) file for full details.

## Written by

Written by [Patrick Rainsberry](https://twitter.com/prrainsberry) <br /> (Autodesk Fusion 360 Business Development)

See more useful [Fusion 360 Utilities](https://tapnair.github.io/index.html)

[![Analytics](https://ga-beacon.appspot.com/UA-41076924-3/HelixGenerator)](https://github.com/igrigorik/ga-beacon)
