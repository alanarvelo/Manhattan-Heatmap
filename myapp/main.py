from graph import prepare_graph
from bokeh.io import curdoc
from bokeh.io import output_file, show

layout = prepare_graph()
curdoc().add_root(layout)
curdoc().title = "Aja Data Lab — Manhattan Heatmap"