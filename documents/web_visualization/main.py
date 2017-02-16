from flask import Flask, render_template, request
from cell import CellQuery
app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True
    )


@app.route("/", methods=["GET"])
def main():
    cellquery = CellQuery()
    bssid_list = cellquery.get_bssid_list()
    return render_template('index.html', bssid_list=bssid_list)

@app.route("/show", methods=["GET"])
def visualize_data():
    bssid = request.args.get('bssid', None)
    if bssid == None:
        return ""
    cellquery = CellQuery()
    aps = cellquery.get(bssid)
    return render_template('visual.html', aps=aps)

if __name__ == "__main__":
    app.run(debug=True)
