# ---- Importing Necessary Packages ----
# data handling packages
from pathlib import Path
import geopandas as gpd
import json
import os
from functools import partial
from helpers import map_other_config

#graph packages
from bokeh.models import ColumnDataSource, GMapOptions, GeoJSONDataSource, HoverTool, CheckboxGroup, Button, Toggle
from bokeh.plotting import figure, gmap
from bokeh.layouts import widgetbox, row, column
from bokeh.models import GeoJSONDataSource
from bokeh.models.glyphs import Patches
from bokeh.models.markers import Diamond, Circle
from shapely.geometry import Point, LineString, Polygon

try:
    MH_GMAPS_KEY = os.environ["MH_GMAPS_KEY"]
except:
    print("MH_GMAPS_KEY could not be imported")

def prepare_data():
    try:
        #____________
        # ---- Data Preparation ----
        #____________
        upper_dir = str(Path(__file__).parent.parent)
        # preparing Knotel offices data to place on Manhattan map
        kdf = gpd.read_file(upper_dir + '/data' + '/nyc_leased_enhanced.csv', index_col=0)
        # Knotel sometimes has various contracts per building, and information looks convoluted in map
        kdf.drop_duplicates(subset='address', inplace=True)
        # converting office data into Bokeh's native data type
        knotel_off = ColumnDataSource(data=kdf)

        # preparing tract data to divide Manhattan map
        gjb = gpd.read_file(upper_dir + '/data' + '/nyc_tract_w_mhi.geojson')
        mn = gjb.loc[gjb.COUNTY == u'New York County', :]
        # getting Tract data into GeoJSON data type
        patch_source = GeoJSONDataSource(geojson=mn.to_json())

        return knotel_off, patch_source

    except Exception as err:
        print("ERROR found on prepare_data:\n{}".format(err))


def prepare_graph():
    try:
        #____________
        # ---- Importing & Creating base figure from Google Maps ----
        #____________
        knotel_off, patch_source = prepare_data()

        # the map is set to Manhattan 
        map_options = GMapOptions(lat=40.737, lng=-73.990, map_type="roadmap", zoom=13, styles=json.dumps(map_other_config))
        #importing GMap into a Bokeh figure
        p = gmap(MH_GMAPS_KEY, map_options, title="Manhattan Heatmap",
                 plot_width=800, plot_height=650, output_backend="webgl",
                tools=['pan', 'wheel_zoom', 'reset', 'box_select', 'tap'])

        #____________
        # ---- OFFICES GLYPH ----
        #____________
        initial_office = Diamond(x="long", y="lat", size=18, fill_color="blue", fill_alpha=0.7, line_color="black", line_alpha=0.7)
        selected_office = Diamond(fill_color="blue", fill_alpha=1)
        nonselected_office = Diamond(fill_color="blue",  fill_alpha=0.15, line_alpha=0.15)
        # glyph gets added to the plot
        office_renderer = p.add_glyph(knotel_off, initial_office, selection_glyph = selected_office, nonselection_glyph = nonselected_office)
        # hover behavior pointing to office glyph
        office_hover = HoverTool(renderers=[office_renderer], tooltips=[("Revenue", "@revenue{$00,}"),("Rentable SQF", "@rentable_sqf{00,}"), 
                                                                        ("People density", "@ppl_density"), ("Address", "@formatted_address")])
        p.add_tools(office_hover)

        #____________
        # ---- TRACT GLYPH ----
        #____________
        tract_renderer = p.patches(xs='xs', ys='ys', source=patch_source, fill_alpha=0, line_color='red', 
                                                                            line_dash='dashed', hover_color='red', hover_fill_alpha=0.5)
        # hack to make tracts unselectable
        initial_tract = Patches(fill_alpha=0, line_color='red', line_dash='dashed')
        tract_renderer.selection_glyph = initial_tract
        tract_renderer.nonselection_glyph = initial_tract
        # hover behavior pointing to tract glyph
        tract_hover = HoverTool(renderers=[tract_renderer], tooltips= [("Median Household Income", "@MHI{$00,}")], mode='mouse') # 
        p.add_tools(tract_hover)

        # Other figure configurations
        p.yaxis.axis_label = "Latitude"
        p.xaxis.axis_label = "Longitude"
        p.toolbar.active_inspect = [tract_hover, office_hover]
        p.toolbar.active_tap =  "auto"
        p.toolbar.active_scroll = "auto"

        #____________
        # ---- Adding widgets & Interactions to figure
        #____________
        # creates a Toggle button
        show_office_toggle = Toggle(label ='Show Building Data', active=True, button_type='primary')
        # callback function for button
        def remove_add_office(active):
            office_renderer.visible = True if active else False
        # event handler
        show_office_toggle.on_click(remove_add_office)

        # same exact logic for tracts. To be combined into a single handler as an improvement!
        show_tract_toggle = Toggle(label ='Show Census Blocks', active=True, button_type='danger')
        def remove_add_tract(active):
            tract_renderer.visible = True if active else False
        show_tract_toggle.on_click(remove_add_tract)

        # plotting
        layout = column([p,
                         row([widgetbox(show_office_toggle), widgetbox(show_tract_toggle)])])

        return layout

    except Exception as err:
        print("ERROR found on prepare_graph:\n{}".format(err))