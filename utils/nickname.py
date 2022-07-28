
import os
import random
import re


regex = re.compile(r'^[a-zA-Z0-9가-힣]{2,20}$') # 한글, 영어, 숫자, 길이 2~20

with open(os.path.join(os.path.dirname(__file__), './nicknames.txt'), 'r', encoding='utf8') as f:
    nicknames = [i for i in f.read().splitlines() if i.strip()]

def choice() -> str:
    return random.choice(nicknames)

def valid(nickname: str) -> bool:
    return bool(regex.match(nickname))