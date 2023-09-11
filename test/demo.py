import sys
sys.path.append('/home/sunil/myproject/Pychunks/pychunks')

from pychunks.llama_index.sentence_splitter import SentenceSplitter
from pychunks.llama_index.token_splitter import TokenTextSplitter
text = "Ram is a good boy"

sentence_text_splitter = SentenceSplitter()
res = sentence_text_splitter.split_text(text = text)
print( res)
token_text_splitter = TokenTextSplitter(separator=" ")


res2 = token_text_splitter.split_text(text=text)
print(res2)