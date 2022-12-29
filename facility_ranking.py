import pandas as pd
import numpy as np
import streamlit as st
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module

# hide menu and footer
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)  # unsafe_allow_html allows us to embed html code





def generate_excel_download_link(df):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="facility_ranking_SSM.xlsx">Download </a>'
    return st.markdown(href, unsafe_allow_html=True)





# DE=pd.read_csv('C:/Python/1. Dashboard/Facility ranking/Data/DE.csv')
# FPE=pd.read_csv('C:/Python/1. Dashboard/Facility ranking/Data/FPE.csv')
# sd=pd.read_csv('C:/Python/1. Dashboard/Facility ranking/Data/SD.csv')

# width in full screen


st.title('AI Ranking-CPHC Project Jhpiego')
# add two columns
col1, col2 = st.columns(2)
with col1:        
    counts=0

    # file upload
    upload_file_FPE = st.file_uploader("Upload Facility Profile Entry Data in CSV format", type=['csv'])

    # if upload_file_DE is not None highlight "file not uploaded"


    if upload_file_FPE:
        FPE = pd.read_csv(upload_file_FPE)
        
        # check the columns heading available in the file
        required_col=['NIN_2_HFI', 'HFI_Name', 'PHC_CHC_Type',
            'State_Name', 'District_Name', 'Taluka_Name', 'Block_Name',
            'Proposed Date', 'Progressive Date',
            'Total Population in catchment area of facility']
        if set(required_col).issubset(FPE.columns):
            st.subheader("Perfect")
            st.write(FPE.head(3))
        else:
            st.subheader(f"Please upload correct file missing columns are {set(required_col)-set(FPE.columns)}")
            counts=1


    # file upload
    upload_file_DE = st.file_uploader("Upload Daily Entry Data in CSV format", type=['csv'])
    if upload_file_DE:
        DE = pd.read_csv(upload_file_DE)
        
        required_col=['NIN ID',  'Entry Date', 'Footfall Male', 'Footfall Female ',
        'Footfall Others ', 'Footfall Total', 'Patients received medicines ',
        'Patients availed diagnostic tests',
        ' Patients availed tele-consulation services ',
        'Wellness sessions conducted ',
        'Total participants of Wellness session']
        if set(required_col).issubset(DE.columns):
            st.subheader("Perfect")
            st.write(DE.head(3))
        else:
            st.subheader(f"Please upload correct file missing columns are {set(required_col)-set(DE.columns)}")
            counts=1


    # file upload
    upload_file_SD = st.file_uploader("Upload Service Delivery Data in CSV format", type=['csv'])
    if upload_file_SD:
        sd = pd.read_csv(upload_file_SD)
        
        required_col=['NIN ID',  'Entry Month', 
        'HTN Individuals screened Male', 'HTN Individuals screened Female',
        'HTN Individuals screened Other', 'HTN Newly diagnosed Male',
        'HTN Newly diagnosed Female', 'HTN Newly diagnosed Other',
        'HTN On treatment Male', 'HTN On treatment Female',
        'HTN On treatment Other', 'DM Individuals screened Male',
        'DM Individuals screened Female', 'DM Individuals screened Other',
        'DM Newly diagnosed Male', 'DM Newly diagnosed Female',
        'DM Newly diagnosed Other', 'DM On treatment Male',
        'DM On treatment Female', 'DM On treatment Other',
        'OC Individuals screened Male', 'OC Individuals screened Female',
        'OC Individuals screened Other', 'OC Newly diagnosed Male',
        'OC Newly diagnosed Female', 'OC Newly diagnosed Other',
        'OC On treatment male', 'OC On treatment Female',
        'OC On treatment Other', 'BC Individuals screened female',
        'BC Newly diagnosed female', 'BC On treatment female',
        'CC Individuals screened female', 'CC Newly diagnosed female',
        'CC On treatment female', 'Individuals referred for screening male',
        'Individuals referred for screening female',
        'Individuals referred for screening other', 'Newly diagnosed Male',
        'Newly diagnosed Female', 'Newly diagnosed Other', 'On treatment Male',
        'On treatment Female', 'On treatment Other',
        'Total Patients received antihypertensive medicines at this centre',
        'Total Patients received ant-diabetic medicines at this centre',
        'Medicines_TPR_AO_M', 'Total TB patients received DOTS from the centre',
        'Medicines_CSOM_EOM', 'Availability of functional BP apparatus',
        'Availability of functional glucometer', 'Closing stock of glucostrips',
        'Performance/team based incentives for MO/SN/CHO',
        'Team based incentives for ASHA/MPW']
        if set(required_col).issubset(sd.columns):
            st.subheader("Perfect")
            st.write(sd.head(3))
        else:
            st.subheader(f"Please upload correct file missing columns are {set(required_col)-set(sd.columns)}")
            counts=1

    # if upload_file_FPE and upload_file_DE and upload_file_SD is not None:
            # markdown processing
        st.markdown('''
        # *************************Processing Done: Please check next section**************************
        ''')
    st.subheader("This tool is developed by : Surendra Mehta Data Analyst Jhpiego India all rights reserved")
with col2:

    if counts==0 and upload_file_FPE and upload_file_DE and upload_file_SD:
    



        # Facility PE cleaning **********************************************************************************************************
        FPE.rename(columns={'NIN_2_HFI':'NIN ID'}, inplace=True)

        # Total Population in catchment area of facility remove any commas and convert in int format
        FPE['Total Population in catchment area of facility']=FPE['Total Population in catchment area of facility'].replace({',': ''}, regex=True)
        FPE['Total Population in catchment area of facility']=FPE['Total Population in catchment area of facility'].astype(int)

        col=['NIN ID', 'HFI_Name', 'PHC_CHC_Type',
            'State_Name', 'District_Name', 'Taluka_Name', 'Block_Name',
            'Proposed Date', 'Progressive Date',
            'Total Population in catchment area of facility']
        FPE=FPE[col]
        geo=['HFI_Name', 'PHC_CHC_Type','State_Name', 'District_Name', 'Taluka_Name', 'Block_Name']

        # fill NA if any value is missing in geo 
        FPE[geo]=FPE[geo].fillna('NA')
        # total facility 
        total_facility=FPE.shape[0]
        st.write(f"Total facility in facility profile entry is :{total_facility}")

        
        # DE cleaning *******************************************************************************************************************
        #Entry Date convert in date format in format of 2022-05-09
        
        DE['Entry Date'] = pd.to_datetime(DE['Entry Date'], format='%Y-%m-%d')
        DE.head(3)
        # add month-year column from entry date
        DE['Month-Year'] = DE['Entry Date'].dt.strftime('%b-%Y')
        DE['Total'] = DE["Footfall Male"] + DE["Footfall Female "]+DE["Footfall Others "]
        # if wellness session conducted is yes then 1 else 0
        DE['Wellness sessions conducted ']=DE['Wellness sessions conducted '].replace({'Yes': 1, 'No': 0})
        DE['Reporting']=1

        DE_col=['NIN ID','Reporting', 'Total',
            ' Patients availed tele-consulation services ',
            'Wellness sessions conducted ',
                'Month-Year']
        DE=DE[DE_col]
        #groupby
        DE=DE.groupby(['NIN ID','Month-Year']).sum().reset_index()


        #total facility in DE
        st.write(f"Total facility in DE is :{DE['NIN ID'].nunique()}") 

        # SD cleaning ********************************************************************************************************************

        #Entry Date convert in date format in format of 2022-11-30
        sd['Entry Month'] = pd.to_datetime(sd['Entry Month'], format='%Y-%m-%d')

        # # add month-year column from entry date
        sd['Month-Year'] = sd['Entry Month'].dt.strftime('%b-%Y')

        #show all the columns in view
        pd.set_option('display.max_columns', None)

        int_col=['Individuals empanelled',
            'Community Based Assessment Checklist filled',
            'HTN Individuals screened Male', 'HTN Individuals screened Female',
            'HTN Individuals screened Other', 'HTN Newly diagnosed Male',
            'HTN Newly diagnosed Female', 'HTN Newly diagnosed Other',
            'HTN On treatment Male', 'HTN On treatment Female',
            'HTN On treatment Other', 'DM Individuals screened Male',
            'DM Individuals screened Female', 'DM Individuals screened Other',
            'DM Newly diagnosed Male', 'DM Newly diagnosed Female',
            'DM Newly diagnosed Other', 'DM On treatment Male',
            'DM On treatment Female', 'DM On treatment Other',
            'OC Individuals screened Male', 'OC Individuals screened Female',
            'OC Individuals screened Other', 'OC Newly diagnosed Male',
            'OC Newly diagnosed Female', 'OC Newly diagnosed Other',
            'OC On treatment male', 'OC On treatment Female',
            'OC On treatment Other', 'BC Individuals screened female',
            'BC Newly diagnosed female', 'BC On treatment female',
            'CC Individuals screened female', 'CC Newly diagnosed female',
            'CC On treatment female', 'Individuals referred for screening male',
            'Individuals referred for screening female',
            'Individuals referred for screening other', 'Newly diagnosed Male',
            'Newly diagnosed Female', 'Newly diagnosed Other', 'On treatment Male',
            'On treatment Female', 'On treatment Other',
            'Total Patients received antihypertensive medicines at this centre',
            'Total Patients received ant-diabetic medicines at this centre','Medicines_TPR_AO_M',"Closing stock of glucostrips"]


        # convert all the int columns in int format
        sd_int=sd[int_col].head()
        # remove any commas in the int columns
        sd[sd_int.columns] = sd[sd_int.columns].replace({',': ''}, regex=True)
        #convert all the int columns in int format
        sd[int_col] = sd[int_col].apply(pd.to_numeric, errors='coerce', axis=1)

        # add total column in sd_int

        #HTN
        sd['HTN screened '] = sd['HTN Individuals screened Male']+ sd['HTN Individuals screened Female']+ sd['HTN Individuals screened Other']
        sd['HTN diagnosed '] = sd['HTN Newly diagnosed Male']+ sd['HTN Newly diagnosed Female']+ sd['HTN Newly diagnosed Other']
        sd['HTN on treatment '] = sd['HTN On treatment Male']+ sd['HTN On treatment Female']+ sd['HTN On treatment Other']

        #DM
        sd['DM screened '] = sd['DM Individuals screened Male']+ sd['DM Individuals screened Female']+ sd['DM Individuals screened Other']
        sd['DM diagnosed '] = sd['DM Newly diagnosed Male']+ sd['DM Newly diagnosed Female']+ sd['DM Newly diagnosed Other']
        sd['DM on treatment '] = sd['DM On treatment Male']+ sd['DM On treatment Female']+ sd['DM On treatment Other']

        #DM
        sd['OC screened '] = sd['OC Individuals screened Male']+ sd['OC Individuals screened Female']+ sd['OC Individuals screened Other']
        sd['OC diagnosed '] = sd['OC Newly diagnosed Male']+ sd['OC Newly diagnosed Female']+ sd['OC Newly diagnosed Other']
        sd['OC on treatment '] = sd['OC On treatment male']+ sd['OC On treatment Female']+ sd['OC On treatment Other']


        #referred
        sd['TB_Referred'] = sd['Individuals referred for screening male']+ sd['Individuals referred for screening female']+ sd['Individuals referred for screening other']

        #Newly diagnosed
        sd['TB_Newly diagnosed'] = sd['Newly diagnosed Male']+ sd['Newly diagnosed Female']+ sd['Newly diagnosed Other']

        #On treatment
        sd['TB_On treatment'] = sd['On treatment Male']+ sd['On treatment Female']+ sd['On treatment Other']
        # if yes than 1 else 0 add both
        sd["equipments_BP_gluco"]=sd["Availability of functional BP apparatus"].replace({'Yes': 1, 'No': 0})+sd["Availability of functional glucometer"].replace({'Yes': 1, 'No': 0})
        sd["pbi_tbi"]=sd["Performance/team based incentives for MO/SN/CHO"].replace({'Yes': 1, 'No': 0})+sd["Team based incentives for ASHA/MPW"].replace({'Yes': 1, 'No': 0})


        selected_col=['NIN ID', 'Facility Name', 'Facility Type', 'State', 'District',
            'Taluka', 'Block', 'Entry Month',
                    'Month-Year',
            'HTN screened ', 'DM screened ',
            'OC screened ','BC Individuals screened female', 'TB_Referred','equipments_BP_gluco',"pbi_tbi"]
        sd=sd[selected_col]


        # group by NIN-ID and month-year sum
        sd=sd.groupby(['NIN ID','Month-Year']).sum().reset_index()

        # total facility in SD
        st.write("Total facility in SD",sd['NIN ID'].nunique())



        df=pd.merge(DE, sd, on=['NIN ID','Month-Year'], how='outer')
        #merge with FPE
        df=pd.merge(FPE,df, on=['NIN ID'], how='outer')



        #df add a target population column with 80 percent of the total population
        df['Target Population']=round(df['Total Population in catchment area of facility']*0.8,0)



        # # all float value in one list
        # float_col=df.select_dtypes(include=['float']).columns.tolist()

        # # convert all the float columns in int format
        # df[float_col] = df[float_col].apply(pd.to_numeric, errors='coerce', axis=1)

        # cal_Reporting map value>=20 than 15, IF value >=10 than 10 else 0
        df['cal_Reporting']=np.where(df['Reporting']>=20,15,np.where(df['Reporting']>=10,10,0))
        # cal_footfall map if 'Total'/'Target Population'>=1, 15,if 'Total'/'Target Population'>=.8, 10,if 'Total'/'Target Population'>=.5,5, else 0

        df['cal_footfall']=np.where((df['Total']/df['Target Population'])>=1,15,np.where((df['Total']/df['Target Population'])>=.8,10,np.where((df['Total']/df['Target Population'])>=.5,5,0)))
        # Equipment value AV4=2,10,IF value =1,5,0
        df['cal_Equipment']=np.where(df['equipments_BP_gluco']==2,10,np.where(df['equipments_BP_gluco']==1,5,0))
        # pbi_tbi value AV4=2,10,IF value =1,5,0
        df['cal_pbi_tbi']=np.where(df['pbi_tbi']==2,10,np.where(df['pbi_tbi']==1,5,0))
        # tb refered value referred/total >=30,10 ,if referred/total >=20,5, else 0
        df['cal_tb']=np.where((df['TB_Referred']/df['Total'])>=.3,10,np.where((df['TB_Referred']/df['Total'])>=.2,5,0))
        # teleconsultation value AM4>=30,5,IF(AM4>=15,3,IF(AM4>=1,1,0
        df['cal_teleconsultation']=np.where(df[' Patients availed tele-consulation services ']>=30,5,np.where(df[' Patients availed tele-consulation services ']>=15,3,np.where(df[' Patients availed tele-consulation services ']>=1,1,0)))
        # wellness and yoga AQ6>=10,5,IF(AQ6>=5,3,0)
        df['cal_wellness']=np.where(df['Wellness sessions conducted ']>=10,5,np.where(df['Wellness sessions conducted ']>=5,3,0))
        # save the df in csv
        

        # pivot table 
        df_pivot=df.pivot_table(index=["NIN ID","HFI_Name","PHC_CHC_Type","State_Name","District_Name","Taluka_Name","Block_Name"],columns='Month-Year',
        values=['HTN screened ','DM screened ','OC screened ','BC Individuals screened female','cal_Reporting','cal_footfall','cal_Equipment',
            'cal_pbi_tbi','cal_tb','cal_teleconsultation','cal_wellness'],aggfunc='sum').reset_index()

        # total unique facility in all 3 uploaded data
        st.write(f"Total facility in all 3 uploaded data {df_pivot['NIN ID'].nunique()}")

        col=[col[0] + '_' + col[1] for col in df_pivot.columns]
        df_pivot.columns = col
        df_pivot = df_pivot.reset_index()



        # filter all columns having "screened" or refered
        screened_col=[col for col in df_pivot.columns if 'screened' in col]

        # import minmaxscaler
        from sklearn.preprocessing import MinMaxScaler

        # apply minmaxscaler on screened_col
        scaler = MinMaxScaler()
        df_pivot[screened_col] = scaler.fit_transform(df_pivot[screened_col])

        # for each month-year calculate the sum of all the columns 
        unique_month=df['Month-Year'].unique()
        #drop blank value
        unique_month=unique_month[~pd.isnull(unique_month)]

        for i in unique_month:
            df_pivot[i+'_sum']=df_pivot[[col for col in df_pivot.columns if i in col]].sum(axis=1)
            # add rank column and based on sum of each month-year rank the facility
            df_pivot[i+'_rank']=df_pivot[i+'_sum'].rank(ascending=False)



        # For Below month ranking will be calculated st.write(unique_month)
        st.subheader('Below month ranking will be calculated')
        st.write(unique_month)
        
        # calculate the sum of all the month-year sum
        df_pivot['Overall Score']=df_pivot[[col for col in df_pivot.columns if 'sum' in col]].sum(axis=1)


        
        

        # keep only ranking and overall score columns
        sum=[col for col in df_pivot.columns if 'sum' in col]
        rank=[col for col in df_pivot.columns if 'rank' in col]

        # add both list in one list
        sum_rank=sum+rank


        # all sum and rank columns in df_pivot convert in int format
        df_pivot[sum_rank] = df_pivot[sum_rank].apply(pd.to_numeric, errors='coerce', axis=1)

        df_rank=df_pivot[['NIN ID_','HFI_Name_','PHC_CHC_Type_', 'State_Name_','District_Name_','Taluka_Name_',
        'Block_Name_','Overall Score']+sum_rank]

            # df subheader 
        st.subheader("Download the Ranking")
        generate_excel_download_link(df_rank)
        
            # df subheader pivot table
        st.subheader("Detailed calculation download")
        generate_excel_download_link(df_pivot)
        
            # subheader download all 3 files analysis
        st.subheader("Download all 3 files analysis")
        generate_excel_download_link(df)

        # df subheader
        

            
        

