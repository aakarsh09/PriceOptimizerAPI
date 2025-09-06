# forecast/urls.py

from django.urls import path
from .views import ChartDataView, DemandForecastView

urlpatterns = [
    path('chart-data/', ChartDataView.as_view(), name='chart-data'),
    path('', DemandForecastView.as_view(), name='forecast-demand'),
]
