from flask import Flask, render_template
import json


app = Flask(__name__)
node_url = None


@app.route('/')
def static_page():
    return render_template('index.html', _node_url=node_url)


if __name__ == '__main__':
    try:
        cfg_file = open("explorer_config.json", "r")
        cfg = json.load(cfg_file)
        node_url = cfg['node_url']
    except Exception as ex:
        print('Missing configuration!')
        raise
    app.run()
