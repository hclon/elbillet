import streamlit as st
import pandas as pd
from streamlit.components.v1 import html

import datetime

st.set_page_config(page_title="Dashboard", layout ="wide")

  
@st.cache
def load_excel():
    df = pd.concat(pd.read_excel('ListEleve.xlsx', usecols='A:G',engine='openpyxl',sheet_name=None), ignore_index=True)
        #df = pd.read_excel('ListEleve.xlsx',engine='openpyxl',sheet_name='2BACLF-1',usecols='A:G')
        # df['OrderDate']= pd.to_datetime(df['Order Date']).dt.strftime('%d-%b-%Y')
        #df['year']= pd.to_datetime(df['OrderDate']).dt.strftime('%Y')
        #df['month']= pd.to_datetime(df['OrderDate']).dt.strftime('%b')
    df['nomComplet'] = df.Nom+" "+df.Prenom
    cl=""
    return df 

df = load_excel()





st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)
st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{padding-left:2px;} label.st-d2{width:130px}</style>', unsafe_allow_html=True)

   
C1,C2,C3,C4 = st.columns([1,5,5,1])
with C2:
            genre = st.radio("", ('الغياب','تأخر'))
            code = st.text_input('رمز مسار', '', key='code',on_change=load_excel)

            with st.expander("بحث متقدم"):
                #nom = st.text_input('الاسم الكامل', '')
                
                cyc = st.radio("", ('إعدادي', 'تأهيلي','تقني'))
                if cyc == 'إعدادي':
                    Mos = st.radio("", ('1APC', '2APC','3APC'))
                if cyc == 'تأهيلي' or cyc == 'تقني':
                    Mos = st.radio("", ('TC', '1BAC','2BAC'))
                
                
                if Mos == "1APC":
                    cl =st.selectbox('الأقسام', ('','1APC 1', '1APC 1', '1APC 3'))
                if Mos == "2APC":
                    cl =st.selectbox('الأقسام', ('','2APC 1', '2APC 1', '2APC 3'))
                if Mos == "3APC":
                    cl =st.selectbox('الأقسام', ('','3APC 1', '3APC 1', '3APC 3'))
                if Mos == "TC":
                    cl =st.selectbox('الأقسام', ('','3APC 1', '3APC 1', '3APC 3'))
                if Mos == "1BAC":
                    cl =st.selectbox('الأقسام', ('','1BACSHF-1', '1BACSHF-2', '1BACSHF-3'))
                if Mos == "2BAC":
                    cl =st.selectbox('الأقسام', ('','2BACLF-1', '2BACSHF-1', '2BACSHF-2'))

                if cl != '':
                    df_classe = pd.read_excel('ListEleve.xlsx',engine='openpyxl',sheet_name=cl,usecols='A:G')
                    df_classe['nomComplet'] = df_classe.Nom+" "+df_classe.Prenom
                    listLearner = dict(zip(df_classe['الرمز'], df_classe.nomComplet))
                    
                    def format_func(option):
                        return listLearner[option]

                    selectedLeaner = st.selectbox("التلاميد", options=list(listLearner.keys()), format_func=format_func)
                    #st.write(f"You selected option {selectedLeaner} called {format_func(selectedLeaner)}")
                    #st.dataframe(df)
                    code =selectedLeaner
with C3:
            if code:
                df_selection = df.query('الرمز==@code')
                nm = df_selection.to_string(columns=['nomComplet'], header=False, index=False)
                cl = df_selection.to_string(columns=['Classe'], header=False, index=False)
                now = datetime.datetime.now()
                d = now.strftime("%Y-%m-%d")
                h = now.strftime("%H:%M")
                tag = "<table width='300px' id='table'>"
                tag = tag + "<tr>  <td class='quantity' colspan='2'> </td>  "  
                tag = tag + "<tr>  <td class='quantity'>"+ h +"</td>  <td class='description'>على الساعة</td> <tr>"
                tag = tag + "<tr>  <td class='quantity'>"+ nm +"</td>  <td class='description'>يرجى السماح   للتلميذ(ة)</td> <tr>"
                tag = tag + "<tr>  <td class='quantity'>"+ cl +"</td>  <td class='description'>المستوى</td> <tr></table>"
                st.write(tag, unsafe_allow_html=True)     
                if st.button('Print',key="print"):
                    
                    nm = df_selection.to_string(columns=['nomComplet'], header=False, index=False)
                    cl = df_selection.to_string(columns=['Classe'], header=False, index=False)

                    tag = "<table>  <tr>  <td class='quantity'>"+ d +"</td>  <td class='description'>ليوم</td> <tr>"  
                    tag = tag + "<tr>  <td class='quantity'>"+ h +"</td>  <td class='description'>على الساعة</td> <tr>"
                    tag = tag + "<tr>  <td class='quantity'>"+ nm +"</td>  <td class='description'>يرجى السماح   للتلميذ(ة)</td> <tr></table>"
                    tag = tag + "<tr>  <td class='quantity'>"+ cl +"</td>  <td class='description'>المستوى</td> <tr></table>"
                    
                    my_js = """
                        document.addEventListener("DOMContentLoaded", function(event) { 
                            var WinPrint = window.open('', '', 'left=0,top=0,width=800,height=900,toolbar=0,scrollbars=0,status=0');
                            WinPrint.document.write(" """+ tag+ """ ");
                            WinPrint.document.close();
                            WinPrint.focus();
                            WinPrint.print();
                            WinPrint.close();
                        });
                        
                    """
                    my_html = f"<script>{my_js}</script>"
                    html(my_html)
st.write('<hr>', unsafe_allow_html=True)

        #st.sidebar.camera_input("Profil")
st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css?family=Open+Sans');
        div[data-testid="metric-container"] {
        margin: 0px auto;
        max-width: 300px;
        border-radius: 10px;
        border-width: 1px;
        border-style: solid;
        border-color="#777";
        overflow: hidden;
        background-clip: padding-box;
        padding: 15px 5px 15px 40%;
        text-align: left;
        font-weight: 400 !important;
        font-family: Open sans;
        color: #172B4C;
        
        }


        /* breakline for metric text         */
        div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
            font-family: Open sans;
            font-size:16px;
            font-weight: 100;
        overflow-wrap: break-word;
        white-space: break-spaces;
        color: #595C5F;
        }
        .css-18e3th9 {
            top:-80px;
        }
        #table{
            margin: 50px 5px 15px 50px;
        }

        .stButton{
            margin: 10px 5px 15px 50px;
        }

        </style>
        """
        , unsafe_allow_html=True)

        





