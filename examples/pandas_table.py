from dash import Dash
from html2dash import html2dash
import dash_mantine_components as dmc
import pandas as pd

element_map = {
    "table": dmc.Table,
}

df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
app = Dash()

pandas_table = html2dash(df.head(50).to_html(index=False), element_map=element_map)
pandas_table.children[0].striped = True
pandas_table.children[0].withBorder = True
app.layout = dmc.Container(pandas_table)

if __name__ == "__main__":
    app.run_server(debug=True)
