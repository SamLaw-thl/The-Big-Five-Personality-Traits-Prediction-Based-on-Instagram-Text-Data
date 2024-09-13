import pandas as pd
import plotly.express as px

# using bar graph to visualize the personality prediction results
def personality_bar_chart(personality_prediction):
    personality_trait_list = list(personality_prediction.keys())
    prediction_list = [value[0] for value in personality_prediction.values()]

    fig = px.bar(x=personality_trait_list, y=prediction_list, labels={'x': 'Personality Traits', 'y': 'Predicted Probability'})
    fig.update_layout(
        title=dict(text='Rader Chart for The Big Five Personality Prediction', x=0.5),
        title_font=dict(size=24)
        )
    fig.show()


# using rader chart to visualize the personality prediction results
def personality_rader_chart(personality_prediction):
    personality_trait_list = list(personality_prediction.keys())
    prediction_list = [value[0] for value in personality_prediction.values()]

    df = pd.DataFrame(dict(r=prediction_list, theta=personality_trait_list))

    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(
        title=dict(text='Rader Chart for The Big Five Personality Prediction', x=0.5),
        title_font=dict(size=24),
        polar=dict(radialaxis=dict(visible=True))
       )
    fig.show()


