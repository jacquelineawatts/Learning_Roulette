""" 
Todos: 
1) Work on hover over of d3 circles---need to a) bring circles to foreground and b) 
show tooltip text only if not already showing upon load.

2) Right now loading API response takes awhile upon first loading the app. Need to 
cache this response and set up cron job to refresh cache (every 24 hrs?)

3) Have svg center on the largest node (math), right now scrollBy has been 
implemented for quick fix.

4) Work on formatting of video modal.
"""

from flask import Flask, request, render_template, session, flash, jsonify, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import requests
import ka_api
from nodes import TopicNode, VideoNode
import cPickle as pickle

app = Flask(__name__)

app.secret_key = "asdfasdf"
app.jinja_env.undefined = StrictUndefined

# Loads cpickle of topic tree built from API response.
# This is globally accessible to all routes.
with open('topic_tree_response.p', 'rb') as pickle_file:
    topic_tree = pickle.load(pickle_file)


@app.route('/')
def show_homepage():
    """Displays homepage."""

    return render_template('homepage.html')


@app.route('/data.json')
def get_data_for_d3():
    """Takes initial API response data and creates nodes and paths for D3 viz."""

    nodes, paths = ka_api.find_nodes_and_paths(topic_tree.head)
    chart_data = jsonify({'nodes':nodes, 'paths':paths})

    return chart_data


@app.route('/find_video')
def get_video():
    """Receives click data from AJAX get request and returns video from API."""

    time = int(request.args.get('time')) * 60
    slug = request.args.get('slug')
    node = topic_tree.head.find_node(slug)
    print 'NODE: ', node

    video = ka_api.get_video(slug, time, node)

    return jsonify(video)


if __name__ == "__main__":

    app.debug = True
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # DebugToolbarExtension(app)
    app.run(host="127.0.0.1")




