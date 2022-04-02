import math
from flask import Flask
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import datetime as dt
from dash.dependencies import State, Input, Output
from dash.exceptions import PreventUpdate

server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
#application = app

# token guweh
# mapbox_access_token = "pk.eyJ1Ijoia3VydWsiLCJhIjoiY2tndHhrYTg0MDZ2NjJ0bnhlOHE3bmpraSJ9.F6_8CkQDbsA-EKC-M6sgNQ"

mapbox_access_token = "pk.eyJ1IjoiaGFuYTAwMSIsImEiOiJja2d1aGt5dm0wZGJvMnFxZnA5b3R5cDB0In0.khUMJXzZmTNfFoO7BfPmVA"

df = pd.read_csv("Data_FM_cleaned.csv")
init_state = df["PROVINSI"].unique()
init_region = df["KABUPATEN/KOTA"].unique()
init_bar_chart = ["- 1 - Sebaran Nilai BHP", "- 2 - Jumlah Alokasi Kanal",
                  "- 3 - Ketersediaan Kanal", "- 4 - Sebaran Umur ISR",
                  "- 5 - ERP Power vs Antenna Height", "- 6 - ERP Power vs Antenna Model",
                  "- 7 - ERP Power vs Tinggi ASL", "- 8 - ERP Power vs Tinggi Antena vs Tinggi ASL",
                  "- 9 - Tinggi ASL vs Tinggi Antena", "- 10 - Lama Waktu Perizinan", "- 11 - Anomali PM 3 Tahun 2017"]
init_style_map = ["Simply Black", "Satellite", "Calming Blue", "Outdoor Play", "Icy Cold", "Disco Night", "Terracota"]
init_options_map = ["- 1 - Semua Wilayah : Kosong & Terisi",
                    "- 2 - Semua Wilayah : Kosong",
                    "- 3 - Semua Wilayah : Terisi",
                    "- 4 - Perbatasan : Kosong & Terisi",
                    "- 5 - Perbatasan : Kosong",
                    "- 6 - Perbatasan : Terisi",
                    "- 7 - Lokasi Prioritas (LOKPRI)"]

WISTARA_LOGO = "assets/logo_wistara.png"

app.title = 'sidasan'
app.layout = html.Div(dbc.Container(
    children=[
        dbc.Row(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dbc.Row(
                                    children=[
                                        html.Div(
                                            html.Img(src=WISTARA_LOGO, height="62px"),
                                            # width={"size": 4, "offset": 3}
                                            className="col-md-3",
                                        ),
                                        html.Div(
                                            children=[
                                                dbc.NavbarBrand(
                                                    children=[
                                                        html.H1("sidasan / FM Broadcast",
                                                                style={"margin-top": "7px",
                                                                       "margin-bottom": "2px"},
                                                                className="rata-tengah"),
                                                        html.H5(
                                                            "Gaining Insight through Diverse and "
                                                            "Interactive Analytic Dashboards",
                                                            className="rata-tengah",
                                                            style={"font-style": "italic",
                                                                   "margin-bottom": "0px"},
                                                        ),
                                                    ],
                                                ),
                                            ],
                                            className="col-md-6 rata-tengah",
                                        ),
                                        html.Div(
                                            html.Img(src="assets/logo_ifast-fest.png", height="61px"),
                                            # dcc.Dropdown(
                                            #     id="map-style-select", multi=False,
                                            #     searchable=False,
                                            #     options=[{"label": i, "value": i} for i in
                                            #     sorted(init_style_map)],
                                            #     placeholder="Pilihan Style Map"
                                            # ),
                                            className="col-md-3 rata-kanan",
                                        ),
                                    ],
                                    align="center",
                                    # justify="left",
                                    # no_gutters=True,
                                    # className="ml-auto"
                                ),
                            ],
                            # color="light",
                            style={"padding": "15px"},
                            # sticky="fixed",
                            className="bg-light",
                        ),
                    ],
                    className="col-md-12",
                ),
            ],
            # style={"margin-bottom": "30px"},
            # className="col-md-6 col-lg-4 col-xl-3",
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        dbc.Row(
                                            children=[
                                                dbc.Col(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("SELAMAT DATANG",
                                                                               className="card-header-custom2",
                                                                               ),
                                                                dbc.CardBody(
                                                                    [
                                                                        # html.H4("Welcome,", className="card-title"),
                                                                        html.H5("Civitas SDPPI",
                                                                                className="card-title"),
                                                                    ],
                                                                    className="card-body-custom",
                                                                    style={"min-height": "80px"},
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        )
                                    ],
                                    width={"size": 3, "order": 0},
                                ),
                                dbc.Col(
                                    children=[
                                        dbc.Row(
                                            children=[
                                                dbc.Col(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Alokasi Kanal",
                                                                               className="card-header-custom"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="info_alokasi_kanal",
                                                                            className="card-title",
                                                                        ),
                                                                        # html.P(
                                                                        #     "Alokasi Kanal",
                                                                        #     className="card-text"
                                                                        # ),
                                                                    ],
                                                                    className="card-body-custom",
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                    style={"text-align": "center"},
                                                    width={"size": 2, "order": 0},
                                                ),
                                                dbc.Col(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Kanal Terisi",
                                                                               className="card-header-custom"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="info_kanal_terisi",
                                                                            className="card-title",
                                                                        ),
                                                                        # html.P(
                                                                        #     "Kanal Terisi",
                                                                        #     className="card-text"
                                                                        # ),
                                                                    ],
                                                                    className="card-body-custom",
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                    style={"padding-left": "0px", "text-align": "center"},
                                                    width={"size": 2, "order": 1},
                                                ),
                                                dbc.Col(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Kanal Kosong",
                                                                               className="card-header-custom"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="info_kanal_kosong",
                                                                            className="card-title",
                                                                        ),
                                                                        # html.P(
                                                                        #     "Kanal Kosong",
                                                                        #     className="card-text"
                                                                        # ),
                                                                    ],
                                                                    className="card-body-custom",
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                    style={"padding-left": "0px", "text-align": "center"},
                                                    width={"size": 2, "order": 2},
                                                ),
                                                dbc.Col(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Total BHP",
                                                                               className="card-header-custom",
                                                                               ),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="info_total_BHP",
                                                                            # className="card-title d-flex "
                                                                            #         "align-content-stretch "
                                                                            #        "flex-wrap",
                                                                            # style={"text-width": "100%"},
                                                                        ),
                                                                        # html.P(
                                                                        #     "Total BHP",
                                                                        #     className="card-text"
                                                                        # ),
                                                                    ],
                                                                    className="card-body-custom",
                                                                    style={"padding": "1.25rem 1rem"},
                                                                ),
                                                            ],
                                                            # className="h-100"
                                                        ),
                                                    ],
                                                    style={"padding-left": "0px", "text-align": "center"},
                                                    width={"size": 2, "order": 3},
                                                ),
                                                dbc.Col(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Provinsi Dipilih",
                                                                               className="card-header-custom"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="article-state",
                                                                            className="card-title",
                                                                        ),
                                                                        # html.P(
                                                                        #     "Provinsi Dipilih",
                                                                        #     className="card-text"
                                                                        # ),
                                                                    ],
                                                                    className="card-body-custom",
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                    style={"padding-left": "0px", "text-align": "center"},
                                                    width={"size": 2, "order": 4},
                                                ),
                                                dbc.Col(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Kab./ Kota Dipilih",
                                                                               className="card-header-custom"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="article-region",
                                                                            className="card-title",
                                                                        ),
                                                                        # html.P(
                                                                        #     "Kab./Kota Dipilih",
                                                                        #     className="card-text"
                                                                        # ),
                                                                    ],
                                                                    className="card-body-custom",
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                    style={"padding-left": "0px", "text-align": "center"},
                                                    width={"size": 2, "order": 5},
                                                ),
                                            ],
                                        ),
                                    ],
                                    width={"size": 9, "order": 1},
                                    style={"padding-left": "0px"},
                                ),
                            ],
                        ),
                        dbc.Card(
                            [
                                # dbc.CardHeader("Pilih Provinsi"),
                                dbc.CardBody(
                                    [
                                        dcc.Loading(
                                            id="loading",
                                            children=dcc.Graph(
                                                id="geo-map",
                                                style={
                                                    "margin-right": "0px",
                                                    "margin-left": "0px",
                                                    "padding-left": "0px",
                                                },
                                                figure={
                                                    "data": [],
                                                    "layout": dict(
                                                        plot_bgcolor='rgba(0,0,0,0)',
                                                        paper_bgcolor='rgba(0,0,0,0)',
                                                    ),
                                                },
                                                config={
                                                    # 'doubleClickDelay': 1000,
                                                    # 'displayModeBar' : True
                                                },
                                            ),
                                        ),
                                    ],
                                    className="dash-graph-custom",
                                ),
                            ],
                            style={
                                "margin-top": 15,
                                # "width": 100%,
                                # "margin": 0 auto,
                                # "padding-left": "0px",
                                # "padding-right": "0px",
                            },
                            # className="card-body map-no-padding",
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        dbc.Row(
                                            children=[
                                                dbc.Col(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Pilihan Map Style",
                                                                               className="rata-tengah "
                                                                                         "card-header-ketzil"),
                                                                dbc.CardBody(
                                                                    [
                                                                        dcc.Dropdown(
                                                                            id="map-style-select", multi=False,
                                                                            searchable=False,
                                                                            options=[{"label": i, "value": i} for i in
                                                                                     sorted(init_style_map)],
                                                                            placeholder="Pilihan Style Map",
                                                                        )
                                                                    ],
                                                                    className="card-body-ketzil",
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dbc.Row(
                                            children=[
                                                dbc.Col(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Pilihan Data Parameter",
                                                                               className="rata-tengah "
                                                                                         "card-header-ketzil"),
                                                                dbc.CardBody(
                                                                    [
                                                                        dcc.Dropdown(
                                                                            id="map-filter-options", multi=False,
                                                                            searchable=False,
                                                                            options=[{"label": i, "value": i} for i in
                                                                                     sorted(init_options_map)],
                                                                            placeholder="Pilih Data Parameter",
                                                                        ),
                                                                    ],
                                                                    className="card-body-ketzil",
                                                                ),
                                                            ],
                                                            style={"margin-top": "15px"},
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                    width={"size": 5, "order": 0},
                                ),
                                dbc.Col(
                                    children=[
                                        dbc.Row(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Titik Selection",
                                                                               className="card-header-ketzil"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="info_map_titik_terselect",
                                                                            className="card-title",
                                                                            style={"font-size": "1.25rem"},
                                                                        ),
                                                                        # html.P(
                                                                        #     "Alokasi Kanal",
                                                                        #     className="card-text"
                                                                        # ),
                                                                    ],
                                                                    className="card-body-ketzil",
                                                                ),
                                                            ],
                                                        ),
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Kanal Terisi",
                                                                               className="card-header-ketzil"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="info_kanal_terisi_terselect",
                                                                            className="card-title",
                                                                            style={"font-size": "1.25rem"},
                                                                        ),
                                                                        # html.P(
                                                                        #     "Kanal Terisi",
                                                                        #     className="card-text"
                                                                        # ),
                                                                    ],
                                                                    className="card-body-ketzil",
                                                                ),
                                                            ],
                                                            className="card-custom",
                                                        ),
                                                    ],
                                                    style={"text-align": "center"},
                                                    # width={"size": 4, "order": 0},
                                                    className="col-md-4",
                                                ),
                                                html.Div(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Kanal Kosong",
                                                                               className="card-header-ketzil"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="info_kanal_kosong_terselect",
                                                                            className="card-title",
                                                                            style={"font-size": "1.25rem"},
                                                                        ),
                                                                    ],
                                                                    className="card-body-ketzil",
                                                                ),
                                                            ],
                                                        ),
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Total BHP",
                                                                               className="card-header-ketzil"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="info_bhp_terselect",
                                                                            className="card-title",
                                                                            style={"font-size": "1.25rem"},
                                                                        ),
                                                                        # html.P(
                                                                        #     "Total BHP",
                                                                        #     className="card-text"
                                                                        # ),
                                                                    ],
                                                                    className="card-body-ketzil",
                                                                ),
                                                            ],
                                                            className="card-custom",
                                                        ),

                                                    ],
                                                    style={"text-align": "center"},
                                                    className="col-md-4",
                                                ),
                                                html.Div(
                                                    children=[
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Provinsi",
                                                                               className="card-header-ketzil"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="info_provinsi_terselect",
                                                                            className="card-title",
                                                                            style={"font-size": "1.25rem"},
                                                                        ),
                                                                        # html.P(
                                                                        #     "Provinsi Dipilih",
                                                                        #     className="card-text"
                                                                        # ),
                                                                    ],
                                                                    className="card-body-ketzil",
                                                                ),
                                                            ],
                                                        ),
                                                        dbc.Card(
                                                            children=[
                                                                dbc.CardHeader("Kab./ Kota Dipilih",
                                                                               className="card-header-ketzil"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.P(
                                                                            "0",
                                                                            id="info_kab_kot_terselect",
                                                                            className="card-title",
                                                                            style={"font-size": "1.25rem"},
                                                                        ),
                                                                        # html.P(
                                                                        #     "Kab./Kota Dipilih",
                                                                        #     className="card-text"
                                                                        # ),
                                                                    ],
                                                                    className="card-body-ketzil",
                                                                ),
                                                            ],
                                                            className="card-custom",
                                                        ),

                                                    ],
                                                    style={"text-align": "center"},
                                                    className="col-md-4",
                                                ),
                                            ],
                                        ),
                                    ],
                                    width={"size": 7, "order": 1},
                                    style={"padding-left": "0px"},
                                ),
                            ],
                            style={
                                "margin-top": 15,
                            },
                        ),
                        dbc.Card(
                            children=[
                                dbc.CardHeader("-- Pilihan Metrik Analisis --",
                                               className="rata-tengah card-header-ketzil"),
                                dbc.CardBody(
                                    [
                                        dcc.Dropdown(
                                            id="chart-select", multi=False,
                                            searchable=False,
                                            options=[{"label": i, "value": i} for i in
                                                     init_bar_chart],
                                            placeholder="Pilih Metrik Analisis",
                                        ),
                                    ],
                                    className="card-body-ketzil",
                                ),
                            ],
                            style={"margin-top": "27px"}
                        ),
                        dbc.Card(
                            [
                                # dbc.CardHeader("Pilih Provinsi"),
                                dbc.CardBody(
                                    [
                                        dcc.Loading(
                                            children=dcc.Graph(
                                                id="bar-chart-detail",
                                                style={"margin-right": "10px", "margin-left": "10px",
                                                       "margin-bottom": "1rem"},
                                                figure={
                                                    "data": [],
                                                    "layout": dict(
                                                        plot_bgcolor='rgba(0,0,0,0)',
                                                        paper_bgcolor='rgba(0,0,0,0)',
                                                    ),
                                                },
                                                config={
                                                    'doubleClickDelay': 1000,
                                                    'showTips': False,
                                                },
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                            style={
                                "margin-top": 15,
                            },
                        ),
                        dbc.Card(
                            [
                                # dbc.CardHeader("Pilih Provinsi"),
                                dbc.CardBody(
                                    [
                                        dcc.Loading(
                                            children=html.Div(
                                                id="table-container-detail",
                                            )
                                        ),
                                    ],
                                ),
                            ],
                            style={
                                "margin-top": 15,
                            },
                            className="scroll_table",
                        ),
                    ],
                    width={"size": 9, "order": 1},
                ),
                dbc.Col(
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "a token of remembrance",
                                    style={"padding-left": "0px", "text-align": "center", "font-weight": "bold"},
                                ),
                                dbc.CardBody(
                                    children=[
                                        html.Iframe(
                                            width="100%",
                                            height=270,
                                            src="https://www.youtube.com/embed/AhIkV-it9rE",
                                            # type="video/mp4"
                                            # frameborder="0",
                                            #allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope;"
                                            #       " picture-in-picture; allowfullscreen"
                                            # sandbox="allow-presentation"
                                        ),
                                    ],
                                    style={
                                        "padding-left": 2,
                                        "padding-right": 2,
                                        "padding-top": 2,
                                        "padding-bottom": 0,
                                    },
                                ),
                            ],
                            className="btn-outline-warning",
                            # style={
                            #     "padding-left": 1,
                            #     "padding-right": 1,
                            #     "padding-top": 1,
                            #     "padding-bottom": 1,
                            # },
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "PROVINSI",
                                    style={"padding-left": "0px", "text-align": "center"},
                                ),
                                dbc.CardBody(
                                    children=[
                                        html.Div(
                                            id="state-checklist-container",
                                            children=dcc.Checklist(
                                                id="state-select-all",
                                                options=[{"label": " Pilih Semua Provinsi", "value": "All"}],
                                                value=[],
                                            ),
                                        ),
                                        dcc.Dropdown(
                                            id="state-select", multi=True, searchable=True,
                                            options=[{"label": i, "value": i} for i in sorted(init_state)],
                                            value=[],
                                            placeholder="Pilih Provinsi",
                                            style={"color": "black"},
                                        ),
                                    ],
                                ),
                            ],
                            style={
                                # "padding-left": 7,
                                # "padding-right": 7,
                                "margin-top": 22,
                                # "padding-bottom": 7,
                            },
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "KABUPATEN/KOTA",
                                    style={"padding-left": "0px", "text-align": "center"},
                                ),
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            id="checklist-container",
                                            children=dcc.Checklist(
                                                id="region-select-all",
                                                options=[{"label": " Pilih Semua Kabupaten/Kota", "value": "All"}],
                                                value=[],
                                            ),
                                        ),
                                        dcc.Dropdown(
                                            id="region-select", multi=True, searchable=True,
                                            value=[],
                                            placeholder="Pilih Kabupaten/Kota",
                                            style={
                                                'color': 'black',
                                                # 'background-color': '#212121'
                                            },
                                        ),
                                    ],
                                ),
                            ],
                            style={
                                # "padding-left": 7,
                                # "padding-right": 7,
                                "margin-top": 15,
                                # "padding-bottom": 7,
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    "enam derajat lintang utara sampai sebelas derajat lintang selatan dan "
                                    "sembilan puluh lima derajat bujur timur sampai "
                                    "seratus empat puluh satu derajat bujur timur",
                                    id="pesan_sponsor",
                                    className="text-success text-justify",
                                ),
                                html.Div(
                                    "Indonesia",
                                    id="pesan_sponsor_2",
                                    className="text-success text-right blockquote-footer",
                                ),
                            ],
                            style={
                                # "padding-left": 7,
                                # "padding-right": 7,
                                "margin-top": 27,
                                "font-style": "italic",
                            },
                        ),
                    ],
                    width={"size": 3, "order": 2},
                    style={"padding-left": "0px"},
                ),
            ],
            # no_gutters=True,
            style={"padding-top": "15px"},
            # className="col-md-6 col-lg-4 col-xl-3",
        ),
    ],
    fluid=True,
    # style={"width": True}
    # className="col-md-12",
)
)


# -----------------------------------------------------------------------------
@app.callback(
    [
        Output("state-select", "value"),
        Output("state-select", "options")
    ],
    [Input("state-select-all", "value")],
)
def update_state_dropdown(state_select_all):
    options = [{"label": i, "value": i} for i in sorted(init_state)]

    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"].split(".")[0] == "state-select-all":
        if state_select_all == ["All"]:
            value = [i["value"] for i in options]
        else:
            value = dash.no_update
    else:
        value = dash.no_update
    return (
        value,
        options,
    )


@app.callback(
    Output("state-checklist-container", "children"),
    [Input("state-select", "value")],
    [
        State("state-select", "options"),
        State("state-select-all", "value")
    ],
)
def state_update_checklist_state(selected, select_options, checked):
    if len(selected) < len(select_options) and len(checked) == 0:
        raise PreventUpdate()

    elif len(selected) < len(select_options) and len(checked) == 1:
        return dcc.Checklist(
            id="state-select-all",
            options=[{"label": " Pilih Semua Provinsi", "value": "All"}],
            value=[],
        )

    elif len(selected) == len(select_options) and len(checked) == 1:
        raise PreventUpdate()

    return dcc.Checklist(
        id="state-select-all",
        options=[{"label": " Pilih Semua Provinsi", "value": "All"}],

        value=["All"],
    )


@app.callback(
    [
        Output("region-select", "value"),
        Output("region-select", "options"),
    ],
    [
        Input("region-select-all", "value"),
        Input("state-select", "value")
    ],
    [
        State("region-select", "value"),
        State("region-select", "options"),
    ],
)
def update_region_dropdown(select_all, state_select, region_select_value, region_select_options):
    filtered_state = df[
        df["PROVINSI"].isin(state_select)
    ]
    state_raw_data = filtered_state
    regions = state_raw_data["KABUPATEN/KOTA"].unique()
    options = [{"label": i, "value": i} for i in sorted(regions)]

    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"].split(".")[0] == "region-select-all":
        if select_all == ["All"]:
            value = [i["value"] for i in options]
        else:
            value = dash.no_update
    elif ctx.triggered[0]["prop_id"].split(".")[0] == "state-select":
        if select_all == ["All"]:
            if len(region_select_value) < len(options):
                value = dash.no_update
            else:
                value = [i["value"] for i in options]
        else:
            value = dash.no_update
    else:
        value = dash.no_update
    return (
        value,
        options
    )


@app.callback(
    Output("checklist-container", "children"),
    [
        Input("region-select", "value"),
        Input("state-select", "value"),
    ],
    [
        State("region-select", "options"),
        State("region-select-all", "value"),
        State("state-select", "options"),
        State("state-select-all", "value")
    ],
)
def update_checklist(selected, state_select_value, select_options, checked, state_select_options,
                     state_select_all):
    if len(selected) > len(select_options):
        return dcc.Checklist(
            id="region-select-all",
            options=[{"label": " Pilih semua Kabupaten/Kota", "value": "All"}],
            value=[],
        )

    elif len(selected) < len(select_options) and len(checked) == 0:
        raise PreventUpdate()

    elif len(selected) < len(select_options) and len(checked) == 1:
        return dcc.Checklist(
            id="region-select-all",
            options=[{"label": " Pilih semua Kabupaten/Kota", "value": "All"}],
            value=[],
        )

    elif len(selected) == len(select_options) and len(selected) == 0:
        ctx = dash.callback_context
        if ctx.triggered[0]["prop_id"].split(".")[0] == "state-select":
            return dcc.Checklist(
                id="region-select-all",
                options=[{"label": " Pilih semua Kabupaten/Kota", "value": "All"}],
                value=[],
            )
        else:
            raise PreventUpdate()

    return dcc.Checklist(
        id="region-select-all",
        options=[{"label": " Pilih Semua Kabupaten/Kota", "value": "All"}],
        value=["All"],
    )


@app.callback(
    [
        Output("geo-map", "figure"),
        Output("geo-map", "selectedData"),
    ],
    [
        Input("state-select", "value"),
        Input("region-select", "value"),
        Input("map-style-select", "value"),
        Input("map-filter-options", "value")
    ],
    [
        State("geo-map", "relayoutData"),
        State("geo-map", "selectedData"),
    ]
)
def update_geo_map(state_select, region_select, map_style_select, map_filter_options,
                   dont_touch_my_map, dont_touch_my_map_2):
    filtered_state = df[df["PROVINSI"].isin(state_select)]
    state_raw_data = filtered_state

    list_ketersediaan_all = [0, 1]

    filtered_data = state_raw_data[state_raw_data["KABUPATEN/KOTA"].isin(region_select)]
    filtered_data_2 = filtered_data[filtered_data["KETERSEDIAAN"].isin(list_ketersediaan_all)]

    colors = ["#0000ff", "#ffffff", "#76f2ff", "#ff6969", "#ff1717"]

    if map_style_select == "Satellite":
        style_map = 'mapbox://styles/hana001/ckh6y1yk81p5j19qqy0qttvjc'
    elif map_style_select == "Calming Blue":
        style_map = 'mapbox://styles/hana001/ckgvpuoyf28xm19mrfq6649vn'
    elif map_style_select == "Simply Black":
        style_map = 'mapbox://styles/plotlymapbox/cjvppq1jl1ips1co3j12b9hex'
    elif map_style_select == "Terracota":
        style_map = 'mapbox://styles/hana001/ckh6ytyd801u319o2bz13n4k2'
    elif map_style_select == "Icy Cold":
        style_map = 'mapbox://styles/hana001/ckgvmqyss0z4o19lhu8bg2n3q'
    elif map_style_select == "Disco Night":
        style_map = 'mapbox://styles/hana001/ckgxfdyxg23gx1ar58u4mkuf6'
    elif map_style_select == "Outdoor Play":
        style_map = 'mapbox://styles/hana001/ckh6yg9at0hha19pcazzlkd9j'
    else:
        style_map = 'mapbox://styles/hana001/ckh6yg9at0hha19pcazzlkd9j'

    latitude = []
    longitude = []
    st_key_id_2 = []
    color_diff = []
    hover_text = []

    if map_filter_options == "- 1 - Semua Wilayah : Kosong & Terisi":
        filtered_data_2_copywkwkwk = filtered_data_2.copy()
        for i in filtered_data_2_copywkwkwk["KETERSEDIAAN"].index:
            if filtered_data_2_copywkwkwk["KETERSEDIAAN"][i] == 0:
                latitude.append(filtered_data_2_copywkwkwk["ST_LAT"][i])
                longitude.append(filtered_data_2_copywkwkwk["ST_LONG"][i])
                st_key_id_2.append(filtered_data_2_copywkwkwk["ST_KEY_ID_2"][i])
                provinsi = str(filtered_data_2_copywkwkwk["PROVINSI"][i])
                kabkot = str(filtered_data_2_copywkwkwk["KABUPATEN/KOTA"][i])
                if not math.isnan(filtered_data_2_copywkwkwk["KANAL"][i]):
                    kanal = str(int(filtered_data_2_copywkwkwk["KANAL"][i]))
                else:
                    kanal = "-"
                if not math.isnan(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i]):
                    frekuensi = str(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i])
                else:
                    frekuensi = "-"
                if not filtered_data_2_copywkwkwk["NAMA STASIUN"][i]:
                    stasiun = "-"
                else:
                    stasiun = str(filtered_data_2_copywkwkwk["NAMA STASIUN"][i])
                hover_text.append("P : " + provinsi + "<br>" +
                                  "K : " + kabkot + "<br>" +
                                  "C : " + kanal + "<br>" +
                                  "F : " + frekuensi + "<br>" +
                                  "S : " + stasiun)
                color_diff.append(colors[0])
            elif filtered_data_2_copywkwkwk["KETERSEDIAAN"][i] == 1:
                latitude.append(filtered_data_2_copywkwkwk["PWL_LAT"][i])
                longitude.append(filtered_data_2_copywkwkwk["PWL_LONG"][i])
                st_key_id_2.append(filtered_data_2_copywkwkwk["ST_KEY_ID_2"][i])
                provinsi = str(filtered_data_2_copywkwkwk["PROVINSI"][i])
                kabkot = str(filtered_data_2_copywkwkwk["KABUPATEN/KOTA"][i])
                if not math.isnan(filtered_data_2_copywkwkwk["KANAL"][i]):
                    kanal = str(int(filtered_data_2_copywkwkwk["KANAL"][i]))
                else:
                    kanal = "-"
                if not math.isnan(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i]):
                    frekuensi = str(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i])
                else:
                    frekuensi = "-"
                if not filtered_data_2_copywkwkwk["NAMA STASIUN"][i]:
                    stasiun = str(filtered_data_2_copywkwkwk["NAMA STASIUN"][i])
                else:
                    stasiun = "-"
                hover_text.append("P : " + provinsi + "<br>" +
                                  "K : " + kabkot + "<br>" +
                                  "C : " + kanal + "<br>" +
                                  "F : " + frekuensi + "<br>" +
                                  "S : " + stasiun)
                color_diff.append(colors[1])

    elif map_filter_options == "- 2 - Semua Wilayah : Kosong":
        filtered_data_2 = filtered_data[filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])]
        filtered_data_2_copywkwkwk = filtered_data_2.copy()
        for i in filtered_data_2_copywkwkwk["KETERSEDIAAN"].index:
            latitude.append(filtered_data_2_copywkwkwk["PWL_LAT"][i])
            longitude.append(filtered_data_2_copywkwkwk["PWL_LONG"][i])
            st_key_id_2.append(filtered_data_2_copywkwkwk["ST_KEY_ID_2"][i])
            provinsi = str(filtered_data_2_copywkwkwk["PROVINSI"][i])
            kabkot = str(filtered_data_2_copywkwkwk["KABUPATEN/KOTA"][i])
            if not math.isnan(filtered_data_2_copywkwkwk["KANAL"][i]):
                kanal = str(int(filtered_data_2_copywkwkwk["KANAL"][i]))
            else:
                kanal = "-"
            if not math.isnan(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i]):
                frekuensi = str(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i])
            else:
                frekuensi = "-"
            if not filtered_data_2_copywkwkwk["NAMA STASIUN"][i]:
                stasiun = str(filtered_data_2_copywkwkwk["NAMA STASIUN"][i])
            else:
                stasiun = "-"
            hover_text.append("P : " + provinsi + "<br>" +
                              "K : " + kabkot + "<br>" +
                              "C : " + kanal + "<br>" +
                              "F : " + frekuensi + "<br>" +
                              "S : " + stasiun)
            color_diff.append(colors[1])

    elif map_filter_options == "- 3 - Semua Wilayah : Terisi":
        filtered_data_2 = filtered_data[filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])]
        filtered_data_2_copywkwkwk = filtered_data_2.copy()
        for i in filtered_data_2_copywkwkwk["KETERSEDIAAN"].index:
            latitude.append(filtered_data_2_copywkwkwk["ST_LAT"][i])
            longitude.append(filtered_data_2_copywkwkwk["ST_LONG"][i])
            st_key_id_2.append(filtered_data_2_copywkwkwk["ST_KEY_ID_2"][i])
            provinsi = str(filtered_data_2_copywkwkwk["PROVINSI"][i])
            kabkot = str(filtered_data_2_copywkwkwk["KABUPATEN/KOTA"][i])
            if not math.isnan(filtered_data_2_copywkwkwk["KANAL"][i]):
                kanal = str(int(filtered_data_2_copywkwkwk["KANAL"][i]))
            else:
                kanal = "-"
            if not math.isnan(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i]):
                frekuensi = str(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i])
            else:
                frekuensi = "-"
            if not filtered_data_2_copywkwkwk["NAMA STASIUN"][i]:
                stasiun = "-"
            else:
                stasiun = str(filtered_data_2_copywkwkwk["NAMA STASIUN"][i])
            hover_text.append("P : " + provinsi + "<br>" +
                              "K : " + kabkot + "<br>" +
                              "C : " + kanal + "<br>" +
                              "F : " + frekuensi + "<br>" +
                              "S : " + stasiun)
            color_diff.append(colors[0])

    elif map_filter_options == "- 4 - Perbatasan : Kosong & Terisi":
        filtered_data_2 = filtered_data[filtered_data["KETERSEDIAAN"].isin(list_ketersediaan_all)]
        filtered_data_2 = filtered_data_2[filtered_data_2["PERBATASAN"].isin([1])]
        filtered_data_2_copywkwkwk = filtered_data_2.copy()
        for i in filtered_data_2_copywkwkwk["KETERSEDIAAN"].index:
            if filtered_data_2_copywkwkwk["KETERSEDIAAN"][i] == 0:
                latitude.append(filtered_data_2_copywkwkwk["ST_LAT"][i])
                longitude.append(filtered_data_2_copywkwkwk["ST_LONG"][i])
                st_key_id_2.append(filtered_data_2_copywkwkwk["ST_KEY_ID_2"][i])
                provinsi = str(filtered_data_2_copywkwkwk["PROVINSI"][i])
                kabkot = str(filtered_data_2_copywkwkwk["KABUPATEN/KOTA"][i])
                if not math.isnan(filtered_data_2_copywkwkwk["KANAL"][i]):
                    kanal = str(int(filtered_data_2_copywkwkwk["KANAL"][i]))
                else:
                    kanal = "-"
                if not math.isnan(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i]):
                    frekuensi = str(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i])
                else:
                    frekuensi = "-"
                if not filtered_data_2_copywkwkwk["NAMA STASIUN"][i]:
                    stasiun = "-"
                else:
                    stasiun = str(filtered_data_2_copywkwkwk["NAMA STASIUN"][i])
                hover_text.append("P : " + provinsi + "<br>" +
                                  "K : " + kabkot + "<br>" +
                                  "C : " + kanal + "<br>" +
                                  "F : " + frekuensi + "<br>" +
                                  "S : " + stasiun)
                color_diff.append(colors[0])
            elif filtered_data_2_copywkwkwk["KETERSEDIAAN"][i] == 1:
                latitude.append(filtered_data_2_copywkwkwk["PWL_LAT"][i])
                longitude.append(filtered_data_2_copywkwkwk["PWL_LONG"][i])
                st_key_id_2.append(filtered_data_2_copywkwkwk["ST_KEY_ID_2"][i])
                provinsi = str(filtered_data_2_copywkwkwk["PROVINSI"][i])
                kabkot = str(filtered_data_2_copywkwkwk["KABUPATEN/KOTA"][i])
                if not math.isnan(filtered_data_2_copywkwkwk["KANAL"][i]):
                    kanal = str(int(filtered_data_2_copywkwkwk["KANAL"][i]))
                else:
                    kanal = "-"
                if not math.isnan(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i]):
                    frekuensi = str(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i])
                else:
                    frekuensi = "-"
                if not filtered_data_2_copywkwkwk["NAMA STASIUN"][i]:
                    stasiun = str(filtered_data_2_copywkwkwk["NAMA STASIUN"][i])
                else:
                    stasiun = "-"
                hover_text.append("P : " + provinsi + "<br>" +
                                  "K : " + kabkot + "<br>" +
                                  "C : " + kanal + "<br>" +
                                  "F : " + frekuensi + "<br>" +
                                  "S : " + stasiun)
                color_diff.append(colors[1])

    elif map_filter_options == "- 5 - Perbatasan : Kosong":
        filtered_data_2 = filtered_data[filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])]
        filtered_data_2 = filtered_data_2[filtered_data_2["PERBATASAN"].isin([1])]
        filtered_data_2_copywkwkwk = filtered_data_2.copy()
        for i in filtered_data_2_copywkwkwk["KETERSEDIAAN"].index:
            latitude.append(filtered_data_2_copywkwkwk["PWL_LAT"][i])
            longitude.append(filtered_data_2_copywkwkwk["PWL_LONG"][i])
            st_key_id_2.append(filtered_data_2_copywkwkwk["ST_KEY_ID_2"][i])
            provinsi = str(filtered_data_2_copywkwkwk["PROVINSI"][i])
            kabkot = str(filtered_data_2_copywkwkwk["KABUPATEN/KOTA"][i])
            if not math.isnan(filtered_data_2_copywkwkwk["KANAL"][i]):
                kanal = str(int(filtered_data_2_copywkwkwk["KANAL"][i]))
            else:
                kanal = "-"
            if not math.isnan(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i]):
                frekuensi = str(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i])
            else:
                frekuensi = "-"
            if not filtered_data_2_copywkwkwk["NAMA STASIUN"][i]:
                stasiun = str(filtered_data_2_copywkwkwk["NAMA STASIUN"][i])
            else:
                stasiun = "-"
            hover_text.append("P : " + provinsi + "<br>" +
                              "K : " + kabkot + "<br>" +
                              "C : " + kanal + "<br>" +
                              "F : " + frekuensi + "<br>" +
                              "S : " + stasiun)
            color_diff.append(colors[1])

    elif map_filter_options == "- 6 - Perbatasan : Terisi":
        filtered_data_2 = filtered_data[filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])]
        filtered_data_2 = filtered_data_2[filtered_data_2["PERBATASAN"].isin([1])]
        filtered_data_2_copywkwkwk = filtered_data_2.copy()
        for i in filtered_data_2_copywkwkwk["KETERSEDIAAN"].index:
            latitude.append(filtered_data_2_copywkwkwk["ST_LAT"][i])
            longitude.append(filtered_data_2_copywkwkwk["ST_LONG"][i])
            st_key_id_2.append(filtered_data_2_copywkwkwk["ST_KEY_ID_2"][i])
            provinsi = str(filtered_data_2_copywkwkwk["PROVINSI"][i])
            kabkot = str(filtered_data_2_copywkwkwk["KABUPATEN/KOTA"][i])
            if not math.isnan(filtered_data_2_copywkwkwk["KANAL"][i]):
                kanal = str(int(filtered_data_2_copywkwkwk["KANAL"][i]))
            else:
                kanal = "-"
            if not math.isnan(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i]):
                frekuensi = str(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i])
            else:
                frekuensi = "-"
            if not filtered_data_2_copywkwkwk["NAMA STASIUN"][i]:
                stasiun = "-"
            else:
                stasiun = str(filtered_data_2_copywkwkwk["NAMA STASIUN"][i])
            hover_text.append("P : " + provinsi + "<br>" +
                              "K : " + kabkot + "<br>" +
                              "C : " + kanal + "<br>" +
                              "F : " + frekuensi + "<br>" +
                              "S : " + stasiun)
            color_diff.append(colors[0])

    else:
        filtered_data_2_copywkwkwk = filtered_data_2.copy()
        for i in filtered_data_2_copywkwkwk["KETERSEDIAAN"].index:
            if filtered_data_2_copywkwkwk["KETERSEDIAAN"][i] == 0:
                latitude.append(filtered_data_2_copywkwkwk["ST_LAT"][i])
                longitude.append(filtered_data_2_copywkwkwk["ST_LONG"][i])
                st_key_id_2.append(filtered_data_2_copywkwkwk["ST_KEY_ID_2"][i])
                provinsi = str(filtered_data_2_copywkwkwk["PROVINSI"][i])
                kabkot = str(filtered_data_2_copywkwkwk["KABUPATEN/KOTA"][i])
                if not math.isnan(filtered_data_2_copywkwkwk["KANAL"][i]):
                    kanal = str(int(filtered_data_2_copywkwkwk["KANAL"][i]))
                else:
                    kanal = "-"
                if not math.isnan(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i]):
                    frekuensi = str(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i])
                else:
                    frekuensi = "-"
                if not filtered_data_2_copywkwkwk["NAMA STASIUN"][i]:
                    stasiun = "-"
                else:
                    stasiun = str(filtered_data_2_copywkwkwk["NAMA STASIUN"][i])
                hover_text.append("P : " + provinsi + "<br>" +
                                  "K : " + kabkot + "<br>" +
                                  "C : " + kanal + "<br>" +
                                  "F : " + frekuensi + "<br>" +
                                  "S : " + stasiun)
                color_diff.append(colors[0])
            elif filtered_data_2_copywkwkwk["KETERSEDIAAN"][i] == 1:
                latitude.append(filtered_data_2_copywkwkwk["PWL_LAT"][i])
                longitude.append(filtered_data_2_copywkwkwk["PWL_LONG"][i])
                st_key_id_2.append(filtered_data_2_copywkwkwk["ST_KEY_ID_2"][i])
                provinsi = str(filtered_data_2_copywkwkwk["PROVINSI"][i])
                kabkot = str(filtered_data_2_copywkwkwk["KABUPATEN/KOTA"][i])
                if not math.isnan(filtered_data_2_copywkwkwk["KANAL"][i]):
                    kanal = str(int(filtered_data_2_copywkwkwk["KANAL"][i]))
                else:
                    kanal = "-"
                if not math.isnan(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i]):
                    frekuensi = str(filtered_data_2_copywkwkwk["FREKUENSI (MHz)"][i])
                else:
                    frekuensi = "-"
                if not filtered_data_2_copywkwkwk["NAMA STASIUN"][i]:
                    stasiun = str(filtered_data_2_copywkwkwk["NAMA STASIUN"][i])
                else:
                    stasiun = "-"
                hover_text.append("P : " + provinsi + "<br>" +
                                  "K : " + kabkot + "<br>" +
                                  "C : " + kanal + "<br>" +
                                  "F : " + frekuensi + "<br>" +
                                  "S : " + stasiun)
                color_diff.append(colors[1])

    # point_selection = []
    # if dont_touch_my_map_2 is not None:
    #     for point in dont_touch_my_map_2["points"]:
    #         point_selection.append(point["pointIndex"])

    radio_station = go.Figure(
        go.Scattermapbox(
            lat=latitude,
            lon=longitude,
            mode="markers",
            marker=dict(
                color=color_diff,
                size=6,
            ),
            selected=dict(marker={"color": "#ffff00"}),
            customdata=st_key_id_2,
            hoverinfo="text",
            text=hover_text,
        )
    )

    # enam derajat lintang utara sampai sebelas derajat lintang selatan dan
    # sembilan puluh lima derajat bujur timur sampai seratus empat puluh satu derajat bujur timur

    if not (not latitude and not longitude):
        enam = max(latitude)
        sebelas = min(latitude)
        sembilan_puluh_lima = min(longitude)
        seratus_empat_puluh_satu = max(longitude)
        center_map_lat = enam - (enam - sebelas) / 2
        center_map_long = seratus_empat_puluh_satu - (seratus_empat_puluh_satu - sembilan_puluh_lima) / 2
        zumba = 4.3
    else:
        center_map_lat = -2.600029
        center_map_long = 118.015776
        zumba = 4

    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "map-style-select" and dont_touch_my_map is not None:

            wistara = {'mapbox.bearing', 'mapbox.center', 'mapbox.pitch', 'mapbox.zoom'}

            gotcha = True

            for i in wistara:
                if not (i in dont_touch_my_map.keys()):
                    gotcha = False
                    break

            if gotcha:
                radio_station.update_layout(
                    margin=go.layout.Margin(l=10, r=10, t=10, b=10, pad=0),
                    clickmode="event+select",
                    hovermode="closest",
                    showlegend=False,
                    mapbox={
                        'accesstoken': mapbox_access_token,
                        'bearing': float(dont_touch_my_map['mapbox.bearing']),
                        'center': {'lat': float(dont_touch_my_map['mapbox.center']['lat']),
                                   'lon': float(dont_touch_my_map['mapbox.center']['lon'])},
                        'pitch': float(dont_touch_my_map['mapbox.pitch']),
                        'zoom': float(dont_touch_my_map['mapbox.zoom']),
                        'style': style_map,
                    },
                    height=550,
                )
                point_selection = []
                if dont_touch_my_map_2 is not None:
                    for point in dont_touch_my_map_2["points"]:
                        point_selection.append(point["pointIndex"])
                radio_station.update_traces(
                    selectedpoints=point_selection,
                )
            else:
                radio_station.update_layout(
                    margin=go.layout.Margin(l=10, r=10, t=10, b=10, pad=0),
                    clickmode="event+select",
                    hovermode="closest",
                    showlegend=False,
                    mapbox={
                        'accesstoken': mapbox_access_token,
                        'bearing': 0,
                        'center': {'lat': center_map_lat, 'lon': center_map_long},
                        'pitch': 5,
                        'zoom': zumba,
                        'style': style_map
                    },
                    height=550,
                )
        else:
            radio_station.update_layout(
                margin=go.layout.Margin(l=10, r=10, t=10, b=10, pad=0),
                clickmode="event+select",
                hovermode="closest",
                showlegend=False,
                mapbox={
                    'accesstoken': mapbox_access_token,
                    'bearing': 0,
                    'center': {'lat': center_map_lat, 'lon': center_map_long},
                    'pitch': 5,
                    'zoom': zumba,
                    'style': style_map
                },
                height=550,
            )
    else:
        radio_station.update_layout(
            margin=go.layout.Margin(l=10, r=10, t=10, b=10, pad=0),
            clickmode="event+select",
            hovermode="closest",
            showlegend=False,
            mapbox={
                'accesstoken': mapbox_access_token,
                'bearing': 0,
                'center': {'lat': center_map_lat, 'lon': center_map_long},
                'pitch': 5,
                'zoom': zumba,
                'style': style_map,
            },
            height=550,
        )

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "map-filter-options" and dont_touch_my_map_2 is not None:
            dont_touch_my_map_2 = None

    return radio_station, dont_touch_my_map_2


@app.callback(
    [
        Output("info_alokasi_kanal", "children"),
        Output("info_kanal_terisi", "children"),
        Output("info_kanal_kosong", "children"),
        Output("info_total_BHP", "children"),
        Output("article-state", "children"),
        Output("article-region", "children"),
    ],
    [
        Input("state-select", "value"),
        Input("region-select", "value"),
        Input("state-select-all", "value"),
        Input("map-filter-options", "value"),
    ],
)
def update_summary_text(state_select, region_select, state_select_all, map_filter_options):
    filtered_state = df[
        df["PROVINSI"].isin(state_select)
    ]
    filtered_data = filtered_state[
        filtered_state["KABUPATEN/KOTA"].isin(region_select)
    ]

    list_ketersediaan_all = [0, 1]

    #ctx = dash.callback_context
    #if ctx.triggered:
    #    prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
    #    if prop_id == "map-filter-options" and map_filter_options is not None:
    if map_filter_options == "- 1 - Semua Wilayah : Kosong & Terisi":
        filtered_data = filtered_data.copy()
    elif map_filter_options == "- 2 - Semua Wilayah : Kosong":
        filtered_data = filtered_data[filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])]
    elif map_filter_options == "- 3 - Semua Wilayah : Terisi":
        filtered_data = filtered_data[filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])]
    elif map_filter_options == "- 4 - Perbatasan : Kosong & Terisi":
        filtered_data = filtered_data[filtered_data["KETERSEDIAAN"].isin(list_ketersediaan_all)]
        filtered_data = filtered_data[filtered_data["PERBATASAN"].isin([1])]
    elif map_filter_options == "- 5 - Perbatasan : Kosong":
        filtered_data = filtered_data[filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])]
        filtered_data = filtered_data[filtered_data["PERBATASAN"].isin([1])]
    elif map_filter_options == "- 6 - Perbatasan : Terisi":
        filtered_data = filtered_data[filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])]
        filtered_data = filtered_data[filtered_data["PERBATASAN"].isin([1])]
    else:
        filtered_data = filtered_data.copy()

    filtered_state_selected = str(filtered_data["PROVINSI"].nunique())
    filtered_data_selected = str(filtered_data["KABUPATEN/KOTA"].nunique())

    filtered_data_terisi = 0
    filtered_data_kosong = 0
    filtered_data_bhp = 0

    for i in filtered_data["KETERSEDIAAN"]:
        if i == 0:
            filtered_data_terisi = filtered_data_terisi + 1
        elif i == 1:
            filtered_data_kosong = filtered_data_kosong + 1
        else:
            filtered_data_kosong = filtered_data_kosong
            filtered_data_terisi = filtered_data_terisi

    for i in filtered_data["BHP"]:
        if not math.isnan(i):
            filtered_data_bhp = filtered_data_bhp + i

    filtered_alokasi_kanal = len(filtered_data["KANAL"])

    return (
        filtered_alokasi_kanal,
        filtered_data_terisi,
        filtered_data_kosong,
        f"{int(filtered_data_bhp):,}",
        filtered_state_selected,
        filtered_data_selected,
    )


@app.callback(
    [
        Output("info_map_titik_terselect", "children"),
        Output("info_provinsi_terselect", "children"),
        Output("info_kab_kot_terselect", "children"),
        Output("info_kanal_terisi_terselect", "children"),
        Output("info_kanal_kosong_terselect", "children"),
        Output("info_bhp_terselect", "children"),
    ],
    [
        Input("map-filter-options", "value"),
        Input("geo-map", "selectedData"),
        Input("state-select", "value"),
        Input("region-select", "value"),

    ],
    [State("geo-map", "relayoutData")],
)
def update_summary_text_geo_select(map_filter_options, geo_select, state_select, region_select,
                                   dont_touch_my_map):
    filtered_state = df[df["PROVINSI"].isin(state_select)]
    filtered_data = filtered_state[filtered_state["KABUPATEN/KOTA"].isin(region_select)]
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "geo-map" and geo_select is not None:
            provider = []
            for point in geo_select["points"]:
                provider.append(point["customdata"])

            filtered_data_selection = filtered_data[filtered_data["ST_KEY_ID_2"].isin(provider)]
        else:
            filtered_data_selection = []
    else:
        filtered_data_selection = []

    info_kanal_terisi_terselect = 0
    info_kanal_kosong_terselect = 0
    info_bhp_terselect = 0
    info_map_titik_terselect = 0,
    info_provinsi_terselect = 0,
    info_kab_kot_terselect = 0,

    if len(filtered_data_selection):
        for i in filtered_data_selection["KETERSEDIAAN"]:
            if i == 0:
                info_kanal_terisi_terselect = info_kanal_terisi_terselect + 1
            elif i == 1:
                info_kanal_kosong_terselect = info_kanal_kosong_terselect + 1
            else:
                info_kanal_kosong_terselect = info_kanal_kosong_terselect
                info_kanal_terisi_terselect = info_kanal_terisi_terselect

        for i in filtered_data_selection["BHP"]:
            if not math.isnan(i):
                info_bhp_terselect = info_bhp_terselect + i

        info_map_titik_terselect = len(filtered_data_selection)
        info_provinsi_terselect = str(filtered_data_selection["PROVINSI"].nunique())
        info_kab_kot_terselect = str(filtered_data_selection["KABUPATEN/KOTA"].nunique())

    return (
        info_map_titik_terselect,
        info_provinsi_terselect,
        info_kab_kot_terselect,
        info_kanal_terisi_terselect,
        info_kanal_kosong_terselect,
        f"{int(info_bhp_terselect):,}"
    )


@app.callback(
    Output("bar-chart-detail", "figure"),
    [
        Input("state-select", "value"),
        Input("region-select", "value"),
        Input("geo-map", "selectedData"),
        Input("chart-select", "value"),
        Input("map-filter-options", "value"),
    ],
    [
        State("geo-map", "relayoutData"),
    ]
)
def update_bar_chart(state_select, region_select, geo_select, chart_select,
                     map_filter_options, dont_touch_my_map):
    filtered_state = df[
        df["PROVINSI"].isin(state_select)
    ]
    filtered_data = filtered_state[
        filtered_state["KABUPATEN/KOTA"].isin(region_select)
    ]

    filtered_data_all = filtered_data.copy()

    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if prop_id == "map-filter-options":
            list_ketersediaan_all = [0, 1]
            if map_filter_options == "- 1 - Semua Wilayah : Kosong & Terisi":
                filtered_data_all = filtered_data.copy()
            elif map_filter_options == "- 2 - Semua Wilayah : Kosong":
                filtered_data_all = filtered_data.copy()
                filtered_data_all = filtered_data_all[
                    filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])
                ]
            elif map_filter_options == "- 3 - Semua Wilayah : Terisi":
                filtered_data_all = filtered_data.copy()
                filtered_data_all = filtered_data_all[
                    filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])
                ]
            elif map_filter_options == "- 4 - Perbatasan : Kosong & Terisi":
                filtered_data_all = filtered_data.copy()
                filtered_data_all = filtered_data_all[filtered_data_all["KETERSEDIAAN"].isin(list_ketersediaan_all)]
                filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
            elif map_filter_options == "- 5 - Perbatasan : Kosong":
                filtered_data_all = filtered_data.copy()
                filtered_data_all = filtered_data_all[
                    filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])]
                filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
            elif map_filter_options == "- 6 - Perbatasan : Terisi":
                filtered_data_all = filtered_data.copy()
                filtered_data_all = filtered_data_all[
                    filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])]
                filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
            else:
                filtered_data_all = filtered_data.copy()

        elif prop_id == "geo-map":
            if geo_select is not None:
                prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
                provider = []
                for point in geo_select["points"]:
                    provider.append(point["customdata"])
                filtered_data_all = filtered_data[filtered_data["ST_KEY_ID_2"].isin(provider)]
            elif map_filter_options is not None:
                list_ketersediaan_all = [0, 1]
                if map_filter_options == "- 1 - Semua Wilayah : Kosong & Terisi":
                    filtered_data_all = filtered_data.copy()
                elif map_filter_options == "- 2 - Semua Wilayah : Kosong":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])
                    ]
                elif map_filter_options == "- 3 - Semua Wilayah : Terisi":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])
                    ]
                elif map_filter_options == "- 4 - Perbatasan : Kosong & Terisi":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin(list_ketersediaan_all)]
                    filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
                elif map_filter_options == "- 5 - Perbatasan : Kosong":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])]
                    filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
                elif map_filter_options == "- 6 - Perbatasan : Terisi":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])]
                    filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
                else:
                    filtered_data_all = filtered_data.copy()
            else:
                filtered_data_all = filtered_data.copy()

        elif prop_id == "chart-select":
            prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if geo_select is not None:
                provider = []
                for point in geo_select["points"]:
                    provider.append(point["customdata"])
                filtered_data_all = filtered_data[filtered_data["ST_KEY_ID_2"].isin(provider)]
            elif map_filter_options is not None:
                list_ketersediaan_all = [0, 1]
                if map_filter_options == "- 1 - Semua Wilayah : Kosong & Terisi":
                    filtered_data_all = filtered_data.copy()
                elif map_filter_options == "- 2 - Semua Wilayah : Kosong":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])
                    ]
                elif map_filter_options == "- 3 - Semua Wilayah : Terisi":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])
                    ]
                elif map_filter_options == "- 4 - Perbatasan : Kosong & Terisi":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin(list_ketersediaan_all)]
                    filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
                elif map_filter_options == "- 5 - Perbatasan : Kosong":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])]
                    filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
                elif map_filter_options == "- 6 - Perbatasan : Terisi":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])]
                    filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
                else:
                    filtered_data_all = filtered_data.copy()
            else:
                filtered_data_all = filtered_data.copy()

        elif prop_id == "region-select" or prop_id == "state-select":
            prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if geo_select is not None:
                provider = []
                for point in geo_select["points"]:
                    provider.append(point["customdata"])
                filtered_data_all = filtered_data[filtered_data["ST_KEY_ID_2"].isin(provider)]
            elif map_filter_options is not None:
                list_ketersediaan_all = [0, 1]
                if map_filter_options == "- 1 - Semua Wilayah : Kosong & Terisi":
                    filtered_data_all = filtered_data.copy()
                elif map_filter_options == "- 2 - Semua Wilayah : Kosong":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])
                    ]
                elif map_filter_options == "- 3 - Semua Wilayah : Terisi":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])
                    ]
                elif map_filter_options == "- 4 - Perbatasan : Kosong & Terisi":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin(list_ketersediaan_all)]
                    filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
                elif map_filter_options == "- 5 - Perbatasan : Kosong":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])]
                    filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
                elif map_filter_options == "- 6 - Perbatasan : Terisi":
                    filtered_data_all = filtered_data.copy()
                    filtered_data_all = filtered_data_all[
                        filtered_data_all["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])]
                    filtered_data_all = filtered_data_all[filtered_data_all["PERBATASAN"].isin([1])]
                else:
                    filtered_data_all = filtered_data.copy()
            else:
                filtered_data_all = filtered_data.copy()
        else:
            filtered_data_all = filtered_data.copy()
    else:
        filtered_data_all = filtered_data.copy()

    fig = go.Figure()

    # Start Building Charts here...

    # -1 - Sebaran Nilai BHP
    if chart_select == "- 1 - Sebaran Nilai BHP" or chart_select is None:
        filtered_data_2 = filtered_data_all[
            filtered_data_all["BHP"].notnull()
        ]
        fig.update_layout(
            title={
                'text': "- ANALISIS SEBARAN NILAI BHP -",
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Arial Courier New, monospace",
                size=12,
                color="Black"
            ),
            # xaxis=dict(title_text="Provinsi"),
            yaxis=dict(title_text="Nilai BHP"),
            barmode='stack',
            showlegend=False,
            clickmode='event+select',
            height=720,
            # responsive=True,
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=30,
                pad=0
            ),
        )

        pv = pd.pivot_table(
            filtered_data_2,
            index=['PROVINSI', 'KABUPATEN/KOTA'],
            # columns=['KABUPATEN/KOTA'],
            values=['BHP'],
            aggfunc=sum,
            # sorted=True,
            fill_value=0
        )

        if not pv.empty:
            # pv = pv.reindex(pv['BHP'].sort_values(ascending=True).index)
            pv = pv.sort_values(['PROVINSI', 'BHP'], ascending=[True, True])

        counter = 0
        for i in pv.index:
            stringcompare = pv.index[counter][0]
            # pw = pv[pv.index[counter][0].isin(stringcompare)]
            pw = filtered_data_2.query('PROVINSI == @stringcompare')
            # pw = pw.reindex(pw['BHP'].sort_values(ascending=False).index)
            total = pw["BHP"].sum()
            fig.add_trace(
                go.Bar(x=[pv.index[counter][0]], y=[pv['BHP'][counter]],
                       legendgroup=pv.index[counter][0],
                       name=pv.index[counter][1],
                       hovertemplate="<b>" + pv.index[counter][1] + "</b>" + "<br>" +
                                     "<br><b>BHP : </b>" + str(f"{(pv['BHP'][counter]):,}") + "<br><br>" +
                                     "<b>Total BHP di " + str(pv.index[counter][0]) + " :</b> " +
                                     str(f"{int(total):,}") + "<br><extra></extra>",
                       hoverlabel=dict(
                           bgcolor="white", ),
                       customdata=[pv.index[counter][1]],
                       )
            )
            counter = counter + 1

    # - 2 - Jumlah Alokasi Kanal
    elif chart_select == "- 2 - Jumlah Alokasi Kanal":
        filtered_data_2 = filtered_data_all.copy()
        fig.update_layout(
            title={
                'text': "- ANALISIS JUMLAH ALOKASI KANAL -",
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Arial Courier New, monospace",
                size=12,
                color="Black"
            ),
            xaxis=dict(title_text="Jumlah Alokasi Kanal"),
            yaxis=dict(categoryorder='total descending'),
            barmode='stack',
            showlegend=False,
            clickmode='event+select',
            height=720,
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=30,
                pad=0
            ),
        )

        pv = pd.pivot_table(
            filtered_data_2,
            index=['PROVINSI', 'KABUPATEN/KOTA'],
            # columns=['KETERSEDIAAN'],
            values=['KETERSEDIAAN'],
            aggfunc='count',
            # sorted=True,
            fill_value=0
        )

        if not pv.empty:
            # pv = pv.reindex(pv['BHP'].sort_values(ascending=True).index)
            pv = pv.sort_values(['PROVINSI', 'KETERSEDIAAN'], ascending=[True, True])

        counter = 0
        for i in pv.index:
            stringcompare = pv.index[counter][0]
            # pw = pv[pv.index[counter][0].isin(stringcompare)]
            pw = filtered_data_2.query('PROVINSI == @stringcompare')
            # pw = pw.reindex(pw['BHP'].sort_values(ascending=False).index)
            total = pw["KETERSEDIAAN"].count()
            fig.add_trace(
                go.Bar(x=[pv['KETERSEDIAAN'][counter]], y=[pv.index[counter][0]],
                       # go.Bar(x=[pv.index[counter][0]], y=[pv['BHP'][counter]],
                       legendgroup=pv.index[counter][0],
                       name=pv.index[counter][1],
                       hovertemplate="<b>" + pv.index[counter][1] + "</b>" +
                                     "<br><br>" + "<b>Alokasi Kanal : </b>" + str(
                           f"{(pv['KETERSEDIAAN'][counter]):,}") + "<br>"
                                     + "----------------------------------------------------" + "<br>" +
                                     "<b>Total Alokasi Kanal di " + str(pv.index[counter][0]) + " :</b> " +
                                     str(f"{int(total):,}") + "<br><extra></extra>",
                       hoverlabel=dict(
                           bgcolor="white", ),
                       customdata=[pv.index[counter][1]],
                       orientation='h',
                       )
            )
            counter = counter + 1

    # - 3 - Channel Vacancy
    elif chart_select == "- 3 - Ketersediaan Kanal":
        filtered_data_2 = filtered_data_all.copy()

        fig.update_layout(
            title={
                'text': "- ANALISIS CHANNEL VACANCY -",
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Arial Courier New, monospace",
                size=12,
                color="Black"
            ),
            xaxis=dict(categoryorder='category ascending'),
            yaxis=dict(title_text="Jumlah Kanal"),
            barmode='stack',
            showlegend=False,
            clickmode='event+select',
            height=720,
            # responsive=True,
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=30,
                pad=0
            ),
        )

        colors = ["#2A66DE", "#FFC32B"]
        filtered_data_2_terisi = filtered_data_2[filtered_data_2['KETERSEDIAAN'].isin([0])]
        filtered_data_2_kosong = filtered_data_2[filtered_data_2['KETERSEDIAAN'].isin([1])]

        pv_terisi = pd.pivot_table(
            filtered_data_2_terisi,
            index=['PROVINSI', 'KABUPATEN/KOTA'],
            # columns=['KABUPATEN/KOTA'],
            values=['KETERSEDIAAN'],
            aggfunc='count',
            # sorted=True,
            fill_value=0
        )
        pv_kosong = pd.pivot_table(
            filtered_data_2_kosong,
            index=['PROVINSI', 'KABUPATEN/KOTA'],
            # columns=['KABUPATEN/KOTA'],
            values=['KETERSEDIAAN'],
            aggfunc='count',
            # sorted=True,
            fill_value=0
        )

        if not pv_terisi.empty:
            pv_terisi = pv_terisi.sort_values(['PROVINSI', 'KETERSEDIAAN'], ascending=[True, True])
        if not pv_kosong.empty:
            pv_kosong = pv_kosong.sort_values(['PROVINSI', 'KETERSEDIAAN'], ascending=[True, True])
        pv = pv_terisi.append(pv_kosong)
        if not pv.empty:
            pv = pv.sort_values(['PROVINSI', 'KABUPATEN/KOTA'], ascending=[True, True])

        counter = 0
        for i in pv_terisi.index:
            stringcompare = pv_terisi.index[counter][0]
            stringcompare_2 = pv_terisi.index[counter][1]
            # pw = pv[pv.index[counter][0].isin(stringcompare)]
            pw = filtered_data_2[filtered_data_2['PROVINSI'] == stringcompare]
            px = pw[pw['KABUPATEN/KOTA'] == stringcompare_2]
            # pw = pw.reindex(pw['BHP'].sort_values(ascending=False).index)
            total = px["KETERSEDIAAN"].count()
            # total_prov = pw["KETERSEDIAAN"].count()
            total_terisi_prov = pw["KETERSEDIAAN"].count() - pw["KETERSEDIAAN"].sum()
            fig.add_trace(
                go.Bar(x=[pv_terisi.index[counter][0] + " - TERISI"], y=[pv_terisi['KETERSEDIAAN'][counter]],
                       legendgroup=pv_terisi.index[counter][0],
                       name=pv_terisi.index[counter][1],
                       hovertemplate="<b>" + pv_terisi.index[counter][1] + "</b><br><br>" +
                                     "<b>Kanal Terisi : </b>" + str(f"{(pv_terisi['KETERSEDIAAN'][counter]):,}") +
                                     "<br>" +
                                     "<b>Jumlah Alokasi : </b>" + str(f"{int(total):,}") + "<br>" +
                                     "----------------------------------------------------" + "<br>" +
                                     "<b>Total Kanal Terisi di " +
                                     str(pv_terisi.index[counter][0]) + " :</b> " + str(int(total_terisi_prov)) +
                                     # "<b>Total Alokasi Kanal di Provinsi : </b>" + str(f"{int(total_prov):,}") +
                                     "<br><extra></extra>",
                       hoverlabel=dict(
                           bgcolor="white", ),
                       customdata=[pv_terisi.index[counter][1]],
                       )
            )
            counter = counter + 1
        counter = 0
        for i in pv_kosong.index:
            stringcompare = pv_kosong.index[counter][0]
            stringcompare_2 = pv_kosong.index[counter][1]
            # pw = pv[pv.index[counter][0].isin(stringcompare)]
            pw = filtered_data_2[filtered_data_2['PROVINSI'] == stringcompare]
            px = pw[pw['KABUPATEN/KOTA'] == stringcompare_2]
            # pw = pw.reindex(pw['BHP'].sort_values(ascending=False).index)
            total = px["KETERSEDIAAN"].count()
            # total_prov = pw["KETERSEDIAAN"].count()
            total_kosong_prov = pw["KETERSEDIAAN"].sum()
            fig.add_trace(
                go.Bar(x=[pv_kosong.index[counter][0] + " - KOSONG"], y=[pv_kosong['KETERSEDIAAN'][counter]],
                       legendgroup=pv_kosong.index[counter][0],
                       name=pv_kosong.index[counter][1],
                       hovertemplate="<b>" + pv_kosong.index[counter][1] + "</b><br><br>" +
                                     "<b>Kanal Kosong : </b>" + str(f"{(pv_kosong['KETERSEDIAAN'][counter]):,}") +
                                     "<br>" +
                                     "<b>Jumlah Alokasi : </b>" + str(f"{int(total):,}") + "<br>" +
                                     "----------------------------------------------------" + "<br>" +
                                     "<b>Total Kanal Kosong di " +
                                     str(pv_kosong.index[counter][0]) + " :</b> " + str(int(total_kosong_prov)) +
                                     # "<b>Total Alokasi Kanal di Provinsi : </b>" + str(f"{int(total_prov):,}") +
                                     "<br><extra></extra>",
                       hoverlabel=dict(
                           bgcolor="white", ),
                       customdata=[pv_kosong.index[counter][1]],
                       )
            )
            counter = counter + 1

    # - 4 - Umur ISR
    elif chart_select == "- 4 - Sebaran Umur ISR":
        filtered_data_2 = filtered_data_all[
            filtered_data_all["UMUR_ISR"].notnull()
        ]
        fig.update_layout(
            title={
                'text': "- ANALISIS SEBARAN UMUR ISR -",
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Arial Courier New, monospace",
                size=13,
                color="Black"
            ),
            xaxis=dict(categoryorder='category ascending'),
            yaxis=dict(title_text="Sebaran Umur ISR"),
            clickmode='event+select',
            showlegend=True,
            height=720,
            # paper_bgcolor='rgb(243, 243, 243)',
            # plot_bgcolor='rgb(243, 243, 243)',
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=30,
                pad=0
            ),
        )

        pw = filtered_data_2.groupby('UMUR_ISR').size()

        pw_data = pd.DataFrame(pw, columns=['Jumlah'])

        data_chart_hover = "<b>Umur ISR: </b>" + pw_data.index.map(int).map(str) + " Tahun" + "<br><br>" + \
                           "<b>Jumlah Stasiun Radio: </b>" + pw_data['Jumlah'].map(str) + \
                           "<br><extra></extra>"

        data_hover = pd.DataFrame(data_chart_hover, columns=['Hover'])

        fig.add_trace(go.Pie(
            labels=[str(int(h)) + " Tahun" for h in pw.index.values],
            values=pw.values,
            insidetextorientation='auto',
            customdata=pw.index.values,
            textfont=dict(size=17),
            textinfo='label+percent',
            hovertemplate=data_hover['Hover'],
            sort=True,
            hoverlabel=dict(bgcolor="white"),
        ))

    # - 10 - Lama Waktu Perizinan
    elif chart_select == "- 10 - Lama Waktu Perizinan":
        # filtered_data_2 = filtered_data_all.copy()
        filtered_data_2 = filtered_data_all[filtered_data_all["APPL_DATE"].notnull()]
        filtered_data_2 = filtered_data_2[filtered_data_2["LICENCE_DATE"].notnull()]

        fig.update_layout(
            title={
                'text': "- ANALISIS LAMA WAKTU PERIZINAN -",
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Arial Courier New, monospace",
                size=12,
                color="Black"
            ),
            xaxis=dict(title_text="Tanggal Pengajuan Aplikasi"),
            yaxis=dict(title_text="Lama Perizinan (Hari)"),
            clickmode='event+select',
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=30,
                pad=0
            ),
            height=720,
        )

        difference = []
        year = []
        month = []
        day = []
        for i, j in zip(filtered_data_2["APPL_DATE"].values, filtered_data_2["LICENCE_DATE"].values):
            applied = dt.datetime.strptime(i, '%d-%b-%y')
            year.append(applied.year)
            month.append(applied.month)
            day.append(applied.day)
            licensed = dt.datetime.strptime(j, '%d-%b-%y')
            differencenya = licensed - applied
            difference.append(differencenya.days)

        list_of_tuples = list(
            zip(
                filtered_data_2["NAMA STASIUN"].values,
                filtered_data_2["APPL_DATE"].values,
                filtered_data_2["LICENCE_DATE"].values,
                filtered_data_2["ST_KEY_ID_2"].values,
                year,
                month,
                day,
                difference
            )
        )

        data_line_chart = pd.DataFrame(
            list_of_tuples, columns=['Nama Stasiun', 'Applied', 'Licensed', 'ST_KEY_ID_2', 'Year',
                                     'Month', 'Day', 'Length'])

        if not data_line_chart.empty:
            data_line_chart = data_line_chart.sort_values(['Year', 'Month', 'Day'], ascending=[True, True, True])

        data_line_chart_x_axis = data_line_chart['Day'].map(str) + "-" + data_line_chart['Month'].map(str) + "-" + \
                                 data_line_chart['Year'].map(str)

        data_line_chart_hover = "<b>" + data_line_chart['Nama Stasiun'].map(str) + "</b><br><br>" + \
                                "<b>" + data_line_chart['Length'].map(str) + "</b>" + " Hari" + "<br><extra></extra>"

        data_line_chart_x_axis = pd.DataFrame(data_line_chart_x_axis, columns=['Tanggal'])

        data_line_chart_hover = pd.DataFrame(data_line_chart_hover, columns=['Hover'])

        the_x_axis = data_line_chart_x_axis['Tanggal'].values
        the_y_axis = data_line_chart['Length'].values
        the_custom_data = data_line_chart['ST_KEY_ID_2'].values
        the_hover_data = data_line_chart_hover['Hover'].values

        fig.add_trace(go.Scatter(
            x=the_x_axis,
            y=the_y_axis,
            mode='lines+markers',
            customdata=the_custom_data,
            hovertemplate=the_hover_data,
            hoverlabel=dict(bgcolor="white"),
            marker=dict(
                color='orange',
                size=7,
            ),
            line=dict(color='mediumblue', width=2),
        ))

    # - 5 - ERP Power vs Antenna Height
    elif chart_select == "- 5 - ERP Power vs Antenna Height":
        filtered_data_2 = filtered_data_all[filtered_data_all["KETERSEDIAAN"].isin([0])]
        filtered_data_2 = filtered_data_2[filtered_data_2["ERP_PWR_DBM"].notnull()]
        filtered_data_2 = filtered_data_2[filtered_data_2["HGT_ANT"].notnull()]

        fig.update_layout(
            title={
                'text': "- ANALISIS ERP vs Antenna Height -",
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Arial Courier New, monospace",
                size=13,
                color="Black"
            ),
            xaxis=dict(
                title='Tinggi Antena (Meter)',
                gridcolor='white',
                type='log',
                # gridwidth=0,
            ),
            yaxis=dict(
                title='ERP (dBm)',
                gridcolor='white',
                # gridwidth=1,
            ),
            clickmode='event+select',
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=30,
                pad=0
            ),
            height=720,
            # paper_bgcolor='rgb(243, 243, 243)',
            # plot_bgcolor='rgb(243, 243, 243)',
        )

        data_chart_hover = "<b>" + filtered_data_2['NAMA STASIUN'].map(str) + "</b><br><br>" + \
                           "<b>ERP: </b>" + filtered_data_2['ERP_PWR_DBM'].map(str) + " dBm" + \
                           "<br><b>Tinggi Antena: </b>" + filtered_data_2['HGT_ANT'].map(int).map(str) + " Meter" + \
                           "<br><extra></extra>"

        data_hover = pd.DataFrame(data_chart_hover, columns=['Hover'])

        fig.add_trace(go.Scatter(
            x=filtered_data_2['HGT_ANT'].values,
            y=filtered_data_2['ERP_PWR_DBM'].values,
            mode='markers',
            customdata=filtered_data_2['ST_KEY_ID_2'].values,
            hovertemplate=data_hover['Hover'],
            hoverlabel=dict(bgcolor="white"),
            marker=dict(
                color='red',
                size=12,
                sizemode='area',
            ),
        ))

    # - 8 - ERP Power vs Tinggi Antena vs Tinggi ASL
    elif chart_select == "- 8 - ERP Power vs Tinggi Antena vs Tinggi ASL":
        filtered_data_2 = filtered_data_all[filtered_data_all["ERP_PWR_DBM"].notnull()]
        filtered_data_2 = filtered_data_2[filtered_data_2["HGT_ANT"].notnull()]
        filtered_data_2 = filtered_data_2[filtered_data_2["H_ASL"].notnull()]

        fig.update_layout(
            title={
                'text': "- ANALISIS ERP Power vs Tinggi Antena vs Tinggi ASL -",
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Arial Courier New, monospace",
                size=12,
                color="Black"
            ),
            xaxis=dict(
                title='Tinggi Antena (Meter)',
                gridcolor='white',
                type='log',
                # gridwidth=0,
            ),
            yaxis=dict(
                title='ERP (dBm)',
                gridcolor='white',
                # gridwidth=1,
            ),
            clickmode='event+select',
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=30,
                pad=0
            ),
            height=720,
        )

        data_chart_hover = "<b>" + filtered_data_2['NAMA STASIUN'].map(str) + "</b><br><br>" + \
                           "<b>ERP: </b>" + filtered_data_2['ERP_PWR_DBM'].map(str) + " dBm" + \
                           "<br><b>Tinggi Antena: </b>" + filtered_data_2['HGT_ANT'].map(int).map(str) + " Meter" + \
                           "<br><b>Tinggi ASL: </b>" + filtered_data_2['H_ASL'].map(int).map(str) + " Meter" + \
                           "<br><extra></extra>"

        data_hover = pd.DataFrame(data_chart_hover, columns=['Hover'])

        fig.add_trace(go.Scatter(
            x=filtered_data_2['HGT_ANT'].values,
            y=filtered_data_2['ERP_PWR_DBM'].values,
            marker_size=filtered_data_2['H_ASL'].values,
            mode='markers',
            marker=dict(sizemode='area', line_width=3),
            customdata=filtered_data_2['ST_KEY_ID_2'].values,
            hovertemplate=data_hover['Hover'],
            hoverlabel=dict(bgcolor="white"),
        ))

    # - 9 - Tinggi ASL vs Tinggi Antena
    elif chart_select == "- 9 - Tinggi ASL vs Tinggi Antena":
        filtered_data_2 = filtered_data_all[filtered_data_all["HGT_ANT"].notnull()]
        filtered_data_2 = filtered_data_2[filtered_data_2["H_ASL"].notnull()]

        fig.update_layout(
            title={
                'text': "- ANALISIS Tinggi ASL vs Tinggi Antena -",
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Arial Courier New, monospace",
                size=12,
                color="Black"
            ),
            xaxis=dict(
                title='Tinggi ASL (Meter)',
                gridcolor='white',
                type='log',
                # gridwidth=0,
            ),
            yaxis=dict(
                title='Tinggi Antena (Meter)',
                gridcolor='white',
                # gridwidth=1,
            ),
            clickmode='event+select',
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=30,
                pad=0
            ),
            height=720,
        )

        data_chart_hover = "<b>" + filtered_data_2['NAMA STASIUN'].map(str) + "</b><br>" + \
                           "<br><b>Tinggi Antena: </b>" + filtered_data_2['HGT_ANT'].map(int).map(str) + " Meter" + \
                           "<br><b>Tinggi ASL: </b>" + filtered_data_2['H_ASL'].map(int).map(str) + " Meter" + \
                           "<br><extra></extra>"

        data_hover = pd.DataFrame(data_chart_hover, columns=['Hover'])

        fig.add_trace(go.Scatter(
            x=filtered_data_2['H_ASL'].values,
            y=filtered_data_2['HGT_ANT'].values,
            # marker_size=filtered_data_2['H_ASL'].values,
            mode='markers',
            marker=dict(
                color='#bcbd22',
                size=12,
                line=dict(
                    color='#d62728',
                    width=1
                ),
            ),
            customdata=filtered_data_2['ST_KEY_ID_2'].values,
            hovertemplate=data_hover['Hover'],
            hoverlabel=dict(bgcolor="white"),
        ))

    # - 6 - ERP Power vs Antenna Model
    elif chart_select == "- 6 - ERP Power vs Antenna Model":
        filtered_data_2 = filtered_data_all[filtered_data_all["ERP_PWR_DBM"].notnull()]
        fig.update_layout(
            title={
                'text': "- ANALISIS ERP Power vs Model Antena -",
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Arial Courier New, monospace",
                size=12,
                color="Black"
            ),
            xaxis=dict(
                title='ERP (dBm))',
                gridcolor='white',
                type='log',
                # gridwidth=0,
            ),
            yaxis=dict(
                title='Model Antena',
                gridcolor='white',
                # gridwidth=1,
            ),
            clickmode='event+select',
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=30,
                pad=0
            ),
            height=720,
        )

        # dewa
        # filtered_data_2 = filtered_data_2.groupby(['ERP_PWR_DBM', 'ANT_MDL']).size().reset_index().groupby('ANT_MDL')[
        #    [0]].max()

        filtered_data_2 = filtered_data_2.groupby(['ERP_PWR_DBM', 'ANT_MDL']).size().reset_index()

        data_chart_hover = "<b>ERP: </b>" + filtered_data_2['ERP_PWR_DBM'].map(str) + " dBm" + \
                           "<br><b>Model Antena: </b>" + filtered_data_2['ANT_MDL'].map(str) + \
                           "<br><extra></extra>"

        data_hover = pd.DataFrame(data_chart_hover, columns=['Hover'])

        fig.add_trace(go.Scatter(
            x=filtered_data_2['ERP_PWR_DBM'].values,
            y=filtered_data_2['ANT_MDL'].values,
            mode='markers',
            marker=dict(color='yellow',
                size=filtered_data_2[0].values,
                sizeref=0.7,
                line=dict(
                    color='black',
                    width=2
            )),
            customdata=filtered_data_2,
            hovertemplate=data_hover['Hover'],
            hoverlabel=dict(bgcolor="white"),
        ))

    # - 7 - ERP Power vs Tinggi ASL
    elif chart_select == "- 7 - ERP Power vs Tinggi ASL":
        filtered_data_2 = filtered_data_all[filtered_data_all["KETERSEDIAAN"].isin([0])]
        filtered_data_2 = filtered_data_2[filtered_data_2["ERP_PWR_DBM"].notnull()]
        filtered_data_2 = filtered_data_2[filtered_data_2["H_ASL"].notnull()]

        fig.update_layout(
            title={
                'text': "- ANALISIS ERP Power vs Tinggi ASL -",
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Arial Courier New, monospace",
                size=13,
                color="Black"
            ),
            xaxis=dict(
                title='Tinggi ASL (Meter)',
                gridcolor='white',
                type='log',
                # gridwidth=0,
            ),
            yaxis=dict(
                title='ERP (dBm)',
                gridcolor='white',
                # gridwidth=1,
            ),
            clickmode='event+select',
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=30,
                pad=0
            ),
            height=720,
            paper_bgcolor='rgb(243, 243, 243)',
            plot_bgcolor='rgb(243, 243, 243)',
        )

        data_chart_hover = "<b>" + filtered_data_2['NAMA STASIUN'].map(str) + "</b><br><br>" + \
                           "<b>ERP: </b>" + filtered_data_2['ERP_PWR_DBM'].map(str) + " dBm" + \
                           "<br><b>Tinggi ASL: </b>" + filtered_data_2['H_ASL'].map(int).map(str) + " Meter" + \
                           "<br><extra></extra>"

        data_hover = pd.DataFrame(data_chart_hover, columns=['Hover'])

        fig.add_trace(go.Scatter(
            x=filtered_data_2['H_ASL'].values,
            y=filtered_data_2['ERP_PWR_DBM'].values,
            mode='markers',
            customdata=filtered_data_2['ST_KEY_ID_2'].values,
            hovertemplate=data_hover['Hover'],
            hoverlabel=dict(bgcolor="white"),
            marker=dict(
                color='#e377c2',
                size=12,
                line=dict(
                    color='#8c564b',
                    width=2
                ),
            ),
        ))

    # - 11 - Anomali PM 3 Tahun 2017
    elif chart_select == "- 11 - Anomali PM 3 Tahun 2017":
        the_labels = ["ANOMALI PM 3 Tahun 2017", "101", "102", "103", "104", "105", "106", "107", "108", "109",
                    "Koordinat latitude dan longitude Pusat Wilayah Layanan ADA, Wilayah Layanan TIDAK ADA",
                    "Pusat Wilayah Layanan ADA, Alokasi Kanal TIDAK ADA",
                    "Pusat Wilayah Layanan TIDAK ADA, Wilayah Layanan ADA, Alokasi Kanal ADA",
                    "Nama Kabupaten tidak konsisten antara Lampiran IV, V, VI",
                    "Nama Wilayah Layanan tidak konsisten antara Lampiran IV dan VI",
                    "Nama Wilayah Layanan ada di 2 kabupaten berbeda dengan koordinat berbeda, "
                    "dan tidak konsisten antara Lampiran IV dan VI",
                    "Pusat Wilayah Layanan ADA 2 dengan 2 koordinat berbeda, namun Alokasi Kanal SAMA/MENYATU",
                    "Latitude Pusat Wilayah Layanan KELIRU",
                    "Nama kabupaten tidak konsisten antara Lampiran IV dan VI"]

        the_parents = ["", "ANOMALI PM 3 Tahun 2017", "ANOMALI PM 3 Tahun 2017", "ANOMALI PM 3 Tahun 2017",
                     "ANOMALI PM 3 Tahun 2017", "ANOMALI PM 3 Tahun 2017", "ANOMALI PM 3 Tahun 2017",
                     "ANOMALI PM 3 Tahun 2017", "ANOMALI PM 3 Tahun 2017", "ANOMALI PM 3 Tahun 2017", "101",
                     "102", "103", "104", "105", "106", "107", "108", "109"]

        the_values = [72, 1, 22, 25, 6, 2, 2, 2, 9, 3, 0.5, 11, 12.5, 3, 1, 1, 1, 4.5, 1.5]

        the_custom_data = ["all", "101", "102", "103", "104", "105", "106", "107", "108", "109",
                           "101", "102", "103", "104", "105", "106", "107", "108", "109"]

        # data_chart_hover = the_values
        # data_hover = pd.DataFrame(data_chart_hover, columns=['Hover'])

        fig.add_trace(go.Sunburst(
            labels=the_labels,
            parents=the_parents,
            values=the_values,
            branchvalues="total",
            customdata=the_custom_data,
            #hovertemplate=data_hover['Hover'],
            hoverlabel=dict(bgcolor="white"),
            textfont=dict(
                family="Arial Courier New, monospace",
                size=16,
                color="Black"
            ),
        ))
        fig.update_layout(
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=30,
                pad=0
            ),
            font=dict(
                family="Arial Courier New, monospace",
                size=16,
                color="Black"
            ),
            height=720,
            paper_bgcolor='rgb(243, 243, 243)',
            plot_bgcolor='rgb(243, 243, 243)',
        )

    # Return selected chart
    return fig


@app.callback(
    Output("table-container-detail", "children"),
    [
        Input("geo-map", "selectedData"),
        Input("state-select", "value"),
        Input("region-select", "value"),
        Input("bar-chart-detail", "selectedData"),
        Input("map-filter-options", "value"),
        Input("bar-chart-detail", "clickData"),
        Input("chart-select", "value"),
    ]
)
def update_table_container(geo_select, state_select, region_select, bar_chart_select,
                           map_filter_options, bar_chart_click, chart_select):
    filtered_state = df[
        df["PROVINSI"].isin(state_select)
    ]
    filtered_data = filtered_state[
        filtered_state["KABUPATEN/KOTA"].isin(region_select)
    ]

    list_ketersediaan_all = [0, 1]
    if map_filter_options == "- 1 - Semua Wilayah : Kosong & Terisi":
        filtered_data = filtered_data.copy()
    if map_filter_options == "- 2 - Semua Wilayah : Kosong":
        filtered_data = filtered_data[
            filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])
        ]
    elif map_filter_options == "- 3 - Semua Wilayah : Terisi":
        filtered_data = filtered_data[
            filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])
        ]
    elif map_filter_options == "- 4 - Perbatasan : Kosong & Terisi":
        filtered_data = filtered_data[filtered_data["KETERSEDIAAN"].isin(list_ketersediaan_all)]
        filtered_data = filtered_data[filtered_data["PERBATASAN"].isin([1])]
    elif map_filter_options == "- 5 - Perbatasan : Kosong":
        filtered_data = filtered_data[
            filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[1]])]
        filtered_data = filtered_data[filtered_data["PERBATASAN"].isin([1])]
    elif map_filter_options == "- 6 - Perbatasan : Terisi":
        filtered_data = filtered_data[
            filtered_data["KETERSEDIAAN"].isin([list_ketersediaan_all[0]])]
        filtered_data = filtered_data[filtered_data["PERBATASAN"].isin([1])]
    else:
        filtered_data = filtered_data.copy()

    table_data_df = pd.DataFrame(data=filtered_data)
    data = table_data_df.to_dict("rows")
    # satu = pd.DataFrame(index=table_data_df.index, columns=table_data_df.columns)

    if geo_select is not None:
        dff = []
        provider = []
        for point in geo_select["points"]:
            provider.append(point["customdata"])
        dff.append((table_data_df[table_data_df["ST_KEY_ID_2"].isin(provider)]))
        for i in range(len(dff)):
            table_data_df = pd.DataFrame(dff[i])
            dua = table_data_df.to_dict("rows")
            data = dua

    geo_data_dict = {
        "PROVINSI": [],
        "KABUPATEN/KOTA": [],
        "WILAYAH LAYANAN": [],
        "KANAL": [],
        "FREKUENSI (MHz)": [],
        "KETERSEDIAAN": [],
        "PERBATASAN": [],
        "NAMA STASIUN": [],
        "BHP": [],
        "STATUS": [],
        "PWL_LAT": [],
        "PWL_LONG": [],
        "ST_LAT": [],
        "ST_LONG": [],
        "CALLSIGN": [],
        "KECAMATAN": [],
        "WIL. LAYANAN STASIUN": [],
        "APPL_DATE": [],
        "LICENCE_DATE": [],
        "MASA_LAKU": [],
        "UMUR_ISR": [],
        "EQ_MDL": [],
        "EQ_MFR": [],
        "ERP_PWR_DBM": [],
        "EQ_PWR": [],
        "ANT_MDL": [],
        "ANT_MFR": [],
        "EMIS_CLASS_1": [],
        "HGT_ANT": [],
        "H_ASL": [],
        "ZONA": [],
    }

    geo_data_dict_2 = {
        "ERROR CODE": [],
        "KATEGORI ERROR": [],
        "DESKRIPSI": [],
        "HALAMAN DI PM 3 -2017": [],
        "PROVINSI": [],
        "KABUPATEN/KOTA": [],
        "WILAYAH LAYANAN": [],
        "KANAL": [],
        "LONGITUDE PWL": [],
        "LATITUDE PWL": [],
    }

    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if prop_id == "chart-select" and chart_select == "- 11 - Anomali PM 3 Tahun 2017":
            # prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
            df_anomaly = pd.read_csv("Anomali_Permen.csv")
            table_data_df = pd.DataFrame(data=df_anomaly)
            data = table_data_df.to_dict("rows")

            return dash_table.DataTable(
                id="table-detail-data",
                # row=[{"name": i} for i in ],
                columns=[{"name": i, "id": i} for i in geo_data_dict_2.keys()],
                data=data,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                editable=False,
                page_size=20,
                style_as_list_view=False,
                style_header={"padding": "0px 5px", 'fontWeight': 'bold'},
                style_cell={'textAlign': 'left'},
                style_data_conditional=[
                                           {
                                               'if': {'row_index': 'odd'},
                                               'backgroundColor': 'rgb(248, 248, 248)',
                                           }
                                       ] + [
                                           {
                                               'if': {'column_id': h},
                                               'textAlign': 'center',
                                           } for h in ['HALAMAN DI PM 3 -2017']
                                       ] + [
                                           {
                                               'if': {'column_id': s},
                                               'textAlign': 'center',
                                           } for s in ['ERROR CODE']
                                       ],
            )

        elif prop_id == "chart-select":
            data = table_data_df.to_dict("rows")

        elif prop_id == "bar-chart-detail":
            prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if bar_chart_select is not None:
                if chart_select == "- 10 - Lama Waktu Perizinan" or \
                        chart_select == "- 5 - ERP Power vs Antenna Height" or \
                        chart_select == "- 8 - ERP Power vs Tinggi Antena vs Tinggi ASL" or \
                        chart_select == "- 9 - Tinggi ASL vs Tinggi Antena" or \
                        chart_select == "- 7 - ERP Power vs Tinggi ASL":
                    dff = []
                    provider = []
                    for point in bar_chart_select["points"]:
                        provider.append(point["customdata"])
                    dff.append((table_data_df[table_data_df["ST_KEY_ID_2"].isin(provider)]))
                    for i in range(len(dff)):
                        table_data_df = pd.DataFrame(dff[i])
                        dua = table_data_df.to_dict("rows")
                        data = dua
                elif chart_select == "- 6 - ERP Power vs Antenna Model":
                    dff = []
                    check1 = []
                    check2 = []
                    for point in bar_chart_select["points"]:
                        check1.append(point["customdata"][0])
                        check2.append(point["customdata"][1])
                    table_data_df = table_data_df[table_data_df['ERP_PWR_DBM'].isin(check1)]
                    table_data_df = table_data_df[table_data_df['ANT_MDL'].isin(check2)]
                    dff.append(table_data_df)
                    for i in range(len(dff)):
                        table_data_df = pd.DataFrame(dff[i])
                        dua = table_data_df.to_dict("rows")
                        data = dua
                elif chart_select == "- 3 - Ketersediaan Kanal":
                    provider = []
                    data = []
                    for point in bar_chart_select["points"]:
                        # provider.append(point["customdata"])
                        table_data_df_2 = table_data_df[table_data_df["KABUPATEN/KOTA"].isin([point["customdata"]])]
                        str_request = point["label"][-6:]
                        if str_request == "TERISI":
                            request_list = [0]
                        elif str_request == "KOSONG":
                            request_list = [1]
                        else:
                            request_list = [0,1]
                        table_data_df_2 = table_data_df_2[table_data_df_2["KETERSEDIAAN"].isin(request_list)]
                        provider.append(table_data_df_2)
                    for i in range(len(provider)):
                        table_data_df = pd.DataFrame(provider[i])
                        dua = table_data_df.to_dict("rows")
                        data = data + dua
                else:
                    dff = []
                    provider = []
                    for point in bar_chart_select["points"]:
                        provider.append(point["customdata"])
                    dff.append((table_data_df[table_data_df["KABUPATEN/KOTA"].isin(provider)]))
                    for i in range(len(dff)):
                        table_data_df = pd.DataFrame(dff[i])
                        dua = table_data_df.to_dict("rows")
                        data = dua
            elif bar_chart_click is not None and chart_select == "- 4 - Sebaran Umur ISR":
                dff = []
                provider = []
                for point in bar_chart_click["points"]:
                    provider.append(int(point["customdata"]))
                dff.append((table_data_df[table_data_df["UMUR_ISR"].isin(provider)]))
                for i in range(len(dff)):
                    table_data_df = pd.DataFrame(dff[i])
                    dua = table_data_df.to_dict("rows")
                    data = dua
            elif bar_chart_click is not None and chart_select == "- 11 - Anomali PM 3 Tahun 2017":
                df_anomaly = pd.read_csv("Anomali_Permen.csv")
                provider = []
                for point in bar_chart_click["points"]:
                    provider.append(point["customdata"])
                for switch_error_code in provider:
                    if switch_error_code == "all":
                        table_data_df = pd.DataFrame(data=df_anomaly)
                        data = table_data_df.to_dict("rows")
                    else:
                        df_anomaly_selected = df_anomaly[df_anomaly["ERROR CODE"].isin(provider)]
                        table_data_df = pd.DataFrame(data=df_anomaly_selected)
                        data = table_data_df.to_dict("rows")

                return dash_table.DataTable(
                    id="table-detail-data",
                    columns=[{"name": i, "id": i} for i in geo_data_dict_2.keys()],
                    data=data,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    editable=False,
                    page_size=20,
                    style_as_list_view=False,
                    style_header={"padding": "0px 5px", 'fontWeight': 'bold'},
                    style_cell={'textAlign': 'left'},
                    style_data_conditional=[
                                               {
                                                   'if': {'row_index': 'odd'},
                                                   'backgroundColor': 'rgb(248, 248, 248)',
                                               }
                                           ] + [
                                               {
                                                   'if': {'column_id': h},
                                                   'textAlign': 'center',
                                               } for h in ['HALAMAN DI PM 3 -2017']
                                           ] + [
                                               {
                                                   'if': {'column_id': s},
                                                   'textAlign': 'center',
                                               } for s in ['ERROR CODE']
                                           ],
                )
    else:
        data = [{}]

    return dash_table.DataTable(
        id="table-detail-data",
        # row=[{"name": i} for i in ],
        columns=[{"name": i, "id": i} for i in geo_data_dict.keys()],
        data=data,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        editable=False,
        page_size=20,
        style_as_list_view=False,
        style_header={"padding": "0px 5px", 'fontWeight': 'bold'},
        style_cell={'textAlign': 'left'},
        style_data_conditional=[
                                   {
                                       'if': {'row_index': 'odd'},
                                       'backgroundColor': 'rgb(248, 248, 248)',
                                   }
                               ] + [
                                   {
                                       'if': {'column_id': h},
                                       'textAlign': 'right',
                                   } for h in ['KANAL', 'FREKUENSI (MHz)']
                               ] + [
                                   {
                                       'if': {'column_id': s},
                                       'textAlign': 'center',
                                   } for s in ['KETERSEDIAAN', 'PERBATASAN', 'ZONA']
                               ],
    )


if __name__ == "__main__":
    app.run_server(debug=True)
