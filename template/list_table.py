import dash_html_components as html

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Thead([
            html.Tr([
                html.Th(col) for col in dataframe.columns
            ])
        ])] +

        # Body
        [html.Tbody(
            [html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(len(dataframe))]
        )]
    )