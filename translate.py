
import streamlit as st
from urllib.request import urlopen
from pathlib import Path
from deep_translator import (GoogleTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                        )

def page3():
    st.header('Product Description Translate (For HTML)',divider='rainbow')
    headcontainer=st.container()
    colA1, colA2,colA3 =st.columns(3)
    groupsider=st.sidebar.container(border=True)
    
    at_eng_link='<div>Store: <a href="https://www.hgcmore.com/pages/at" style="text-decoration-line: underline;">AT+</a></div>\n'
    at_chi_link='<div>商店: <a href="https://www.hgcmore.com/pages/at" style="text-decoration-line: underline;">AT+</a></div>\n'
    imart_eng_link='<div>Store: <a href="https://www.hgcmore.com/pages/imart" style="text-decoration-line: underline;">i mart</a></div>\n'
    imart_chi_link='<div>商店: <a href="https://www.hgcmore.com/pages/imart" style="text-decoration-line: underline;">i mart</a></div>\n'
    
    sample_str= """產品內容:

*TSA海關專用密碼鎖, 保障安全.
*高承重穩定設計, 承載重物更放心.
*靜音萬向輪配備彈簧避震及刹車機構, 行走質感舒適.
*兩檔高度調節鋁合金拉杆, 隨時調整配合身高.
*新型抗菌PC材質箱身及鋁合金中框, 確保堅固耐用.
*儲物倉備有多個獨立分區, 物品取放更輕鬆簡單.

商品描述 :

26"行李箱
- 重量 : 約 4.5 kg
- 呎吋 : 71*43*37 cm

28"行李箱
- 重量 : 約 5.0 kg
- 呎吋 : 75*44*39 cm

30"行李箱
- 重量 : 約 5.2 kg
- 呎吋 : 81.5*44*39 cm

*呎吋為手工測量可能存在誤差, 于3釐米內之差別屬正常情況, 請以實物為准.
*圖片產品顏色因應燈光效果而有所色差，敬請留意"""
   
    openbrtext = groupsider.toggle(":spider_web: Add BR",value=True)
    colA1.write('Org Text')
    txt = colA1.text_area('org',label_visibility="collapsed",value=sample_str
                        , height=400
                            )

    text_length = len(txt)

    if text_length>=5000:
       st.error(f' Text length need to be between 0 and 5000 characters, current text length: {text_length}  characters')
    
    if text_length<=5000:
        translated_en = GoogleTranslator(source='auto', target='en').translate(text=txt)
        translated_ct = GoogleTranslator(source='auto', target='zh-TW').translate(text=txt)
 
        if openbrtext:
            colA2.write('Chinese + BR')
            colA3.write('ENG + BR') 
            with colA2.container(height=400,border=False):
                st.code(translated_ct.replace('\n', '<br/>\n'),language='html')
                
            with colA3.container(height=400,border=False):
                st.code(translated_en.replace('\n', '<br/>\n'),language='html')
        else:
            genre = groupsider.radio(
                    "HGC hyperlink",
                    ["AT+","i mart","None"],
                    index=0,horizontal=True
                )

            colA2.write(f'Chinese -- :red[ {genre}]')
            colA3.write(f'ENG -- :red[ {genre}]') 
        
            if genre=="AT+":
                chi_pref=at_chi_link
                eng_pref=at_eng_link
            if genre=="i mart":
                chi_pref=imart_chi_link
                eng_pref=imart_eng_link
            if genre=="None":
                chi_pref=""
                eng_pref=""
            with colA2.container(height=400,border=False):
                st.code(chi_pref + translated_ct,language='html')
                
            with colA3.container(height=400,border=False):
                st.code(eng_pref + translated_en,language='html')
                
page3()