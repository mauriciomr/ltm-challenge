import pandas as pd
from datetime import datetime
from typing import List, Tuple

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    tweets_df = pd.read_json(file_path, lines=True)
    # New datafreme with date and user
    filtered_df = tweets_df[['date', 'user']].copy()
    # add username column 
    filtered_df['username'] = filtered_df['user'].apply(lambda x: x['username'])
    filtered_df['date'] = pd.to_datetime(filtered_df['date'])

    # grouping by date format because date has datime format
    tweets_by_dates = filtered_df.groupby(filtered_df['date'].dt.date).size()

    # get top ten dates 
    top_ten_dates = tweets_by_dates.nlargest(10).index
    top_ten_dates_user = []

    for fecha in top_ten_dates:
        # filter by date
        tweets_by_date= filtered_df[filtered_df['date'].dt.date == fecha]
        
        # count twits by user
        tweets_by_dates_user= tweets_by_date['username'].value_counts()
        
        # get the top user 
        top_user = tweets_by_dates_user.idxmax()
        
        # add to array
        top_ten_dates_user.append((fecha, top_user))

    return top_ten_dates_user
