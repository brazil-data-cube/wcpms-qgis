..
    This file is part of Python QGIS Plugin for WCPMS.
    Copyright (C) 2024 INPE.

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


=====================
WCPMS Plugin Overview
=====================

The figure below shows the WCPMS-QGIS interface containing the form with the parameters required to make requests to the WCPMS.

The first field to be selected refers to the data cube of interest; these cubes are products from satellites such as `Sentinel`, `CBERS`, and `Landsat`. The next parameter refers to the selection of the band or spectral index, whose time series will be used to calculate the phenological metrics.

After selecting these attributes, the user can choose the period of interest, which by default corresponds to one year of observations.

Finally, select the coordinate of interest (longitude and latitude), and use the Calculate Phenological Metrics button to compute the metrics using the selected parameters.

.. image:: ./assets/img/wcpms_plugin_overview.png
    :width: 30%
    :align: center
    :alt: WCPMS-PLUGIN


========================================
Retrieve and Export Phenological Metrics
========================================

In the example below, the calculation of phenological metrics was requested for a sample coordinate in the west of Bahia, in Barreiras, using as reference the NDVI time series derived from the `Copernicus Sentinel-2/MSI Level-2A` satellite for the full year of 2023.

In this example, it is possible to visualize the phenology of the time series and the highlighted metrics such as the `Peak of Season` (POS) and the `End of Season` (EOS). There is also a visualization of a sample `Sentinel-2` image corresponding to the date of the EOS metric.

.. image:: ./assets/screenshots/get_phenological_metrics.png
    :width: 100%
    :alt: WCPMS-PLUGIN
