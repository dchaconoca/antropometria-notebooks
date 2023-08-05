#################################
## Common Functions
#################################

import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt 

# Select columns of a dataframe
# Returns a dataset only with the selected columns

def select_data(df, col_drop=[], col_leave=[]):
     
    if col_leave:
        df = df.loc[:,col_leave]
    
    if col_drop:
        df.drop(col_drop, axis=1, inplace=True)
    
    return df


# Create a horizontal bar char with Altair
# Each bar is a categorie

def char_bars(df, x_in, y_in, detail, title, title_x, title_y):
    
    x = alt.X(x_in, title = title_x, stack='zero', 
          axis = alt.Axis(format = ",.2s", grid=True, titleAnchor='middle', labelFontSize=12))
    y = alt.Y(y_in, title=title_y, axis = alt.Axis(labelAngle=0, labelFontSize=10))
    
    tooltip=[alt.Tooltip(detail, title='Grado de obesidad'),
             alt.Tooltip(y_in, title='Rango de edad'),
             alt.Tooltip(x_in, title='Cantidad individuos')]

    bars = alt.Chart(df).mark_bar().encode(
        x=x,
        y=y,
        tooltip=tooltip,
        color=alt.Color(detail) 
    ).properties(
        title=title,
        width=700, 
        height=300
    )

    text = alt.Chart(df).mark_text(dx=-12, dy=3, color='white').encode(
        x=alt.X(x_in, stack='zero'),
        y=y_in,
        detail=detail,
        text=alt.Text(x_in)
    )
    
    final_graph = bars + text
    
    return final_graph