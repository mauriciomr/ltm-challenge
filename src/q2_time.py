from typing import List, Tuple
import emoji
import pandas as pd
from collections import Counter

def extract_emojis(text: str) -> List[str]:
    """get emojis from text."""
    return [char for char in text if char in emoji.EMOJI_DATA]

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    # load file in dataframe
    tweets_df = pd.read_json(file_path, lines=True)

    # get all emogis from text
    all_emojis = [em for tweet in tweets_df['content'] for em in extract_emojis(tweet)]

    #count emojis
    emoji_counts = Counter(all_emojis)

    # retun de top ten emojis
    top_ten_emojis = emoji_counts.most_common(10)

    return top_ten_emojis