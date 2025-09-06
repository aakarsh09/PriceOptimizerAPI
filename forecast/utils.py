from prophet import Prophet
import pandas as pd

def forecast_demand(monthly_sales, periods=6):
    # Prepare data for Prophet
    data = pd.DataFrame(monthly_sales)
    data.rename(columns={'month': 'ds', 'total_units': 'y'}, inplace=True)

    data['ds'] = pd.to_datetime(data['ds'])

    model = Prophet()
    model.fit(data)

    future = model.make_future_dataframe(periods=periods, freq='M')
    forecast = model.predict(future)

    # Return only future forecast (after last date in original data)
    forecasted = forecast[['ds', 'yhat']].tail(periods)
    return forecasted
