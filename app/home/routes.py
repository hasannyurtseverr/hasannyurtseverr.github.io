# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask.helpers import send_file
import pandas as pd
from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import numpy as np
import os
import re
import time
from flask import Flask,  session

@blueprint.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    # f1 = open("../output.xls", 'r')   
    path = '../output.xls'
    print(path)
    return send_file('../output.xls',  as_attachment=True, cache_timeout=0)

@blueprint.route('/success', methods = ['POST'])  
def move_forward():
    #Moving forward code
    print("Moving Forward...")
    
    return success()
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)
        f2 = request.files['file2']
        f2.save(f2.filename) 
        print(f)
        print("Başarılı")  
        return deneme(f,f2)
        # return render_template("forms-general.html", name = f.filename)  

def deneme(name,name2):  
    start = time.time()
    print("Timer saymaya başladı...")

    bms_tablosu=name
    device_creatordan_alinan_excel=name2
    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    #Bms tablosundan alınan variableların Integer,Analog,Digital şeklinde filtrelenmesi
    # skiprows ile üst satır alınmıyor, usecols ile sadece B-P arasında ki sütunlar alınıyor.
    # ---------------------------------------------------------------
    bms_table_int = pd.read_excel(bms_tablosu,'Integer',skiprows = 1, usecols = 'B:P')
    bms_table_int=bms_table_int.dropna(subset=['Variable'])

    # ---------------------------------------------------------------
    bms_table_dig = pd.read_excel(bms_tablosu,'Digital',skiprows = 1, usecols = 'B:P')
    bms_table_dig=bms_table_dig.dropna(subset=['Variable'])
    # ---------------------------------------------------------------
    bms_table_analog = pd.read_excel(bms_tablosu,'Analog',skiprows = 1, usecols = 'B:P')
    bms_table_analog=bms_table_analog.dropna(subset=['Variable'])
    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    #Bms tablosundaki verilerinin hepsinin tek bir dataframede birleştirilmesi ve indexlerinin resetlenmesi
    frames=[bms_table_int,bms_table_dig,bms_table_analog]
    bms_table = pd.concat(frames)
    bms_table=bms_table.reset_index(drop=True)
    # ---------------------------------------------------------------
    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    # Değişkenlerin short,long,descr,category gibi kısımlarının alınması
    short_dscr=[]
    variable_name=[]
    long_descr=[]
    bms_adress=[]
    category=[]
    short_name=[]
    long_name=[]
    desc_name=[]
    pv_name=[]
    direction=[]
    for i in range(len(bms_table)):
        short_dscr.append(bms_table['Code1'][i])
        variable_name.append(bms_table['Variable'][i])
        long_descr.append(bms_table['Description'][i])
        bms_adress.append(bms_table['BMS'][i])
        category.append(bms_table['NESNE'][i])
        short_name.append('short')
        desc_name.append('descr')
        long_name.append('long')
        pv_name.append('PV')
        if (bms_table['DataType'][i] == "I"):
            direction.append("Integer")
        if (bms_table['DataType'][i] == "D"):
            direction.append("Digital")
        if (bms_table['DataType'][i] == "A"):
            direction.append("Analog")
    # Değişkenlerin Translations kısmının category hariç yapıştırılcak formata getirilmesi
    short_paste = pd.DataFrame(list(zip(pv_name,variable_name, short_name, short_dscr)),
                    columns =['Section','Item','Key','EN'])
    long_paste = pd.DataFrame(list(zip(pv_name, variable_name, long_name,long_descr)),
                    columns =['Section','Item','Key','EN'])
    desc_paste = pd.DataFrame(list(zip(pv_name, variable_name, desc_name,long_descr)),
                    columns =['Section','Item','Key','EN'])
    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    # Priority kısmı için Mask Koduna göre değişkenleri sıralatıp priority verme işleminin gerçekleştirilmesi
    prio = pd.DataFrame(list(zip(bms_adress,variable_name, short_dscr,category,direction)),
                    columns =['BMS Address','Item','EN','Category','Direction'])
    x=prio.sort_values(by=['EN'])
    z=x.reset_index(drop=True)
    z=z.reset_index()
    end = time.time()
    print(end - start)
    categorytest = np.unique(category)
    end = time.time()
    print(end - start)
    my_dict ={}
    for i in range(len(categorytest)):
        my_dict[categorytest[i]]= 'c_10'+str(i).zfill(2)+''  

    new0=pd.read_excel(device_creatordan_alinan_excel,'Variables',skiprows = 5)
    new0=new0.sort_values(by=['Code'])
    new0=new0.reset_index()
    z=z.sort_values(by=['Item'])
    z=z.reset_index(drop=True)
    end = time.time()
    print(end - start)
    sts=0
    for i in range(len(new0)):
        for j in range (sts,len(z)):
            if (new0['Code'][i] == z['Item'][j]):           
                new0["PV Priority"][i]=z['index'][j]         
                new0["PV Category"][i]=my_dict[z['Category'][j]] 
                if z['Category'][j] == "ALARM":
                    new0["Type"][i]= "Alarm"
                else:
                    new0["Type"][i]=z['Direction'][j]    
                sts=j                   
                break
    new0=new0.replace(False,"False")
    new0=new0.replace(True,"True")
    end = time.time()
    print(end - start)
    # new0=new0.sort_index()
    new0=new0.sort_values(by=['index'])
    new0=new0.drop(["index"],axis=1)
    z=z.sort_index()        
                        
    # prio = pd.DataFrame(list(zip(priorty, priority_name, priority_category,direction_s)),
    #                 columns =['PV Priority','Name','PV Category','Type']) 
    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    # Category kısmı için yapılan düzenlemeler
    category_numeric=[]
    category_key=[]
    category_desc=[]
    pv_for_category=[]
    category_plantvisor=[]

    for i in range(len(categorytest)):
        category_numeric.append('category~'+my_dict[categorytest[i]]+'')
        category_key.append("descr")
        category_desc.append(categorytest[i])
        pv_for_category.append("PV")
        category_plantvisor.append(category_numeric[i][9:])
        
    category_paste=pd.DataFrame(list(zip(pv_for_category,category_numeric, category_key, category_desc)),
                    columns =['Section','Item','Key','EN'])


    PlantVisor = pd.DataFrame(list(zip(category_plantvisor)),
                    columns =['ID']) 
    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    # İnteger değişkenlerinin enum kısımları
    # ---------------------------------------------------------------
    int_enum=bms_table_int.dropna(subset=['Code2'])
    int_enum=int_enum.reset_index(drop=True)
    enum_list_int=[]
    enum_list_int_descr=[]
    enum_list_int_key=[]
    pv_for_enum_list_int=[]
    id_for_enum_int=[]
    User_for_enum_int=[]
    ItemValue_for_enum_int=[]
    for i in range(len(int_enum)):      
        for j in range(int(int_enum['Code2'].iloc[i].split(";")[0].split(":")[0]),int(int_enum['Code2'].iloc[i].split(";")[len(int_enum['Code2'].iloc[i].split(";"))-2].split(":")[0])+1):
            User_for_enum_int.append(' ')
            id_for_enum_int.append(int_enum['Variable'].iloc[i])
            ItemValue_for_enum_int.append(str(j))
            enum_list_int.append(int_enum['Variable'].iloc[i]+'~combo~'+str(j))                
            if int(int_enum['Code2'].iloc[i].split(";")[0].split(":")[0]) == 1:
                j=j-1        
            if int_enum['Code2'].iloc[i].split(";")[j].split(":")[1] == ' ':
                enum_list_int_descr.append("--")
            else:        
                if int_enum['Code2'].iloc[i].split(";")[j].split(":")[1][0] == ' ':
                    enum_list_int_descr.append(int_enum['Code2'].iloc[i].split(";")[j].split(":")[1][1:])
                else:
                    enum_list_int_descr.append(int_enum['Code2'].iloc[i].split(";")[j].split(":")[1])
            enum_list_int_key.append("descr")
            pv_for_enum_list_int.append("PV")    
    PlantVisor_int_enum_paste=pd.DataFrame(list(zip(id_for_enum_int,User_for_enum_int,enum_list_int,ItemValue_for_enum_int)),
                    columns =['ID','User','ItemID','Item Value'])         
    int_enum_paste=pd.DataFrame(list(zip(pv_for_enum_list_int,enum_list_int, enum_list_int_key, enum_list_int_descr)),
                    columns =['Section','Item','Key','EN'])           
    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    
    # ---------------------------------------------------------------
    # Digital değişkenlerinin enum kısımları
    # ---------------------------------------------------------------
    dig_enum=bms_table_dig.dropna(subset=['Code2'])
    dig_enum=dig_enum.reset_index(drop=True)
    enum_list_dig=[]
    enum_list_dig_descr=[]
    enum_list_dig_key=[]
    pv_for_enum_list_dig=[]
    id_for_enum_dig=[]
    User_for_enum_dig=[]
    ItemValue_for_enum_dig=[]
    for i in range(len(dig_enum)):    
        for j in range(int(dig_enum['Code2'].iloc[i].split(";")[0].split(":")[0]),int(dig_enum['Code2'].iloc[i].split(";")[len(dig_enum['Code2'].iloc[i].split(";"))-2].split(":")[0])+1):
            User_for_enum_dig.append(' ')
            id_for_enum_dig.append(dig_enum['Variable'].iloc[i])
            ItemValue_for_enum_dig.append(str(j))        
            enum_list_dig.append(dig_enum['Variable'].iloc[i]+'~combo~'+str(j))        
            if dig_enum['Code2'].iloc[i].split(";")[j].split(":")[1] == ' ':
                enum_list_dig_descr.append("--")
            else:
                if dig_enum['Code2'].iloc[i].split(";")[j].split(":")[1][0] == ' ':
                    enum_list_dig_descr.append(dig_enum['Code2'].iloc[i].split(";")[j].split(":")[1][1:])
                else:
                    enum_list_dig_descr.append(dig_enum['Code2'].iloc[i].split(";")[j].split(":")[1])                   
            enum_list_dig_key.append("descr")
            pv_for_enum_list_dig.append("PV") 
    PlantVisor_dig_enum_paste=pd.DataFrame(list(zip(id_for_enum_dig,User_for_enum_dig,enum_list_dig,ItemValue_for_enum_dig)),
                    columns =['ID','User','ItemID','Item Value'])  
    dig_enum_paste=pd.DataFrame(list(zip(pv_for_enum_list_dig,enum_list_dig, enum_list_dig_key, enum_list_dig_descr)),
                    columns =['Section','Item','Key','EN'])                        
    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    PlantVisor_enum = [PlantVisor_dig_enum_paste, PlantVisor_int_enum_paste]
    PlantVisor_enum = pd.concat(PlantVisor_enum)

    frames2 = [short_paste, long_paste, desc_paste, category_paste,dig_enum_paste, int_enum_paste]
    Translations = pd.concat(frames2)

    # ---------------------------------------------------------------

    temp_device = pd.read_excel("template.xls",'Device')
    df1 = pd.DataFrame([[np.nan] * len(temp_device.columns)], columns=temp_device.columns)
    temp_device = df1.append(temp_device, ignore_index=True)
    
    temp_plantwatch = pd.read_excel("template.xls",'PlantWatch')
    df4 = pd.DataFrame([[np.nan] * len(temp_plantwatch.columns)], columns=temp_plantwatch.columns)
    temp_plantwatch = df4.append(temp_plantwatch, ignore_index=True)
    
    temp_modbus = pd.read_excel("template.xls",'Modbus')
    df5 = pd.DataFrame([[np.nan] * len(temp_modbus.columns)], columns=temp_modbus.columns)
    temp_modbus = df5.append(temp_modbus, ignore_index=True)

    temp_image = pd.read_excel("template.xls",'Images',header=None)
    # df6 = pd.DataFrame([[np.nan] * len(temp_image.columns)], columns=temp_image.columns)
    # temp_image = df6.append(temp_image, ignore_index=True)
    # ---------------------------------------------------------------
    # Variables
    temp_variables = pd.read_excel("template.xls",'Variables')
    df2 = pd.DataFrame([[np.nan] * len(temp_variables.columns)], columns=temp_variables.columns)
    temp_variables = df2.append(temp_variables, ignore_index=True)
    temp_variables = temp_variables.head(6)
    temp_variables.columns = new0.columns
    son_variables= temp_variables.append(new0, ignore_index=True)
    # son_variables.to_excel("output22.xlsx",sheet_name="Variables",index = False, header=False)
    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    # PlantVisor
    temp_plantvisor_variables = pd.read_excel("template.xls",'PlantVisor')
    df3 = pd.DataFrame([[np.nan] * len(temp_plantvisor_variables.columns)], columns=temp_plantvisor_variables.columns)
    temp_plantvisor_variables = df3.append(temp_plantvisor_variables, ignore_index=True)
    temp_plantvisor_variables = temp_plantvisor_variables.head(13)
    temp_plantvisor_variables.columns = PlantVisor_enum.columns
    son_plantvisor= temp_plantvisor_variables.append(PlantVisor_enum, ignore_index=True)
    temp_plantvisor_variables = pd.read_excel("template.xls",'PlantVisor')
    temp_plantvisor_variables_mid=temp_plantvisor_variables.iloc[14:19]
    temp_plantvisor_variables_mid.columns = PlantVisor_enum.columns
    son_plantvisor_2= temp_plantvisor_variables_mid.append(PlantVisor, ignore_index=True)
    son_plantvisor_3= son_plantvisor.append(son_plantvisor_2, ignore_index=True)
    # son_plantvisor_3.to_excel("output22.xlsx",sheet_name="PlantVisor",index = False, header=False)
    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    # Translations
    temp_translations = pd.read_excel("template.xls",'Translations')
    df7 = pd.DataFrame([[np.nan] * len(temp_translations.columns)], columns=temp_translations.columns)
    temp_translations = df7.append(temp_translations, ignore_index=True)
    temp_translations = temp_translations.head(25)
    temp_translations.columns = Translations.columns
    son_translations= temp_translations.append(Translations, ignore_index=True)
    # son_translations.to_excel("output22.xlsx",sheet_name="Translations",index = False, header=False)
    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    # Device Creatordan export edilen excele güncellenmiş hallerinin yapıştırılması için verilen çıktı
    with pd.ExcelWriter('output.xls',engine='openpyxl',
                        mode='w') as writer: 
        temp_device.to_excel(writer,sheet_name="Device",index = False,header=False)
    with pd.ExcelWriter('output.xls',engine='openpyxl',
                        mode='a') as writer:  
        son_variables.to_excel(writer, sheet_name='Variables',index = False,header=False)
    with pd.ExcelWriter('output.xls',engine='openpyxl',
                        mode='a') as writer:  
        son_plantvisor_3.to_excel(writer, sheet_name='PlantVisor',index = False,header=False)
    with pd.ExcelWriter('output.xls',engine='openpyxl',
                        mode='a') as writer:  
        temp_plantwatch.to_excel(writer, sheet_name='PlantWatch',index = False,header=False)
    with pd.ExcelWriter('output.xls',engine='openpyxl',
                        mode='a') as writer:  
        temp_modbus.to_excel(writer, sheet_name='Modbus',index = False,header=False)
    with pd.ExcelWriter('output.xls',engine='openpyxl',
                        mode='a') as writer:  
        temp_image.to_excel(writer, sheet_name='Images',index = False,header=False)
    with pd.ExcelWriter('output.xls',engine='openpyxl',
                        mode='a') as writer:  
        son_translations.to_excel(writer, sheet_name='Translations',index = False,header=False)                           
    end = time.time()
    print(end - start)
    return html_table2(son_variables,son_plantvisor_3,son_translations,temp_device,temp_plantwatch,temp_modbus,temp_image)

def html_table2(df2,df3,df7,df1,df4,df5,df6):
    print("test2")
    return render_template('device.html',  tables2=[df2.to_html(classes='table table-bordered table-striped',table_id="tbl2")],titles=df2.columns.values,
    tables3=[df3.to_html(classes='table table-bordered table-striped',table_id="tbl3")],
    tables7=[df7.to_html(classes='table table-bordered table-striped',table_id="tbl7")],   
    tables1=[df1.to_html(classes='table table-bordered table-striped',table_id="tbl1")],
    tables4=[df4.to_html(classes='table table-bordered table-striped',table_id="tbl4")],
    tables5=[df5.to_html(classes='table table-bordered table-striped',table_id="tbl5")],
    tables6=[df6.to_html(classes='table table-bordered table-striped',table_id="tbl6")])

@blueprint.route('/index')
@login_required
def index():

    return render_template('index.html', segment='index.html')

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
