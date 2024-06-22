import pandas as pd
from collections import Counter
from typing import List, Tuple

def extract_mentions(users: List[dict]) -> List[str]:
    """get usernme from mentions"""
    return [user['username'] for user in users]

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    # load file in panda dataframe
    tweets_df = pd.read_json(file_path, lines=True)

    #  get the mentions in every twit
    all_mentions = [mention for mentions in tweets_df['mentionedUsers'].dropna() for mention in extract_mentions(mentions)]

    # count mentions
    mention_counts = Counter(all_mentions)

    # get top ten mentioned users
    top_ten_user_mentions = mention_counts.most_common(10)

    return top_ten_user_mentions