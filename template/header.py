import config
import dash_html_components as html

def header():
    return html.Div(
        className='header',
        children=[
            html.Div(
                className="iconArea",
                children=[
                    html.Img(src="../assets/pan_bread_1kin_yama.png")
                ]
            ),
            html.Div(
                className="titleArea",
                children=[
                    html.Span(config.TITLE_NAME)
                ]
            ),
            html.Div(
                className="socialArea",
                children=[
                    html.Img(src="../assets/GitHub-Mark-Light-64px.png")
                ]
            )
        ]
    )