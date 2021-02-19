from google_trans_new import google_translator as gtrans
import sys
import os
# 파일의 질문 인수
qry_list = sys.argv[1:-1]
# qry_list 내용 
# ["파이썬에서", ""리스트를", "문자열로", "변환하라"]
# 파일의 예제 파일 저장할 이름
file_name = sys.argv[-1]
qry = "".join(qry_list)
# 질문 번역
trans = gtrans()
trans_text = trans.translate(qry, lang_tgt="en")
print(trans_text) 
os.system(f"howdoi {trans_text} > {file_name}")



