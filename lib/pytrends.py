import pytrends

from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq(hl='en-US', tz=360)

#keywords to analyze
kw_list = ['regret voting Trump', 'why did I vote Trump', 'Trump regret 2024']

pytrends.build_payload(kw_list, timeframe='2024-11-01 2025-11-06', geo='US', cat=0, gprop='')

#pytrends dataframe for interest over time
df = pytrends.interest_over_time()
print(df.head())