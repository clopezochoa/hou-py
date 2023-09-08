
# Houdini Python Tools

Python based tools to be used within HoudiniFX.

## License

GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Attribution Requirement:
If you use, modify, or distribute this software or any derivative
work based on this software, you must provide clear attribution to
the original author, Carlos Lopez Ochoa Aledo, by including a link to
his LinkedIn profile: [Carlos Lopez Ochoa Aledo's LinkedIn Profile](https://www.linkedin.com/in/cloa/).

Please adhere to this attribution requirement when using this software.

## Authors

Carlos López-Ochoa Aledo

- [github](https://www.github.com/clopezochoa)
- [linkedin](https://www.linkedin.com/in/cloa/)

## Installation

In order to be able to import custom python modules in houdini you should make a few checks:

1. Python scripts are stored in a path like this. If the scripts folder or the python folder don't exist, create them.
```
  C:\Users\'your_user_name'\Documents\houdini'your_houdini_version'\scripts\python
```
2. There must be a **PYTHONPATH** variable holding that path in the User Environment Variables dialog.