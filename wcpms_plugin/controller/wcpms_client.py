#
#    This file is part of Python Client Library for WCPMS.
#    Copyright (C) 2024 INPE.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Python Client Library for Web Crop Phenology Metrics Service"""

import json
import os
import urllib
import warnings
from datetime import datetime as dt
from datetime import timedelta

import geopandas as gpd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import requests
import seaborn as sns
from scipy.signal import savgol_filter

warnings.filterwarnings("ignore")

class WCPMS:
    """Implement a client for WCPMS.

    .. note::

        For more information about coverage definition, please, refer to
        `WCPMS specification <https://github.com/brazil-data-cube/wcpms-spec>`_.
    """

    def __init__(self, url, access_token=None):
        """Create a WCPMS client attached to the given host address (an URL).

        Args:
            url (str): URL for the WCPMS server.
            access_token (str, optional): Authentication token to be used with the WCPMS server.
        """
        #: str: URL for the WCPMS server.
        self._url = url

        #: str: Authentication token to be used with the WCPMS server.
        self._access_token = access_token

def get_phenometrics(url, cube, latitude, longitude):
    """Returns in dictionary form all the phenological metrics calculated for the given spatial location, as well as the time series and timeline used.

    Args:
        url: The url of the available wcpms service running

        cube : Dictionary with information about a BDC's data cubes with collection, start_date, end_date, freq and band.

        longitude : (int/float) A longitude value according to EPSG:4326.

        latitude : (int/float) A latitude value according to EPSG:4326.

    Returns:
        Phenometrics: A phenological metrics object as a dictionary.
        TimeSeries: A time series object as a dictionary.


    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If the response body is not a json document.

    Example:

        Retrieves a Phenometrics for S2-16D-2 data product:

        .. doctest::
            :skipif: WCPMS_EXAMPLE_URL is None

            >>> from wcpms import *
            >>> wcpms_url = WCPMS_EXAMPLE_URL
            >>> datacube = cube_query(
            ...                       collection="S2-16D-2",
            ...                       start_date="2021-01-01",
            ...                        end_date="2021-12-31",
            ...                       freq='16D',
            ...                       band="NDVI")
            >>> pm = get_phenometrics(
            ...                  url = wcpms_url,
            ...                  cube = datacube,
            ...                  latitude=-29.20, longitude= -55.95)
            ...
            >>> pm['phenometrics']
            {'aos_v': 2975.66650390625,
             'bse_v': 6233.1669921875,
             'eos_t': '2021-07-13T00:00:00',
             'eos_v': 5489.0,
             ...
             'sos_t': '2021-01-02T00:00:00',
             'sos_v': 7649.0, '
             'vos_t': '2021-12-20T00:00:00',
             'vos_v': 4817.33349609375
            }
    """
    query = dict(
        collection=cube['collection'],
        band=cube['band'],
        start_date=cube['start_date'],
        end_date=cube['end_date'],
        freq=cube['freq'],
        latitude=latitude,
        longitude=longitude,
    )

    url_suffix = '/phenometrics?'+urllib.parse.urlencode(query)

    data = requests.get(url + url_suffix)
    data_json = data.json()

    return data_json['result']

def cube_query(collection, start_date, end_date, freq, band):
    """An object that contains the information associated with a collection that can be downloaded or acessed.

    Args:
        collection: String containing the collection id identifier.

        start_date : String containing the begin of a time interval. Following YYYY-MM-DD structure.

        end_date : String containing the begin of a time interval. Following YYYY-MM-DD structure.

        freq : String containing the frequency of images of the associated collection. Following (N-days) structure.

        band : String containing the attribute (band) name.

    Returns:
    dictionary: A dictionary with information about a BDC's data cubes with collection, start_date, end_date, freq and band.


    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If the response body is not a json document.
    """
    return dict(
        collection = collection,
        band = band,
        start_date = start_date,
        end_date = end_date,
        freq=freq
    )

def smooth_timeseries(ts, method='savitsky', window_length=3, polyorder=1):
    if (method=='savitsky'):
        smooth_ts = savgol_filter(x=ts, window_length=window_length, polyorder=polyorder)
    return smooth_ts

def plot_phenometrics(cube, ds_phenos):

    y_new = smooth_timeseries(ts=ds_phenos['timeseries']['values'], method='savitsky', window_length=3)

    timeline = ds_phenos['timeseries']['timeline']
    timeseries = ds_phenos['timeseries']['values']
    phenometrics = ds_phenos['phenometrics']

    pos_t_minus = dt.strptime(phenometrics['pos_t'].split('T')[0], "%Y-%m-%d")
    pos_t_plus = dt.strptime(phenometrics['pos_t'].split('T')[0], "%Y-%m-%d")

    pos_t_minus = pos_t_minus - timedelta(days=5)
    pos_t_plus = pos_t_plus + timedelta(days=5)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        name='LIOS',
        mode="lines",
        x=[phenometrics['sos_t'].split('T')[0], phenometrics['sos_t'].split('T')[0], phenometrics['pos_t'].split('T')[0], phenometrics['eos_t'].split('T')[0], phenometrics["eos_t"].split('T')[0]],
        y=[0, phenometrics["sos_v"], phenometrics["pos_v"], phenometrics["eos_v"], 0],
        fill='toself',
        showlegend=False,
        fillcolor='rgba(153, 247, 254, 0.4)',
        line=dict(color= 'rgba(153, 247, 254, 0.4)')
    ))

    fig.add_trace(go.Scatter(
        name=cube['band'],
        x=timeline,
        y=timeseries,
        line=dict(color='#17BECF')
    ))

    fig.add_trace(go.Scatter(
        name="Smooth " + cube['band'],
        x=timeline,
        y=y_new,
        line=dict(color='#ff0000')
    ))

    fig.add_trace(go.Scatter(
        name='LOS',
        mode="lines",
        x=[phenometrics["sos_t"].split('T')[0], phenometrics["eos_t"].split('T')[0]],
        y=[phenometrics["sos_v"], phenometrics["eos_v"]],
        showlegend=False,
        line=dict(color='#000000', dash='dashdot')
    ))

    fig.add_trace(go.Scatter(
        name='AOS',
        mode="lines",
        x=[phenometrics["pos_t"].split('T')[0], phenometrics["pos_t"].split('T')[0]],
        y=[phenometrics["pos_v"], 0],
        showlegend=False,
        line=dict(color='#000000', dash='dashdot')
    ))

    fig.add_trace(go.Scatter(
        name='SOS',
        mode="markers",
        x=[phenometrics['sos_t'].split('T')[0]],
        y=[phenometrics['sos_v']],
        marker=dict(color='#008c00', size=12, line=dict(color= '#000000', width= 2) )
    ))

    fig.add_trace(go.Scatter(
        name='POS',
        mode="markers",
        x=[phenometrics["pos_t"].split('T')[0]],
        y=[phenometrics["pos_v"]],
        marker=dict(color='#0009e3', size=12, line=dict(color='#000000', width=2 ) )
    ))

    fig.add_trace(go.Scatter(
        name='EOS',
        mode="markers",
        x=[phenometrics["eos_t"].split('T')[0]],
        y=[phenometrics["eos_v"]],
        marker=dict(color='#8a6100', size=12, line=dict(color='#000000', width=2 ) )
    ))

    fig.add_trace(go.Scatter(
        name='VOS',
        mode="markers",
        x=[phenometrics["vos_t"].split('T')[0]],
        y=[phenometrics["vos_v"]],
        marker=dict(color='#e35400', size=12, line=dict(color='#000000', width=2 ) )
    ))

    fig.show()

def plot_phenometrics_matplotlib(cube, ds_phenos, layout = (12, 6), attr = {}):
    y_new = smooth_timeseries(ts=ds_phenos['timeseries']['values'], method='savitsky', window_length=3)

    timeline_str = ds_phenos['timeseries']['timeline']
    timeline = [dt.strptime(t.split('T')[0], "%Y-%m-%d") for t in timeline_str]
    timeseries = ds_phenos['timeseries']['values']
    phenometrics = ds_phenos['phenometrics']

    sos_t = dt.strptime(phenometrics['sos_t'].split('T')[0], "%Y-%m-%d")
    pos_t = dt.strptime(phenometrics['pos_t'].split('T')[0], "%Y-%m-%d")
    eos_t = dt.strptime(phenometrics['eos_t'].split('T')[0], "%Y-%m-%d")
    vos_t = dt.strptime(phenometrics['vos_t'].split('T')[0], "%Y-%m-%d")

    sos_v = phenometrics["sos_v"]
    pos_v = phenometrics["pos_v"]
    eos_v = phenometrics["eos_v"]
    vos_v = phenometrics["vos_v"]

    fig, ax = plt.subplots(figsize = layout) # convert from pixels to inches

    # Fill LIOS region
    lios_dates = [sos_t, sos_t, pos_t, eos_t, eos_t]
    lios_values = [0, sos_v, pos_v, eos_v, 0]
    ax.fill(lios_dates, lios_values, color='skyblue', alpha=0.4, label='LIOS')

    # Raw time series
    ax.plot(timeline, timeseries, label=cube['band'], color='#17BECF')

    # Smoothed time series
    ax.plot(timeline, y_new, label=f"Smooth {cube['band']}", color='#ff0000')

    # LOS line
    ax.plot([sos_t, eos_t], [sos_v, eos_v], linestyle='dashdot', color='black', label='LOS')

    # AOS line (vertical)
    ax.plot([pos_t, pos_t], [pos_v, 0], linestyle='dashdot', color='black', label='AOS')

    # SOS point
    ax.plot(sos_t, sos_v, 'o', label='SOS', color='#008c00', markersize=10, markeredgecolor='black', markeredgewidth=2)

    # POS point
    ax.plot(pos_t, pos_v, 'o', label='POS', color='#0009e3', markersize=10, markeredgecolor='black', markeredgewidth=2)

    # EOS point
    ax.plot(eos_t, eos_v, 'o', label='EOS', color='#8a6100', markersize=10, markeredgecolor='black', markeredgewidth=2)

    # VOS point
    ax.plot(vos_t, vos_v, 'o', label='VOS', color='#e35400', markersize=10, markeredgecolor='black', markeredgewidth=2)

    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    ax.set_title(("\nPhenological Metrics for\n{} ({})\n").format(*attr))
    plt.xlabel(None)
    plt.ylabel(None)
    ax.legend(
        bbox_to_anchor=(1.01, 1),
        loc='upper left',
        borderaxespad=0
    )

    plt.tight_layout()
    plt.show()

def plot_phenometrics_seaborn(cube, ds_phenos, layout=(12, 4), attr={}):
    # Smooth time series
    y_new = smooth_timeseries(ts=ds_phenos['timeseries']['values'], method='savitsky', window_length=3)

    # Prepare timeline and values
    timeline_str = ds_phenos['timeseries']['timeline']
    timeline = [dt.strptime(t.split('T')[0], "%Y-%m-%d") for t in timeline_str]
    timeseries = ds_phenos['timeseries']['values']
    phenometrics = ds_phenos['phenometrics']

    # Key phenology dates
    sos_t = dt.strptime(phenometrics['sos_t'].split('T')[0], "%Y-%m-%d")
    pos_t = dt.strptime(phenometrics['pos_t'].split('T')[0], "%Y-%m-%d")
    eos_t = dt.strptime(phenometrics['eos_t'].split('T')[0], "%Y-%m-%d")
    vos_t = dt.strptime(phenometrics['vos_t'].split('T')[0], "%Y-%m-%d")

    sos_v = phenometrics["sos_v"]
    pos_v = phenometrics["pos_v"]
    eos_v = phenometrics["eos_v"]
    vos_v = phenometrics["vos_v"]

    # Prepare DataFrame for Seaborn
    df = pd.DataFrame({
        'Date': timeline,
        'Raw': timeseries,
        'Smoothed': y_new
    })

    plt.figure(figsize=layout)
    ax = plt.gca()

    # Fill LIOS region (custom Matplotlib)
    lios_dates = [sos_t, sos_t, pos_t, eos_t, eos_t]
    lios_values = [0, sos_v, pos_v, eos_v, 0]
    ax.fill(lios_dates, lios_values, color='skyblue', alpha=0.4, label='LIOS')

    # Plot raw and smoothed lines
    sns.lineplot(data=df, x='Date', y='Raw', label=cube['band'], ax=ax, color='#17BECF')
    sns.lineplot(data=df, x='Date', y='Smoothed', label=f"Smooth {cube['band']}", ax=ax, color='#ff0000')

    # LOS line
    ax.plot([sos_t, eos_t], [sos_v, eos_v], linestyle='dashdot', color='black', label='LOS')

    # AOS line (vertical)
    ax.plot([pos_t, pos_t], [0, pos_v], linestyle='dashdot', color='black', label='AOS')

    # Plot phenology points (using Seaborn's scatter)
    sns.scatterplot(x=[sos_t], y=[sos_v], ax=ax, label='SOS',
                    color='#008c00', s=100, edgecolor='black', zorder=5)
    sns.scatterplot(x=[pos_t], y=[pos_v], ax=ax, label='POS',
                    color='#0009e3', s=100, edgecolor='black', zorder=5)
    sns.scatterplot(x=[eos_t], y=[eos_v], ax=ax, label='EOS',
                    color='#8a6100', s=100, edgecolor='black', zorder=5)
    sns.scatterplot(x=[vos_t], y=[vos_v], ax=ax, label='VOS',
                    color='#e35400', s=100, edgecolor='black', zorder=5)

    # Formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.xticks(rotation=30)

    ax.set_title(("Phenological Metrics for {} ({})\n").format(*attr))
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.legend(
        bbox_to_anchor=(1.01, 1),
        loc='upper left',
        borderaxespad=0
    )

    plt.tight_layout()
    plt.show()

def plot_advanced_phenometrics(cube, ds_phenos):

    y_new = smooth_timeseries(ts=ds_phenos['timeseries'], method='savitsky', window_length=3)

    timeline = ds_phenos['timeline'][:21]
    timeseries = ds_phenos['timeseries'][:21]
    phenometrics = ds_phenos['phenometrics']

    pos_t_minus = dt.strptime(phenometrics['pos_t'].split('T')[0], "%Y-%m-%d")
    pos_t_plus = dt.strptime(phenometrics['pos_t'].split('T')[0], "%Y-%m-%d")

    pos_t_minus = pos_t_minus - timedelta(days=5)
    pos_t_plus = pos_t_plus + timedelta(days=5)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        name='LIOS',
        mode="lines",
        x=[phenometrics['sos_t'].split('T')[0], phenometrics['sos_t'].split('T')[0], phenometrics['pos_t'].split('T')[0], phenometrics['eos_t'].split('T')[0], phenometrics["eos_t"].split('T')[0]],
        y=[0, phenometrics["sos_v"], phenometrics["pos_v"], phenometrics["eos_v"], 0],
        fill='toself',
        showlegend=False,
        fillcolor='rgba(153, 247, 254, 0.4)',
        line=dict(color= 'rgba(153, 247, 254, 0.4)')
    ))

    fig.add_trace(go.Scatter(
        name=cube['band'],
        x=timeline,
        y=timeseries,
        line=dict(color='#17BECF')
    ))

    fig.add_trace(go.Scatter(
        name="Smooth " + cube['band'],
        x=timeline,
        y=y_new,
        line=dict(color='#ff0000')
    ))

    fig.add_trace(go.Scatter(
        name='AOS',
        mode="lines",
        x=[phenometrics["pos_t"].split('T')[0], phenometrics["pos_t"].split('T')[0]],
        y=[phenometrics["pos_v"], 0],
        showlegend=False,
        line=dict(color='#000000', dash='dashdot')
    ))

    fig.add_trace(go.Scatter(
        name='SOS',
        mode="markers",
        x=[phenometrics['sos_t'].split('T')[0]],
        y=[phenometrics['sos_v']],
        marker=dict(color='#008c00', size=12, line=dict(color= '#000000', width= 2) )
    ))

    fig.add_trace(go.Scatter(
        name='POS',
        mode="markers",
        x=[phenometrics["pos_t"].split('T')[0]],
        y=[phenometrics["pos_v"]],
        marker=dict(color='#0009e3', size=12, line=dict(color='#000000', width=2 ) )
    ))


    fig.add_trace(go.Scatter(
        name='VOS',
        mode="markers",
        x=[phenometrics["vos_t"].split('T')[0]],
        y=[phenometrics["vos_v"]],
        marker=dict(color='#e35400', size=12, line=dict(color='#000000', width=2 ) )
    ))

    fig.add_trace(go.Scatter(
        name='EOS',
        mode="markers",
        x=[phenometrics["eos_t"].split('T')[0]],
        y=[phenometrics["eos_v"]],
        marker=dict(color='#8a6100', size=12, line=dict(color='#000000', width=2 ) )
    ))

    sos_time = dt.strptime(phenometrics['sos_t'].split('T')[0], "%Y-%m-%d")
    eos_time = dt.strptime(phenometrics['eos_t'].split('T')[0], "%Y-%m-%d")

    fig.add_vrect(x0=sos_time - timedelta(days=16), x1=sos_time + timedelta(days=16),
              annotation_text="Uncertainty", annotation_position="top left", fillcolor="green", opacity=0.25, line_width=0)

    fig.add_vrect(x0=eos_time - timedelta(days=16), x1=eos_time + timedelta(days=16),
              annotation_text="Uncertainty", annotation_position="top left", fillcolor="green", opacity=0.25, line_width=0)

    fig.show()

def get_collections(url):
    """List available data cubes in the BDC's SpatioTemporal Asset Catalogs (STAC).

    Args:
        url : The url of the available wcpms service running

    Returns:
    list: A list form the unique identifier of each of the data cubes available in the BDC's SpatioTemporal Asset Catalogs (STAC).


    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If the response body is not a json document.

    Example:

        Retrieves available data cubes in the BDC.

        .. doctest::
            :skipif: WCPMS_EXAMPLE_URL is None

            >>> from wcpms import *
            >>> wcpms_url = WCPMS_EXAMPLE_URL
            >>> collections = get_collections(wcpms_url)
            ...
            >>> collections
            ['CBERS4-MUX-2M-1', 'CBERS4-WFI-16D-2', 'CBERS-WFI-8D-1', 'LANDSAT-16D-1', 'mod13q1-6.1', 'myd13q1-6.1', 'S2-16D-2']
    """
    url_suffix = '/list_collections'

    data = requests.get(url + url_suffix)
    data_json = data.json()

    return data_json['coverages']

def get_description(url):
    """List the information on each of the phenological metrics, such as code, name, description and method.

    Args:
        url : The url of the available wcpms service running

    Returns:
    list: A list form the unique identifier of each of the phenological metrics, with its code, name, description and method.


    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If the response body is not a json document.
    """
    url_suffix = '/describe'

    data = requests.get(url + url_suffix)
    data_json = data.json()

    html_table = '<tr>'+'<td><b>Code</b></td>'+'<td><b>Name</b></td>'+'<td><b>Description</b></td>'+'<td><b>Method</b></td>'+'<td><b>Value</b></td>'+'<td><b>Time</b></td>'+'</tr>'

    for item in data_json['description']:
        html_table+='<tr>'+'<td>'+item['Code']+'</td>'+'<td>'+item['Name']+'</td>'+'<td>'+item['Description']+'</td>'+'<td>'+item['Method']+'</td>'+'<td>'+str(item['Value'])+'</td>'+'<td>'+str(item['Time'])+'</td>'+'</tr>'

    return data_json['description']

def gpd_read_file(shapefile_dir):
    data = gpd.read_file(os.path.join(shapefile_dir))
    return data

def gdf_to_geojson(df):
    return json.loads(df.to_json())["features"][0]['geometry']

def plot_points_region(polygon, phenos):
    x, y = [],[]
    for p in phenos:
        x.append(p["point"][0])
        y.append(p["point"][1])
    df = gpd.GeoSeries(polygon["geometry"])
    fig = px.scatter(df, x=x, y=y)
    fig.show()

def get_timeseries_region(url, cube, geom):
    """Retrieves the satellite images time series for each pixel centers within the boundaries of the given region from the Brazil Data Cube catalog.

    Args:
        url: The url of the available wcpms service running.

        cube : Dictionary with information about a BDC's data cubes with collection, start_date, end_date, freq and band.

        geom : GeoJSON containing the geometry used to retrive time series, according to EPSG:4326.

    Returns:
    list: A list of dictionaries with satellite images time series for each pixel.


    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If the response body is not a json document.
    """
    body = dict(
        collection=cube['collection'],
        band=cube['band'],
        start_date=cube['start_date'],
        end_date=cube['end_date'],
        freq=cube['freq'],
        geom=geom
    )

    url_suffix = '/timeseries'

    data = requests.post(url + url_suffix, json = body)

    data_json = data.json()

    return data_json['result']

def get_phenometrics_region(url, cube, timeseries):
    """List phenological metrics calculated for each spatial location within the boundaries of the given region.

    Args:
        url: The url of the available wcpms service running.

        cube : Dictionary with information about a BDC's data cubes with collection, start_date, end_date, freq and band.

        timeseries : JSON containing a list of dictionaries with satellite images time series for each pixel.

    Returns:
    list: A list of dictionaries with phenological metrics calculated for each pixel centers.


    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If the response body is not a json document.
    """
    body = dict(
        collection=cube['collection'],
        band=cube['band'],
        start_date=cube['start_date'],
        end_date=cube['end_date'],
        freq=cube['freq'],
        timeseries=timeseries
    )

    url_suffix = '/phenometrics'

    data = requests.post(url + url_suffix, json = body)
    data_json = data.json()

    return data_json['result']

def plot_points_region(polygon, phenos):
    x, y = [],[]
    for p in phenos:
        x.append(p["point"][0])
        y.append(p["point"][1])
    df = gpd.GeoSeries(polygon["geometry"])
    geo_axes = df.plot()
    geo_axes.scatter(x, y, c='red')
    geo_axes.plot()
