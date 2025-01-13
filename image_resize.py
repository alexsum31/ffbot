import streamlit as st
import pandas as pd
from PIL import Image, ImageFile,ImageChops, ExifTags
import numpy as np
import os
from pathlib import Path
import re
from io import StringIO,BytesIO
import math
import datetime
#from stqdm import stqdm
from time import sleep
from  streamlit_vertical_slider import vertical_slider
import base64

def load_image(image_file):
	#img = Image.open(image_file).convert("RGB")
    img = Image.open(image_file)
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif = img._getexif()
        # if exif[orientation] is None:
        #     print('no tag')
        if exif[orientation] == 3:
            img=img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img=img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img=img.rotate(90, expand=True)  
    except:
        print("no tag")
    return img

def trim(img):
    pim =img.convert("RGB")
    A_pim = img
    im  = np.array(pim)
    white = [255,255,255]
    Y, X = np.where(np.all(im!=white,axis=2))
    Max_Y=max(Y).astype(int)
    Min_Y=min(Y).astype(int)
    Max_X=max(X).astype(int)
    Min_X=min(X).astype(int)
    A_im1 = A_pim.crop((Min_X, Min_Y+1, Max_X+1,Max_Y+1))
    return A_im1



def cropimage(iMA,border,updown,leftright,methodA,img_type):
    if img_type=='image/png':
         height=iMA.height
         width=iMA.width
         A_im1 = iMA
    else:
        A_pim = trim(iMA)
        height=A_pim.height
        width=A_pim.width
        A_im1 = A_pim
        
    if width>height : 
       # new_width  = 750
        new_width  = int(10 * border)#int(600 *((100-border)/100))
        new_height = int(math.ceil(new_width * height / width ))
    else:
        #new_height = 750
        new_height  =int(10 * border)#int(600 *((100-border)/100))
        new_width  = int(math.ceil(new_height * width / height))
        
    listA=[Image.Resampling.LANCZOS,Image.Resampling.NEAREST,Image.Resampling.BILINEAR,Image.Resampling.BICUBIC]
    ##imgA = A_im1.resize((new_width, new_height), Image.ANTIALIAS)Image.NEAREST
    imgA = A_im1.resize((new_width, new_height), listA[methodA])

    
    imgC=writebg(imgA,updown,leftright,img_type)
    return imgC

def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

def writebg(iMB,UD2,leftright,img_type):
    from PIL import Image
    lr2=(100-leftright)/50
    UD3=(UD2)/50
    img = Image.new("RGB", (600, 600), (255, 255, 255))
    img_past=iMB.size
    if img_type=='image/png' or img_type=='image/webp':
        img.paste(iMB,(300-int((img_past[0]/2)*lr2),300-int((img_past[1]/2)*UD3)), iMB.convert('RGBA'))#mask=iMB

    else:
        img.paste(iMB,(300-int((img_past[0]/2*lr2)),300-int((img_past[1]/2)*UD3)))
    iMC=img
    return iMC
    

def multiple_replace(string, rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)

    
def get_image_download_link(img,qat=100):
    buffered = BytesIO()
    img.save(buffered, format="JPEG",quality=qat, optimize=True)
    return buffered.getvalue()


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def generate_download_button(imgT, filename, file_label,qat=100):
    st.download_button(label=f":frame_with_picture: {file_label}",
                           data= get_image_download_link(imgT,qat),
                            file_name=filename,
                            mime="image/jpeg", use_container_width=True,help='Download file')
     

import random

def drawworkingarea(idx,uploaded_files,options,sampling_method,zoom_levels,updown_levels,fileoutimg,leftright_levels,quality_levels):
    file=uploaded_files[idx]
    STANDARDCOLOR='#24CB67'
    with st.container(border=True):

        #zoom_levels[file.name] = st.slider("Zoom", min_value=-50, max_value=50, step=1,value=10 ,key=str(idx)+'_zoom')
        #updown_levels[file.name] = st.slider("updown", min_value=0, max_value=100, step=1,value=49, key=str(idx)+'_updown')
        #leftright_levels[file.name] = st.slider("leftright", min_value=0, max_value=100, step=1,value=50, key=str(idx)+'_leftright')
        container_cols =st.columns((1,1,1))
        with container_cols[0]:
            zoom_levels[file.name]=vertical_slider(
                                            label = "Zoom",  #Optional
                                            key = str(idx)+'_zoom',
                                            height = 80, #Optional - Defaults to 300
                                            step = 1, #Optional - Defaults to 1
                                            default_value=55 ,#Optional - Defaults to 0
                                            slider_color= STANDARDCOLOR,
                                            thumb_color = STANDARDCOLOR,
                                            min_value= 20, # Defaults to 0
                                            max_value= 80, # Defaults to 10
                                            #value_always_visible = True ,#Optional - Defaults to False
                                    )
      
        with container_cols[1]:
            leftright_levels[file.name]=vertical_slider(
                        label = "x axis",  #Optional
                        key = str(idx)+'_leftright',
                        height = 80, #Optional - Defaults to 300
                        step = 1, #Optional - Defaults to 1
                        default_value=50 ,#Optional - Defaults to 0
                        min_value= 1, # Defaults to 0
                        max_value= 100, # Defaults to 10
                        slider_color= STANDARDCOLOR,
                        thumb_color = STANDARDCOLOR,
                        #value_always_visible = True ,#Optional - Defaults to False
                    )
        
        with container_cols[2]:                                
            updown_levels[file.name]=vertical_slider(
                            label = "y axis",  #Optional
                            key = str(idx)+'_updown',
                            height = 80, #Optional - Defaults to 300
                            step = 1, #Optional - Defaults to 1
                            default_value=50 ,#Optional - Defaults to 0
                            min_value= 1, # Defaults to 0
                            max_value= 100, # Defaults to 10
                            slider_color= STANDARDCOLOR,
                            thumb_color = STANDARDCOLOR,
                            #value_always_visible = True ,#Optional - Defaults to False
                        ) 
 
        imgB = load_image(file,)
        fileoutimg[idx]=cropimage(imgB,zoom_levels[file.name],updown_levels[file.name], leftright_levels[file.name] ,options.index(sampling_method),file.type)
        st.image(fileoutimg[idx],use_container_width=True)
        
        extstr=file.name.rfind('.')
        fullstrlen=len(file.name)
        finalstrlen=(fullstrlen-extstr)*-1
        generate_download_button(imgT=fileoutimg[idx], filename=file.name[0:finalstrlen]+'.jpg', file_label=file.name[0:finalstrlen],qat=100)
def tellfilesize(img,qua):
    import io
    edited_image_buffer = io.BytesIO()
    img.save(edited_image_buffer, format='JPEG',quality=qua, optimize=True)
    return edited_image_buffer.tell()

def byte2size(file_size):
    if file_size >= 1024 * 1024:
        file_size_str = f"{file_size / (1024 * 1024):.2f} MB"
    elif file_size >= 1024:
        file_size_str = f"{file_size / 1024:.2f} KB"
    else:
        file_size_str = f"{file_size} bytes"
    return file_size_str    
        
def page2():
    st.header("Product Image Converter (Batch)", divider='rainbow')
    MAX_LINES = 20
    st.caption(f'Maxmium upload to {MAX_LINES} images per batch')
    
    if 'batch_num' not in st.session_state:
        st.session_state['batch_num'] = 0
        
    uploaded_files = st.file_uploader("Upload your images", type=['.jpg','.JPG','.png','.PNG','.jpeg','.JPEG','.gif','.GIF','.webp','.WEBP','.tif'],accept_multiple_files=True)
    
    if len(uploaded_files)>0:
        st.session_state['batch_num'] = len(uploaded_files)
    else:
        st.session_state['batch_num'] = 0
        
    if len(uploaded_files) > MAX_LINES:
        st.warning(f"Maximum number of files reached. Only the first {MAX_LINES} will be processed.")
        uploaded_files = uploaded_files[:MAX_LINES]
        
    st.sidebar.subheader(f"TL upload file: :green[{st.session_state.batch_num}]")    

    
    options=['Lanczos','Nearest','Bilinear','Bicubic']
    sampling_method=st.sidebar.selectbox('Sampling Method',options,0)
    maxcolumn_show=st.sidebar.slider('Column in row:',min_value=1,max_value=10,value=6)        
    zoom_levels = {}
    updown_levels = {}
    leftright_levels={}
    fileoutimg = {}
    quality_levels={}
    idx = 0 
    if uploaded_files:
       
        cols = st.columns(maxcolumn_show) 
        key_list = []
                  
        for idx, file in enumerate(uploaded_files): 
            key_list.append(uploaded_files[idx].name)
            filesize_KB=round(uploaded_files[idx].size/1024,2)
           
            checknowcol=idx % maxcolumn_show
            with cols[checknowcol]:
                    drawworkingarea(idx,uploaded_files,options,sampling_method,zoom_levels,updown_levels,fileoutimg,leftright_levels,quality_levels)
                

        suffixA = datetime.datetime.now().strftime("%y%m%d%H%M%S")
        zipfilename='Reszied_img_'+ suffixA +'.zip'
  
        if st.sidebar.button('Download all file in zip',key='we9031'):
            st.write(key_list)
            b64=packagezip(fileoutimg,key_list,zipfilename,) 
         
            href = f'<a href=\"data:file/zip;base64,{b64}\" download="{zipfilename}">Click Here To download</a>'
            st.markdown(href, unsafe_allow_html=True)
                            
def packagezip(uploadfile,indivi_filename,zip_file_name):
    import zipfile
    zip_buf=BytesIO()
    
    with zipfile.ZipFile(zip_buf, 'w') as zipf:
        for idx, url in enumerate(uploadfile):

            main, file_extension = os.path.splitext(indivi_filename[idx])
            n_filename = "".join([main,'.jpg'])#file_extension
           
            try:
                 with open(n_filename,"wb") as f:
                    f.write(get_image_download_link(uploadfile[idx]))   
                    zipf.write(n_filename,n_filename)
            except Exception as e:
                 print(f"無法下載或添加文件 {n_filename}：{e}")     
    zip_buf.seek(0)
    return base64.b64encode(zip_buf.read()).decode()
        

    
   
                
def app():        
    page2()


app()