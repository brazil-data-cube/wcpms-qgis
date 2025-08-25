#
# This file is part of Python QGIS Plugin for WCPMS.
# Copyright (C) 2025 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
#!/bin/bash

pydocstyle wcpms_plugin/*.py wcpms_plugin/controller/*.py wcpms_plugin/controller/files_export/*.py setup.py && \
isort wcpms_plugin setup.py --check-only --diff && \
check-manifest --ignore ".drone.yml,.readthedocs.yml" && \
sphinx-build -qnW --color -b doctest wcpms_plugin/help/source wcpms_plugin/help/_build && \
pytest
