from graph import prepare_graph
from pathlib import Path

from threading import Thread
from flask import Flask, render_template, request
from tornado.ioloop import IOLoop
from bokeh.embed import server_document
from bokeh.server.server import Server
from bokeh.themes import Theme

app = Flask(__name__)
app.debug = True
curr_dir = str(Path(__file__).parent)

def bkapp(doc):
    try:
        layout = prepare_graph()

        # curdoc().add_root(layout)
        doc.add_root(layout)
        doc.theme = Theme(filename=curr_dir + "/theme.yaml")
    except Exception as err:
        print("ERROR found on bkapp:\n{}".format(err))

@app.route('/', methods=['GET'])
def bkapp_page():
    try:
        print(request.__dict__)
        script = server_document('http://localhost:5006/bkapp') #headers={"host":"0.0.0.0"}
        return render_template("embed.html", script=script, template="Flask")
        return "hello world"
        # layout = prepare_graph()
        # curdoc().add_root(layout)
        # curdoc().title = "Aja Data Lab — Manhattan Heatmap"
        # return curdoc
    except Exception as err:
        print("ERROR found on bkapp_page:\n{}".format(err))

def bk_worker():
    try:
        # Can't pass num_procs > 1 in this configuration. If you need to run multiple
        # processes, see e.g. flask_gunicorn_embed.py
        server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8080", "0.0.0.0:8080", "localhost:5006", "172.17.0.1"]) #localhost:8000, port=8080, 'REMOTE_PORT': 56806"
        server.start()
        server.io_loop.start()
    except Exception as err:
        print("ERROR found on bk_worker:\n{}".format(err))

Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8080/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    # app.run(port=8080)
    app.run(debug=True, host='0.0.0.0', port=8080) # ssl_context=(curr_dir + '/cert.pem', curr_dir + '/key.pem') -p 5006:5006 -e MH_GMAPS_KEY=AIzaSyA0aGEr1BTCddZTgKgVf5vYZbmdDfpIGg0