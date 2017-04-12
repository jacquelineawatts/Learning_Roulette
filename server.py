from flask import Flask, request, render_template, session, flash, jsonify, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import requests
import ka_api
from nodes import TopicNode, VideoNode

app = Flask(__name__)

app.secret_key = "asdfasdf"
app.jinja_env.undefined = StrictUndefined

# Builds topic tree when first runnig the app
topic_tree = ka_api.call_api_and_return_tree('Topic')

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




