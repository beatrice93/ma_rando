import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, dcc, html, Input, Output

# Load the CSV data
df = pd.read_csv("data/hikes.csv", sep=",", decimal=",").drop(
    columns=["Identifiant", "Dénivelé négatif"]
)
df["Distance"] = (
    df["Distance"]
    .str.replace(" km", "")
    .str.replace(",", ".")
    .str.replace(" ", "")
    .astype(float)
)
df["Dénivelé positif"] = (
    df["Dénivelé positif"]
    .str.replace("+ ", "")
    .str.replace(" m", "")
    .str.replace(" ", "")
    .astype(int)
)
df["Difficulté"] = df["Difficulté"].astype(str)
df["Lignes"] = df["Lignes"].map(lambda cell: cell[1:-1].replace("'", ""))
df["Département"] = df["Département"].astype(str)
df["Lien"] = df["Lien"].apply(lambda x: html.A("lien", href=x))

# Check for "temps_de_trajet" column
has_temps_de_trajet = "Temps de trajet" in df.columns
if has_temps_de_trajet:
    df["Temps de trajet"] = df["Temps de trajet"].astype(int)

departements_list = df["Département"].unique().tolist()


# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H1("Ma rando"), width=12)),
        dbc.Row(dbc.Col(html.H2("Filtres"), width=12)),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Distance (km) :"),
                        dcc.RangeSlider(
                            id="distance-filter",
                            min=0,
                            max=50,
                            step=5,
                            value=[0, 50],
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        html.Label("Dénivelé (m) :"),
                        dcc.RangeSlider(
                            id="elevation-filter",
                            min=0,
                            max=1000,
                            value=[0, 1000],
                            step=100,
                        ),
                    ],
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Difficulté :"),
                        dcc.Dropdown(
                            id="difficulty-filter",
                            options=[
                                {"label": diff, "value": diff}
                                for diff in df["Difficulté"].unique()
                            ],
                            value=["Facile", "Moyenne", "Difficile"],
                            multi=True,
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        html.Label("Temps de voyage (minutes) :"),
                        dcc.Input(
                            id="time-filter",
                            type="number",
                            min=30,
                            value=60,
                            step=1,
                            disabled=not has_temps_de_trajet,
                        ),
                    ],
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Département :"),
                        dcc.Dropdown(
                            id="department-filter",
                            options=[
                                {"label": dept_name, "value": dept_name}
                                for dept_name in departements_list
                            ],
                            value=departements_list,
                            multi=True,
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("Rechercher une gare :"),
                        dcc.Dropdown(
                            id="station-filter",
                            options=[
                                {"label": station, "value": station}
                                for station in df["Gare départ"].unique()
                            ],
                            value="",
                            searchable=True,
                            multi=False,
                            clearable=True,
                        ),
                    ]
                ),
            ]
        ),
        dbc.Row(html.H2("Résultats")),
        dbc.Row(
            id="table-container",
            children=[
                dbc.Table.from_dataframe(df, id="hike-table"),
            ],
        ),
    ]
)


# Callback to update the table based on filters
@app.callback(
    Output("table-container", "children"),
    Input("distance-filter", "value"),
    Input("elevation-filter", "value"),
    Input("difficulty-filter", "value"),
    Input("time-filter", "value"),
    Input("department-filter", "value"),
    Input("station-filter", "value"),
)
def update_table(distance, elevation, difficulty, time, departement, gare):
    filtered_df = df

    if distance:
        filtered_df = filtered_df[filtered_df["Distance"].between(*distance)]

    if elevation:
        filtered_df = filtered_df[filtered_df["Dénivelé positif"].between(*elevation)]

    if difficulty:
        filtered_df = filtered_df[filtered_df["Difficulté"].isin(difficulty)]

    # Only filter by "Temps de trajet" if present
    if has_temps_de_trajet and time:
        filtered_df = filtered_df[filtered_df["Temps de trajet"].between(30, time)]

    if departement:
        filtered_df = filtered_df[filtered_df["Département"].isin(departement)]
        
    if gare:
        filtered_df = filtered_df[filtered_df["Gare départ"] == gare]

    # Only show "Temps de trajet" column if present
    display_df = filtered_df.copy()
    if not has_temps_de_trajet and "Temps de trajet" in display_df.columns:
        display_df = display_df.drop(columns=["Temps de trajet"])

    return dbc.Table.from_dataframe(display_df, id="hike-table")


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
