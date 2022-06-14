from pydantic import BaseModel
from typing import Dict, List
from app.config import SENSITIVE_PATH

class DFAFilter():
    
    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'

    def add(self, keyword):
        if not isinstance(keyword, str):
            keyword = keyword.decode('utf-8')
        keyword = keyword.lower()
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path):
        with open(path, encoding='UTF-8') as f:
            for keyword in f:
                self.add(keyword.strip())

    def filter(self, message, repl="*"):
        if not isinstance(message, str):
            message = message.decode('utf-8')
        message = message.lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        return ''.join(ret)
    
    
    def is_contain_sensi_key_word(self, message):
        repl = '_-__-'
        dest_string = self.filter(message=message, repl=repl)
        if repl in dest_string:
            return True
        return False
    
    
    def get_words(self, message):
        start = False
        all_words = []
        current = []

        for i, s in enumerate(self.filter(message)+'   '):

            # 开始发现一个星星,标记开始,记录字符
            if not start and s == '*':
                start = True
                current.append(message[i])

            # 已经开始,遇到星星
            elif start and s == "*":
                current.append(message[i])

            # 已经开始，不是星星了，更新开始状态
            # 录入字符， 改变current
            elif start and s != "*":
                start = False
                all_words.append(''.join(current))
                current = []

            # 没开始也不是星星
            elif not start and s != '*':
                pass

            else:
                print('Unknow condition,hahaha ')
                
        return all_words
        



class TextInfo(BaseModel):
    result:List[Dict]


class DFAParser():
    def __init__(self, text_handler = None):
        self.text_handler = text_handler if text_handler else DFAFilter()
        self._initialize()
        
    def _initialize(self):
        self.text_handler.parse(SENSITIVE_PATH)
        
    def parse(self, texts:List[str]):
        # return {t:self.text_handler.is_contain_sensi_key_word(t) for t in texts}
        result = []
        for t in texts:
            contain = self.text_handler.is_contain_sensi_key_word(t)
            words = self.text_handler.get_words(t)
            result.append(
                {
                    "text":t,
                    "sensitive":contain,
                    "sensitive_words":words
                }
            )
            
        return TextInfo(result = result)