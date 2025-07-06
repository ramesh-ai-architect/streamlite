import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def get_sample_data():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    return pd.DataFrame({
        'Month': months,
        'Sales': np.random.randint(100, 500, len(months)),
        'Profit': np.random.randint(10, 100, len(months)),
        'Region': np.random.choice(['East', 'West', 'North', 'South'], len(months))
    })

def forecast_sales(df, steps=3):
    df = df.copy()
    df['MonthIndex'] = range(1, len(df)+1)
    model = LinearRegression()
    model.fit(df[['MonthIndex']], df['Sales'])

    future = pd.DataFrame({'MonthIndex': range(len(df)+1, len(df)+steps+1)})
    future['SalesForecast'] = model.predict(future[['MonthIndex']])
    return future