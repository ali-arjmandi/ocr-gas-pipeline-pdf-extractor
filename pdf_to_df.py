import os, cv2
import pytesseract
from PyPDF2 import PdfFileReader
import numpy as np
import pandas as pd
from pdf2image import convert_from_path

def vertical(frame, vertical_val):
    vertical = np.copy(frame)
    rows = vertical.shape[0]
    verticalsize = rows // vertical_val
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)
    return vertical

def horizontal(frame, horizontal_val):
    h = np.copy(frame)
    cols = h.shape[1]
    horizontal_size = cols // horizontal_val
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    h = cv2.erode(h, horizontalStructure)
    h = cv2.dilate(h, horizontalStructure)
    return h

def main_area(v, img):
    contours, _ = cv2.findContours(v,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    min_x = img.shape[1]
    for contour in contours:
        x,y,_,h = cv2.boundingRect(contour)
        if y < img.shape[0]/8 and x > img.shape[1]*(5/8) and x < img.shape[1]*(6/8):
            f_x = x
            f_y = y
            f_h = h
        if y < img.shape[0]/8 and x > img.shape[1]*(15/16):
            if x < min_x :
                min_x = x
        if y < img.shape[0]/8 and x > img.shape[1]*(13/16) and x < img.shape[1]*(14/16):
            line_x = x

    if 'f_x' not in locals():
        return 404
    w = min_x - f_x
    area = img[f_y+20:int(f_h*0.78),f_x+1:f_x+w]
    line_x = line_x - f_x+1
    return (area, line_x)
            
def threshold(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                25,
                5
            )
    return th

def del_text(h, img, line_x):
    list = []
    contours, _ = cv2.findContours(h,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x,y,w,_ = cv2.boundingRect(contour)
        if x < img.shape[1]*(1/5):
            list.append((x, y))
            cv2.rectangle(img,(x,y-1),(x+w,y+1),(0,0,0),-1)

    list = list[::-1]
    if len(list) < 3:
        cv2.rectangle(img,(int(img.shape[1]*(1/16)),0),(line_x-2,img.shape[0]),(0,0,0),-1)

    if len(list) == 3:
        x = list[1][0]
        y = list[1][1]
        cv2.rectangle(img,(x,y),(line_x-2,img.shape[0]),(0,0,0),-1)

    if len(list) >= 6:
        x1 = list[1][0]
        y1 = list[1][1]
        y2 = list[3][1]
        x3 = list[4][0]
        y3 = list[4][1]
        cv2.rectangle(img,(x1,y1+2),(line_x-3,y2-2),(0,0,0),-1)
        cv2.rectangle(img,(x3,y3+2),(line_x-3,img.shape[0]),(0,0,0),-1)

    return img

def analize_right(str, shape):
    row = str.split("\n")
    columns = row[0].split('\t')
    units = []
    for h in range(1, len(row)):
        units.append(row[h].split('\t'))

    df = pd.DataFrame(units, columns=columns)
    df = df.loc[(df['conf'] != '-1') & (df['text'] != 'NO')]
    df.iloc[:,:11] = df.iloc[:,:11].astype(int)

    pt_list = df.loc[(df['text'] == 'PT'),'top'].values
    if len(pt_list):
        pt_top = int(pt_list[0])
        if len(pt_list) == 2:
            pt_down = int(pt_list[1])

    tak_of = pd.DataFrame(columns=['PTNo','ItemCode','Qty','Type']) 

    width = shape[1]
    pt_var = int(width * 0.055)
    tmp_var = int(shape[0] * 0.01)
    mat_min = int(width * 0.078)
    mat_max = int(width * 0.165)
    j_min = int(width * 0.602)
    j_max = int(width * 0.723)
    k_var = int(width * 0.843)
    material = df.loc[(df['left'] > mat_min) & (df['left'] < mat_max),'text'].values
    
    for index in df[df['left']<=pt_var].index:
        
        if df.loc[index,'text'].isdigit():
            top = df.loc[index, "top"]
            tmp = df.loc[(df.loc[:,'top']>top - tmp_var) & (df.loc[:,'top']<top + tmp_var),["text","left"]]
            j = tmp.loc[(tmp['left'] > j_min) & (tmp['left'] < j_max),'text'].values
            k = tmp.loc[(tmp['left'] > k_var) ,'text'].values
            if len(j): j = j[0]
            else: j = '-'
            if len(k):
                if k[0][-1] == 'M':
                    k = k[0][:-1]
                else:
                    k = k[0]
            else: k = '-'
            if len(pt_list) == 1:
                l = material[0]
            elif len(pt_list) == 2:
                if top <= pt_down:
                    l = material[0]
                elif top > pt_down:
                    l = material[1]
            else:
                l = '-'

            query = {'PTNo':df.loc[index,'text'], 'ItemCode':j, 'Qty':k, 'Type':l}
            tak_of = tak_of.append(query , ignore_index=True)
    return tak_of

def cut(h, v, img):
    contours, _ = cv2.findContours(v,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    min_x = 0
    last_x = img.shape[1]
    for contour in contours:
        x,y,_,_ = cv2.boundingRect(contour)
        if y > img.shape[0]*0.75:
            if x > min_x and x < img.shape[1]*0.25 :
                min_x = x
                min_y = y
        if y < img.shape[0]*0.1:
            if x > img.shape[1]*0.95 and x < last_x :
                last_x = x
                    
    img = img[min_y:img.shape[0],min_x:last_x]
    bw = threshold(img)
    v2 = vertical(bw,1)
    h2 = horizontal(bw,1)
    contours, _ = cv2.findContours(h2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    list = []
    for contour in contours:
        _,y,_,_ = cv2.boundingRect(contour)
        list.append(y)
    M = list[-2] - list[-1]
    
    contours, _ = cv2.findContours(v2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    line2_x = img.shape[1]
    line_x = img.shape[1]
    line_y = 0
    for contour in contours:
        x,y,_,h = cv2.boundingRect(contour)
        if x < line_x and x > img.shape[1]*0.2 :
            line_x = x
            line_y = y
            line_h = h-M
        if x > img.shape[1]*0.58 and x < line2_x:
            line2_x = x
    kernel = np.ones((2,2),np.uint8)
    tmp_img = cv2.dilate(img,kernel,iterations = 1)
    img[:,int(img.shape[1]*0.90):] = tmp_img[:,int(img.shape[1]*0.90):]
    cv2.rectangle(bw,(line_x,line_y),(line2_x,line_h),(0,0,0),-1)
    cv2.rectangle(bw,(line2_x,0),(img.shape[1], 7*M),(0,0,0),-1)
    v2 = vertical(bw,10)
    h2 = horizontal(bw,10)
    mask = v2 + h2
    bw = bw - mask
    return (cv2.bitwise_not(bw), M)

def find_element(values, pdf, shape):
    line = pd.DataFrame(columns=['LineNo','Document No','Drawing No','LineClass',
        'UnitNo','P&IDNo','PressDesign','TempDesign',
        'PressOperating','TempOperating','TestFluid','PressTest',
        'InsualtionType','InsulationThk','PaintCode','HeatTransfer',
        'StressAnalysis','Density','SteamTracing','TracingSize',
        'ElecTracing','NDT','PWHT','Phase','Rev','SHEETS'])
    sheet = pd.DataFrame(columns=['Sheet','Of','Rev','DocClass'])
    height = shape[0]
    width = shape[1]
    LineNo = ''
    Document = ''
    Drawing = ''
    LineClass = ''
    UnitNo = '-'
    PIDNo = ''
    PressDesign = ''
    TempDesign = ''
    PressOperating = ''
    TempOperating = ''
    TestFluid = ''
    PressTest = ''
    InsualtionType = ''
    InsulationThk = ''
    PaintCode = ''
    HeatTransfer = ''
    StressAnalysis = ''
    Density = ''
    SteamTracing = ''
    TracingSize = ''
    ElecTracing = ''
    NDT = ''
    PWHT = ''
    Phase = ''
    Rev = ''
    page = ''
    SHEETS = ''
    for i in values:
        x = i[0]
        y = i[1]
        txt = i[2]
        if i[3] == 'a':
            PressDesign = txt
        elif i[3] == 'b':
            PressOperating = txt
        elif i[3] == 'c':
            TempDesign = txt
        elif i[3] == 'd':
            TempOperating = txt
        elif i[3] == 'e':
            SteamTracing = txt
        elif i[3] == 'f':
            TracingSize = txt
        elif i[3] == 'g':
            ElecTracing = txt
        elif i[3] == 'h':
            if txt != ':' and LineNo == '':
                LineNo = txt
        elif i[3] == 'i':
            Document += txt
        elif i[3] == 'j':
            Drawing = txt
        elif i[3] == 'k':
            org = txt
            if org == '1':
                org = 'I'
        elif i[3] == 'l':
            Rev = txt
            if len(Rev) == 2:
                Rev = 'D'+Rev[1]
        elif i[3] == 'm':
            page = txt
        elif i[3] == 'n':
            SHEETS = txt
            while '/' in SHEETS:
                SHEETS = SHEETS[1:]
            while not SHEETS[0].isdigit():
                SHEETS = SHEETS[1:]
            if len(SHEETS)>=2:
                if SHEETS[0]=='7':
                    SHEETS = SHEETS[1:]
        elif i[3] == 'o':
            DocClass = txt
        elif x < width*0.083 and y > height*0.258 and y < height*0.344:
            TestFluid = txt
        elif x < width*0.083 and y > height*0.344 and y < height*0.447:
            InsualtionType = txt
        elif x < width*0.083 and y > height*0.447 and y < height*0.525:
            PaintCode = txt
        elif x < width*0.083 and y > height*0.525 and y < height*0.619:
            StressAnalysis = txt
        elif x > width*0.083 and x < width*0.223 and y > height*0.258 and y < height*0.344:
            PressTest = txt
        elif x > width*0.083 and x < width*0.223 and y > height*0.344 and y < height*0.447:
            InsulationThk = txt
        elif x > width*0.083 and x < width*0.223 and y > height*0.447 and y < height*0.525:
            HeatTransfer = txt
        elif x > width*0.083 and x < width*0.223 and y > height*0.525 and y < height*0.619:
            Density = txt
        elif x > width*0.15 and x < width*0.223 and y > height*0.619 and y < height*0.697:
            NDT = txt
            if len(NDT) > 2 :
                if NDT[1] != 'O':
                    NDT = NDT[:-3]+'%'+NDT[-2:]
        elif x > width*0.15 and x < width*0.223 and y > height*0.697 and y < height*0.8:
            PWHT = txt
        elif x > width*0.15 and x < width*0.223 and y > height*0.8 and y < height*0.886:
            Phase = txt
        elif x > width*0.242 and x < width*0.404 and y > height*0.8 and y < height*0.886:
            PIDNo = txt
    if len(LineNo.split('-')):
        LineClass = LineNo.split('-')[-2]
    if len(Document):
        if Document[-1] == '1':
            Document = Document[:-1] + 'I'
        tmp = Document.split('-')
        Document = 'DWG'+'-'+'-'.join(tmp[1:])
    if len(LineNo):
        for i in range (len(LineNo)-1):
            if LineNo[i] == '\"' or LineNo[i] == '”':
                LineNo = LineNo[:i]+LineNo[i+1:]
    pdf_split = pdf.split('-')
    if len(pdf_split) == 11:
        LineClass = pdf_split[2]
        org = pdf_split[8]
        Document = 'DWG-'+'-'.join(pdf_split[6:10])
        for i in range (len(pdf_split[1])):
            if pdf_split[1][i].isdigit():
                UnitNo = pdf_split[1][i:i+3]
                break
        if len(UnitNo) > 1 and  UnitNo in pdf:
            LineNo = pdf.split(UnitNo)[0]+'-'+UnitNo+'-'+pdf.split(UnitNo)[1].split('-')[0]+'-'+pdf.split(UnitNo)[1].split('-')[1]+'-'+pdf_split[3].split('_')[0]
            Drawing = pdf_split[1].split(UnitNo)[0]+'-'+UnitNo+'-'+pdf_split[1].split(UnitNo)[1]
        page = pdf_split[3].split('_')[-1]
    query1 = {
        'LineNo': LineNo,
        'Document No': Document,
        'Drawing No': Drawing,
        'LineClass': LineClass,
        'UnitNo': UnitNo,
        'P&IDNo': PIDNo,
        'PressDesign': PressDesign,
        'TempDesign': TempDesign,
        'PressOperating': PressOperating,
        'TempOperating': TempOperating,
        'TestFluid': TestFluid,
        'PressTest': PressTest,
        'InsualtionType': InsualtionType,
        'InsulationThk': InsulationThk,
        'PaintCode': PaintCode,
        'HeatTransfer': HeatTransfer,
        'StressAnalysis': StressAnalysis,
        'Density': Density,
        'SteamTracing': SteamTracing,
        'TracingSize': TracingSize,
        'ElecTracing': ElecTracing,
        'NDT': NDT,
        'PWHT': PWHT,
        'Phase': Phase,
        'Rev': Rev,
        'SHEETS': SHEETS
    } 
    query2 = {
        'Sheet' : page,
        'Of' : SHEETS,
        'Rev' : Rev,
        'DocClass' : DocClass
    }
    line = line.append(query1 , ignore_index=True)
    sheet = sheet.append(query2 , ignore_index=True)
    return (line, sheet)

def analize_down(str1, str2, shape, M):
    row = str1.split("\n")
    columns = row[0].split('\t')
    units = []
    for h in range(1, len(row)):
        units.append(row[h].split('\t'))
    df1 = pd.DataFrame(units, columns=columns)
    df1 = df1.loc[(df1['conf'] != '-1')]
    df1.iloc[:,:11] = df1.iloc[:,:11].astype(int)

    row = str2.split("\n")
    columns = row[0].split('\t')
    units = []
    for h in range(1, len(row)):
        units.append(row[h].split('\t'))
    df2 = pd.DataFrame(units, columns=columns)
    df2 = df2.loc[(df2['conf'] != '-1')]
    df2.iloc[:,:11] = df2.iloc[:,:11].astype(int)

    x_list = []
    values = []
    for index in df1[df1['left']<shape[1]/2].index:
        if ":" in df1.loc[index, 'text'] and len(df1.loc[index, 'text'])>1:
            if df1.loc[index, 'text'][-1] == ':':
                x_list.append((df1.loc[index, 'left'], df1.loc[index, 'top']))
            elif df1.loc[index, 'text'][0] == ':':
                values.append((df1.loc[index, 'left'],df1.loc[index, 'top'],df1.loc[index, 'text'][1:],''))
            else:
                values.append((df1.loc[index, 'left'],df1.loc[index, 'top'],df1.loc[index, 'text'].split(':')[-1],''))
        elif ":" in df1.loc[index, 'text'] and len(df1.loc[index, 'text'])==1:
            x_list.append((df1.loc[index, 'left'], df1.loc[index, 'top']))
        width = shape[1]
        height = shape[0]
        if df1.loc[index, 'left'] > width*0.08 and df1.loc[index, 'left'] < width*0.114  and df1.loc[index, 'top'] < 2*M:
            values.append((df1.loc[index, 'left'],df1.loc[index, 'top'],df1.loc[index, 'text'],'a'))
        elif df1.loc[index, 'left'] > width*0.172 and df1.loc[index, 'left'] < width*0.2 and df1.loc[index, 'top'] > M and df1.loc[index, 'top'] < 2*M:
            values.append((df1.loc[index, 'left'],df1.loc[index, 'top'],df1.loc[index, 'text'],'b'))
        elif df1.loc[index, 'left'] > width*0.08 and df1.loc[index, 'left'] < width*0.114 and df1.loc[index, 'top'] > 2*M and df1.loc[index, 'top'] < 3*M:
            values.append((df1.loc[index, 'left'],df1.loc[index, 'top'],df1.loc[index, 'text'],'c'))
        elif df1.loc[index, 'left'] > width*0.172 and df1.loc[index, 'left'] < width*0.2 and df1.loc[index, 'top'] > 2*M and df1.loc[index, 'top'] < 3*M:
            values.append((df1.loc[index, 'left'],df1.loc[index, 'top'],df1.loc[index, 'text'],'d'))
        elif df1.loc[index, 'left'] > width*0.033 and df1.loc[index, 'left'] < width*0.097 and df1.loc[index, 'top'] > height*0.705 and df1.loc[index, 'top'] < height*0.791:
            values.append((df1.loc[index, 'left'],df1.loc[index, 'top'],df1.loc[index, 'text'],'e'))
        elif df1.loc[index, 'left'] > width*0.097 and df1.loc[index, 'left'] < width*0.147 and df1.loc[index, 'top'] > height*0.705 and df1.loc[index, 'top'] < height*0.791:
            values.append((df1.loc[index, 'left'],df1.loc[index, 'top'],df1.loc[index, 'text'],'f'))
        if df1.loc[index, 'left'] > width*0.087 and df1.loc[index, 'left'] < width*0.151 and df1.loc[index, 'top'] > height*0.8 and df1.loc[index, 'top'] < height*0.886:
            if ('X'in df1.loc[index, 'text'] or 'x'in df1.loc[index, 'text']) and 'YES'in df1.loc[index, 'text']:
                values.append(('','','YES','g'))
            elif ('X'in df1.loc[index, 'text'] or 'x'in df1.loc[index, 'text']) and 'NO'in df1.loc[index, 'text']:
                values.append(('','','NO','g'))
            else:
                values.append(('','','-','g'))
            
    for i in x_list:
        min = 0
        i_x = i[0]
        i_y = i[1]
        tmp = df1.loc[(df1['left'] > i_x) & (df1['top'] > i_y-M/3) & (df1['top'] < i_y+M/3)]
        min = tmp['left'].min()
        if isinstance(min, int):
            values.append((tmp.loc[tmp['left'] == min,"left"].values[0],tmp.loc[tmp['left'] == min,"top"].values[0],tmp.loc[tmp['left'] == min,"text"].values[0],''))

    for index in df2[df2['left']<shape[1]/2].index:
        width = shape[1]
        height = shape[0]
        x = df2.loc[index, 'left'] + int(width/2)
        y = df2.loc[index, 'top'] 
        if x > width*0.589 and x < width*0.704 and y > height*0.6 and y < height*0.7:
            values.append(('','',df2.loc[index, 'text'],'h'))
        elif x > width*0.59 and x < width*0.7 and y > height*0.774 and y < height*0.86:
            values.append(('','',df2.loc[index, 'text'],'i'))
        elif x > width*0.75 and x < width*0.822 and y > height*0.774 and y < height*0.86:
            values.append(('','',df2.loc[index, 'text'],'j'))
        elif x > width*0.8714 and x < width*0.8951 and y > height*0.774 and y < height*0.86:
            values.append(('','',df2.loc[index, 'text'],'k'))
        elif x > width*0.9049 and x < width*0.9216 and y > height*0.774 and y < height*0.86:
            values.append(('','',df2.loc[index, 'text'],'l'))
        elif x > width*0.9216 and x < width*0.9364 and y > height*0.774 and y < height*0.86:
            values.append(('','',df2.loc[index, 'text'],'m'))
        elif x > width*0.93781 and x < width*0.9648 and y > height*0.774 and y < height*0.86:
            values.append(('','',df2.loc[index, 'text'],'n'))
        elif x > width*0.9648 and y > height*0.774 and y < height*0.86:
            values.append(('','',df2.loc[index, 'text'],'o'))
    return values

if __name__ == '__main__':
    dir = input('folder directory: ')
    list = os.listdir(dir)
    for i in list:
        flag = False
        format = i.split('.')[-1]
        if format == "pdf" or format == "PDF":
            src = dir+"\\"+i[:-4]
            input1 = PdfFileReader(open(src+".pdf", 'rb'))
            if input1.getPage(0).mediaBox[2] < 1800:
                dpi = 290
                flag = True
            else:
                dpi = 160
            img = convert_from_path(dir+"\\"+i, dpi=dpi)[0]
            img = np.array(img) 
            img = img[:, :, ::-1].copy()
            bw = threshold(img) 

            v = vertical(bw, 20)
            if main_area(v, img) != 404:
                new_img, line_x = main_area(v, img)
            else:
                print('Error: Bad pdf file.')
                continue
            new_bw = threshold(new_img)
            h = horizontal(new_bw, 20)
            kernel = np.ones((2,2),np.uint8)
            new_bw = cv2.dilate(new_bw,kernel,iterations = 1)
            new_img = del_text(h, new_bw, line_x)
            new_img = cv2.bitwise_not(new_img)
            cv2.imwrite(src+".jpg",new_img)
            str = pytesseract.image_to_data(new_img,config='--psm 6 -c textord_old_xheight=1  -c tessedit_char_blacklist=([/|\\\"—_])')
            tak_of = analize_right(str, new_img.shape)
    #============================================================

            h = horizontal(bw, 10)
            v = vertical(bw, 40)
            new_img, M = cut(h,v,img)
            str1 = pytesseract.image_to_data(new_img[:,:int(new_img.shape[1]/2)], config='--psm 6 -c textord_old_xheight=1 -c tessedit_char_blacklist=|[]l—')
            if flag:
                new_img = cv2.blur(new_img,(1,1))
                new_img = cv2.adaptiveThreshold(
                    new_img, 255,
                    cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                    25,
                    25
                )
                new_img = cv2.bitwise_not(new_img)
            str2 = pytesseract.image_to_data(new_img[:,int(new_img.shape[1]/2):], config='--psm 6 -c tessedit_char_blacklist=|[]l— ')
            cv2.imwrite(src+".jpg", new_img)
            values = analize_down(str1, str2, new_img.shape, M)
            line, sheet = find_element(values, i, new_img.shape)