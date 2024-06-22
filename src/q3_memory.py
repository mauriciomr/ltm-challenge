import pandas as pd
from collections import Counter
from typing import List, Tuple

def extract_mentions(users: List[dict]) -> List[str]:
    """get usernme from mentions"""
    return [user['username'] for user in users]

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    # init mention counter
    mention_counter = Counter()
    
    # load line by line the file
    with pd.read_json(file_path, lines=True, chunksize=1000) as reader:
        for chunk in reader:
            for mentions in chunk['mentionedUsers'].dropna():
                mention_counter.update(extract_mentions(mentions))
    
    # get top ten mentioned users
    top_ten_user_mentions = mention_counter.most_common(10)
    
    return top_ten_user_mentions
