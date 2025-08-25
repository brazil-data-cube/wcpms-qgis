..
    This file is part of Python QGIS Plugin for WCPMS.
    Copyright (C) 2025 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.


=========================================================
Python QGIS Plugin for Web Crop Phenology Metrics Service
=========================================================

.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com/brazil-data-cube/wtss/blob/master/LICENSE
        :alt: Software License

.. image:: https://img.shields.io/badge/lifecycle-experimental-orange.svg
        :target: https://www.tidyverse.org/lifecycle/#experimental
        :alt: Software Life Cycle

.. image:: https://badges.gitter.im/brazil-data-cube/community.png
        :target: https://gitter.im/brazil-data-cube/community#
        :alt: Join the chat

.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord


Called Web Crop Phenology Metrics Service (WCPMS) the software extracts phenological metrics from big EO image collections, modeled as multidimensional data cubes, produced by the BDC project of INPE.

It allows analysts to calculate phenological metrics on cloud. The opposite of the on-premises established algorithms, so with no need to download big EO data sets on their personal computers.

We created the wcpms.py library from scratch to facilitate phenology extraction operations. This library was developed to be interoperable with other Python libraries, thus enabling users to integrate established libraries into their own workflows for pre- or post-processing and analysis. The wcpms.py library has a group of functions, the main ones are:

- ``get_collections``: returns in list format the unique identifier of each of the data cubes available in the BDC's SpatioTemporal Asset Catalogs (STAC).

- ``get_description``: returns in dictionary format the information on each of the phenology metrics, such as code, name, description and method.

- ``get_phenometrics``: returns in dictionary form all the phenological metrics calculated for the given spatial location.

For more information on WCPMS, see:

- `wcpms.py <https://github.com/brazil-data-cube/wcpms.py>`_: it is a Python client library that supports the communication to a WCPMS service.

- `wcpms server <https://github.com/GSansigolo/wcpms>`_: it is a client library for R.

- `wcpms documentation <https://wcpms.readthedocs.io/en/latest/>`_: the WCPMS documentation on readthedocs.

The WCPMS Plugin was developed by the Brazil Data Cube project, which offers a straightforward and efficient way to extracts phenological metrics from big EO image collections.

The primary goal of the presented plugin is to streamline and enhance access to the WCPMS service by providing users with a graphical interface that integrates directly into the QGIS environment.

The plugin WCPMS for QGIS is based on the Python programming language with the Python QT library, and its graphical interface with the software QT Designer.

Installation
------------

See `Development Installation <./wcpms/help/source/dev_install.rst>`_.

See `User Installation <./wcpms/help/source/user_install.rst>`_.

Changes
-------

See `History changes <./CHANGES.rst>`_.

License
-------

See `LICENSE <./LICENSE>`_.
