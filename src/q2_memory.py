import pandas as pd
import emoji
from collections import Counter
from typing import List, Tuple

def extract_emojis(text: str) -> List[str]:
    """get emojis from text."""
    return [char for char in text if char in emoji.EMOJI_DATA]

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
   
    # emoji counter
    emoji_counter = Counter()
    
    # get emojis from file
    with pd.read_json(file_path, lines=True, chunksize=1000) as reader:
        for chunk in reader:
            for content in chunk['content']:
                emojis = extract_emojis(content)
                emoji_counter.update(emojis)
    
    # retun de top ten emojis
    top_ten_emojis = emoji_counter.most_common(10)
    
    return top_ten_emojis