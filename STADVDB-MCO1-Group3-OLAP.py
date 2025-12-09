# Group 3 Members:

# ANG, Danielle Faith L.
# CAPIO, Simone Franceska Emanuelle M.

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import mysql.connector
import plotly.graph_objects as go
import pandas as pd

# Establish MySQL connection
# Kindly input your own settings
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Yalowi7(",
    database="gamesdata"
)

# Dash app setup
app = dash.Dash(__name__)

# Helper function to execute a query and return the results
def execute_query(query):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Fetch genres from the database
def get_genres():
    query = "SELECT DISTINCT genre FROM genres;"
    genres = execute_query(query)
    return [{'label': genre['genre'], 'value': genre['genre']} for genre in genres]

# Define the layout of the app
app.layout = html.Div([
    html.H1("Group 3's OLAP Dashboard"),

    # Dropdown for selecting the OLAP operation
    html.Label("Select an OLAP Operation:"),
    dcc.Dropdown(
        id='operation-dropdown',
        options=[
            {'label': 'Roll-Up', 'value': 'rollup'},
            {'label': 'Drill-Down', 'value': 'drilldown'},
            {'label': 'Slice', 'value': 'slice'},
            {'label': 'Dice', 'value': 'dice'}
        ],
        value='rollup',
        style={'margin-bottom': '15px'}
    ),

    # Dropdown for selecting the Query Type
    html.Label("Select Query Type:"),
    dcc.Dropdown(
        id='query-type-dropdown',
        options=[
            {'label': 'Basic Query', 'value': 'basic'},
            {'label': 'Optimized Query', 'value': 'optimized'}
        ],
        value='basic',
        multi=False,
        style={'margin-bottom': '15px'}
    ),

    # Dropdown for selecting a year (only used in drill-down, slice, and dice)
    html.Label("Filter by Year (Drill-down, Slice, Dice):"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in range(2010, 2025)],
        value=2023,
        multi=False,
        style={'margin-bottom': '15px'}
    ),

    # Dropdown for selecting genres (only used in slice and dice)
    html.Label("Filter by Genre (Slice, Dice):"),
    dcc.Dropdown(
        id='genre-dropdown',
        options=get_genres(),  # Get genres from the database
        value='Action',  # Set a default genre
        multi=False,
        style={'margin-bottom': '15px'}
    ),

    # Dropdown for selecting the platform supported (only used in dice)
    html.Label("Filter by Platform (Dice):"),
    dcc.Dropdown(
        id='platform-dropdown',
        options=[
            {'label': 'Windows', 'value': 'windows_support'},
            {'label': 'Mac', 'value': 'mac_support'},
            {'label': 'Linux', 'value': 'linux_support'}
        ],
        value='windows_support',
        style={'margin-bottom': '15px'}
    ),

    # Loading component around the graph container
    dcc.Loading(
        id="loading-overlay",
        type="default",  # Choose 'default' for spinner or 'dot' for dot animation
        children=html.Div(id='graph-container')
    )
])

# Callback to update the dropdowns' disabled state
@app.callback(
    [Output('year-dropdown', 'disabled'),
     Output('genre-dropdown', 'disabled'),
     Output('platform-dropdown', 'disabled')],
    [Input('operation-dropdown', 'value')]
)

def toggle_dropdowns(selected_operation):
    if selected_operation == 'rollup':
        return True, True, True
    elif selected_operation == 'drilldown':
        return False, True, True
    elif selected_operation == 'slice':
        return False, False, True
    elif selected_operation == 'dice':
        return False, False, False
    return True, True, True  # Default state if operation isn't selected

# Callback to update the graph based on the selected OLAP operation
@app.callback(
    Output('graph-container', 'children'),
    [Input('operation-dropdown', 'value'),
     Input('query-type-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('genre-dropdown', 'value'),
     Input('platform-dropdown', 'value')]
)

def update_graph(selected_operation, query_type, selected_year, selected_genre, selected_platform):
    if selected_operation == 'rollup':
        # Roll-Up: User Engagement by Genre
        if query_type == 'basic':
            # Basic Roll-Up Query
            query = """
            SELECT gnr.genre AS Genre, COUNT(g.game_id) AS Total_Games, AVG(g.average_playtime_forever) AS Avg_Playtime_Forever
            FROM games g
            JOIN game_genres gg ON g.game_id = gg.game_id
            JOIN genres gnr ON gg.gen_id = gnr.gen_id
            GROUP BY gnr.genre
            ORDER BY Avg_Playtime_Forever DESC;
            """
        else:
            # Optimized Roll-Up Query
            query = """
            WITH GenreCounts AS (
                SELECT
                    gg.gen_id,
                    COUNT(g.game_id) AS Total_Games,
                    AVG(g.average_playtime_forever) AS Avg_Playtime_Forever
                FROM Games g
                JOIN Game_Genres gg ON g.game_id = gg.game_id
                GROUP BY gg.gen_id
            )
            SELECT gnr.genre AS Genre, gc.Total_Games, gc.Avg_Playtime_Forever as Avg_Playtime_Forever
            FROM GenreCounts gc
            JOIN Genres gnr ON gc.gen_id = gnr.gen_id
            ORDER BY gc.Avg_Playtime_Forever DESC;
            """
        data = execute_query(query)
        
        # Create a horizontal bar chart for the Roll-Up operation
        fig = px.bar(data, x='Avg_Playtime_Forever', y='Genre', orientation='h', title="Average Playtime Forever by Game Genre")
        return [dcc.Graph(id='olap-graph', figure=fig)]  # Return the graph

    elif selected_operation == 'drilldown':
        # Drill-Down: Reviews by month for a specific year
        if query_type == 'basic':
            # Basic Drill-Down Query
            query = f"""
            SELECT MONTH(release_date) AS release_month, 
                    COUNT(reviews.review_id) AS total_reviews, 
                    SUM(recommendations) AS total_recommendations, 
                    AVG(average_playtime_forever) AS avg_playtime
            FROM reviews
            JOIN games ON reviews.game_id = games.game_id
            WHERE YEAR(release_date) = {selected_year}
            GROUP BY MONTH(release_date);
            """
        else:
            # Optimized Drill-Down Query
            query = f"""
            WITH FilteredGames AS (
                SELECT game_id, release_date, recommendations, average_playtime_forever
                FROM games
                WHERE YEAR(release_date) = {selected_year}
            )
            SELECT
                MONTH(release_date) AS release_month,
                COUNT(reviews.review_id) AS total_reviews,
                SUM(recommendations) AS total_recommendations,
                AVG(average_playtime_forever) AS avg_playtime
            FROM reviews
            JOIN FilteredGames fg ON reviews.game_id = fg.game_id
            GROUP BY MONTH(release_date);
            """
        data = execute_query(query)

        # If there's no data, display a message
        if not data:
            return [html.Div("No data available for the selected parameters.")]

        if isinstance(data, list):
            data = pd.DataFrame(data, columns=['release_month', 'total_reviews', 'total_recommendations', 'avg_playtime'])

        # Create a grouped bar chart for the Drill-Down operation
        months = pd.DataFrame({'release_month': range(1, 13)})

        # Merge with the existing data to include all months
        data = months.merge(data, on='release_month', how='left').fillna(0)

        # Create a figure for Total Reviews
        fig_reviews = go.Figure()
        fig_reviews.add_trace(go.Bar(
            x=data['release_month'],
            y=data['total_reviews'],
            name='Total Reviews',
            marker_color='blue',
            opacity=0.7  # Make bars slightly transparent
        ))

        # Update layout for Total Reviews graph
        fig_reviews.update_layout(
            title=f"Monthly Total Reviews for {selected_year}",
            xaxis_title='Release Month',
            yaxis_title='Total Reviews',
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']
            ),
            yaxis=dict(title='Total Reviews', zeroline=True),
            barmode='group'  # Grouped bars for Total Reviews
        )

        # Create a combined figure for Average Playtime and Total Recommendations
        fig_combined = go.Figure()

        # Add a line chart for Total Recommendations
        fig_combined.add_trace(go.Scatter(
            x=data['release_month'],
            y=data['total_recommendations'],
            mode='lines+markers',
            name='Total Recommendations',
            line=dict(color='green'),
            yaxis='y'  # Use the primary y-axis
        ))

        # Add a line chart for Average Playtime
        fig_combined.add_trace(go.Scatter(
            x=data['release_month'],
            y=data['avg_playtime'],  # Assuming you have avg_playtime in your DataFrame
            mode='lines+markers',
            name='Average Playtime',
            line=dict(color='orange'),
            yaxis='y2'  # Use a secondary y-axis
        ))

        # Update layout for combined graph
        fig_combined.update_layout(
            title=f"Monthly Recommendations and Average Playtime Trends for {selected_year}",
            xaxis_title='Release Month',
            yaxis_title='Count',
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']
            ),
            yaxis=dict(title='Total Recommendations', zeroline=True),
            yaxis2=dict(title='Average Playtime (minutes)', overlaying='y', side='right'),
        )

        # Return both graphs
        return [dcc.Graph(id='olap-graph-reviews', figure=fig_reviews),
                dcc.Graph(id='olap-graph-combined', figure=fig_combined)]

    elif selected_operation == 'slice':
        # Slice: Filter games by genre for a specific year
        if query_type == 'basic':
            # Basic Slice Query
            query = f"""
            SELECT games.name, price
            FROM games
            JOIN game_genres ON games.game_id = game_genres.game_id
            JOIN genres ON game_genres.gen_id = genres.gen_id
            WHERE genres.genre = '{selected_genre}' AND YEAR(games.release_date) = {selected_year};
            """
        else:
            # Optimized Slice Query
            query = f"""
            SELECT games.name, price
            FROM games
            JOIN game_genres ON games.game_id = game_genres.game_id
            JOIN genres ON game_genres.gen_id = genres.gen_id
            WHERE genres.genre = '{selected_genre}' AND YEAR(games.release_date) = {selected_year};
            """
        data = execute_query(query)

        # If there's no data, display a message
        if not data:
            return [html.Div("No data available for the selected parameters.")]

        # Create a scatter plot for the Slice operation
        fig = px.bar(data, x='name', y='price', title=f"{selected_genre} Games by Price for {selected_year}",
                  labels={'name': 'Game Name', 'price': 'Price'},
                  color='price')
        return [dcc.Graph(id='olap-graph', figure=fig)]  # Return the graph

    elif selected_operation == 'dice':
        # Dice: Filter games by multiple dimensions
        if query_type == 'basic':
            # Basic Dice Query
            query = f"""
            SELECT games.name, achievements
            FROM games
            JOIN game_genres ON games.game_id = game_genres.game_id
            JOIN genres ON game_genres.gen_id = genres.gen_id
            WHERE genres.genre = '{selected_genre}' AND YEAR(games.release_date) = {selected_year} AND games.{selected_operation} = 1;
            """
        else:
            # Optimized Dice Query
            query = f"""
            WITH FilteredGames AS (
                SELECT game_id, name, achievements
                FROM games
                WHERE YEAR(release_date) = {selected_year} AND {selected_platform} = 1
            )
            SELECT fg.name, fg.achievements
            FROM FilteredGames fg
            JOIN game_genres gg ON fg.game_id = gg.game_id
            JOIN genres gnr ON gg.gen_id = gnr.gen_id
            WHERE gnr.genre = '{selected_genre}';
            """
        data = execute_query(query)

        # If there's no data, display a message
        if not data:
            return [html.Div("No data available for the selected parameters.")]

        fig = px.bar(data, x='name', y='achievements', title=f"{selected_genre} Games (Released in {selected_year}, {selected_platform})")

        return [dcc.Graph(id='olap-graph', figure=fig)]  # Return the graph

    # Default message if no valid operation is selected
    return [html.Div("Please select an OLAP operation.")]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)