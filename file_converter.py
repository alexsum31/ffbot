import streamlit as st
from io import StringIO,BytesIO
import pandas as pd
import datetime

def packing_df(filename):
    storemap={'AT+ 沙田':'at-st', 
              'AT+ Sha Tin':'at-st',
              'AT+ 荔枝角陳列室':'at-lck',
              'AT+ Lai Chi Kok':'at-lck'}

    dicA={  'Order Status':'no_use1',   'Order Date':'訂單日期',
            'Order Num':'訂單號碼', 'SKU':'商品貨號',
            'Product Model Desc':'商品名稱',  'QTY':'數量',
            'SPR':'商品原價',  'Product Cost':'商品成本',
            'Effective Selling Price':'商品結帳價', 'Pickup Location':'門市名稱',
            'Invoice Name':'收件人', 'Invoice Shipping Name':'no_use9',
            'Invoice Email':'電郵',  'Invoice Phone':'收件人電話號碼',
            'Invoice Delivery Phone':'no_use10','Invoice Delivery Address':'no_use11',
            'Delivery Fee':'no_use12',  'Promotion Code':'no_use13', 'Promotion Program':'no_use135','Invoice Num':'no_use14', 'Invoice Date':'no_use15'}
    maindf=pd.read_excel(filename,sheet_name="Result")
    maindf.columns = maindf.columns.map(dicA)
    df = maindf[maindf.columns.drop(list(maindf.filter(regex='no_')))]
    df.loc[:, '門市名稱'] = df['門市名稱'].replace(storemap)
    #df['門市名稱'] = df['門市名稱'].map(storemap) #1. missing no mapping item show
    specified_columns=['訂單號碼', '預購訂單',  '訂單日期',
                            '訂單狀態',  '送貨方式',   '送貨狀態',   '商品貨號',
                            '商品名稱',   '選項',        '商品類型',     '數量',   '預購商品',    '商品預購提示',
                            '加購品類型',    '收件人',    '收件人電話號碼',       '電郵',
                            '地址 1',    '地址 2',    '到貨日期',      '到貨時間',  '完整地址',
                            '門市名稱', '訂單標籤',     '訂單備註',   '管理員備註', '出貨備註',      '串接物流貨態',
                            '貨件追蹤號碼',  '順豐 / Alfred 智能櫃點碼',     '商品成本',
                            '商品原價', '商品結帳價',    '運費',    '附加費',      '已退款金額',     '退貨單編號',
                            '退貨便代碼',     '儲位編號',     'deposit',    'balance',  'lang',    'free_premium', 'remark'
                            ]

    #new_columns = specified_columns + list(set(df.columns) - set(specified_columns))
    new_df = pd.DataFrame(columns=specified_columns)

    for index, row in df.iterrows():
        new_row = []
        for column in specified_columns:
            if column in df.columns:
                new_row.append(row[column])
            else:
                new_row.append(None) 
        # for column in set(df.columns) - set(specified_columns):
        #     new_row.append(row[column])
        new_df.loc[index] = new_row

    new_df.loc[:, 'lang'] = 'CHT'

    return new_df


def app():
    col1 , col2=st.columns( [1,1])
    
    col1.header("AT2Pickme File Converter", divider='rainbow')
    
    T_today=datetime.date.today().strftime('%Y%m%d')
    df_uploaded = col1.file_uploader('Choose AT website file:',type = ['xlsx'])
    if df_uploaded:
        # try:
            temp=packing_df(df_uploaded)
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # Write each dataframe to a different worksheet.
                temp.to_excel(writer, sheet_name='Sheet1',index=False)
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                column_index = 19 
                fill = workbook.add_format({'bg_color': 'yellow'})
                worksheet.set_column(column_index, column_index, cell_format=fill)
                writer._save()
                col1.download_button(
                    label="Download Excel worksheets",
                    data=buffer,
                    file_name="Pickme_{}.xlsx".format(T_today),
                    mime="application/vnd.ms-excel"
                )
         
        # except:
        #     col1.error('Read file error',  icon="⚠️")

app()