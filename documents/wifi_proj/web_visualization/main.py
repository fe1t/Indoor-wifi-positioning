from flask import Flask, render_template
from cell import CellQuery
app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True
    )


@app.route("/")
def visualize_data():
    cellquery = CellQuery()
    aps = cellquery.get()
    return render_template('visual.html', aps=aps)

if __name__ == "__main__":
    app.run(debug=True)
