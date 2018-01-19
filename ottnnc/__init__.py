import yaml, requests

from os import path
from buildui import get_layouts

from pyxley.utils import create_app, default_static_path, default_template_path

here = path.abspath(path.dirname(__file__))

def get_api_data():
    # load the configuration
    with open(here+'/config.yml', 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit()

    dataset = []
    for appname in config['apps']:
        print("Collecting %s" % appname)
        headers = {
            'Accept': 'application/json',
            'Authorization': 'key %s' % config['apps'][appname]['key'],
        }
        rq = requests.get('https://%s.data.thethingsnetwork.org/api/v2/query' % appname, headers=headers)
        if (rq.status_code == 401):
            print("Not authorized")
        else:
            if (rq.text):
                dataset.append(rq.json())

# create the flask app
app = create_app(here, default_static_path(), default_template_path())
app.brand = "MakeZurich"

# build the layout
get_layouts(app, here+"/../data/test.csv")

if __name__ == "__main__":
    # get_api_data()
    # TODO: filter the datasets by the value column in the config
    # ..... then pass it into the app layout
    app.run(debug=True)
