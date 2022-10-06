from tracemalloc import Snapshot
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from bs4 import BeautifulSoup
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title="My Scraper", page_icon=":tada:", layout="wide")

with st.container():

    left_column, right_column = st.columns(2)
    with left_column:
        left_column.subheader("Hi, Welcome in Scraper Wuzzuf ")
        left_column.write(
            "I am Enthusiast Student With Data Science and Machine learning and Doing Things That Serve This Fields."
        )
        left_column.write(
            "[For Contact With Us  >](https://www.linkedin.com/in/3hmedgomaa)")
    with right_column:
        def load_lottieurl(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        lottie_coding = load_lottieurl(
            "https://assets3.lottiefiles.com/packages/lf20_kpoaosqz.json")
        st_lottie(lottie_coding, height=240, key="coding")


with st.container():
    st.write("---")
    try:
        try:
            v = int(float(st.text_input('Enter Number of Search Page')))
        except ValueError:
            st.write('')
        x = st.text_input('Enter Field of Search')
        if st.button('Collect'):
            mm = v
            ss = x

            e = '.css-n2jc4m{display:-webkit-inline-box;display:-webkit-inline-flex;display:-ms-inline-flexbox;display:inline-flex;-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-text-decoration:none;text-decoration:none;color:inherit;margin-bottom:4px;}.css-adtuo7{cursor:pointer;padding:0 4px;border-radius:4px;}.css-1ve4b75{font-size:12px;font-weight:600;display:-webkit-inline-box;display:-webkit-inline-flex;display:-ms-inline-flexbox;display:inline-flex;-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;min-height:20px;margin-right:4px;border-radius:2px;max-width:196px;white-space:nowrap;overflow:hidden;cursor:default;text-overflow:ellipsis;padding:2px 4px;background-color:#EBEDF0;color:#001433;cursor:pointer;padding:0 4px;border-radius:4px;}'
            data = ss
            data = data.split(" ")
            P_url = f'https://wuzzuf.net/search/jobs/?a=navbl%7Cspbl&q={data[0]}%20{data[1]}%20%20jobs&start=0'
    except IndexError:
        st.write('')

    page = 0
    job_titles = []
    company_names = []
    location_names = []
    City_Name = []
    Job_posting_time = []
    Job_type = []
    Level_Of_Jobs = []
    Experience_Years = []
    Urls = []
    try:
        while True:

            page_url = f'{P_url[:-1]}{page}'
            result = requests.get(page_url)
            src = result.content
            soup = BeautifulSoup(src, "lxml")

            ad_number = int(soup.find('strong').text)

            job_title = soup.find_all("h2", {"class": "css-m604qf"})
            company_name = soup.find_all("a", {"class": "css-17s97q8"})
            location_name = soup.find_all("span", {"class": "css-5wys0k"})
            Job_posting_times = soup.find_all(
                'div', {"class": ["css-4c4ojb", "css-do6t5g"]})
            Job_types = soup.find_all('div', attrs={'class': 'css-1lh32fc'})
            Level_Of_Job = soup.find_all('div', attrs={'class': 'css-y4udm8'})
            Experience_Year = soup.find_all(
                'div', attrs={'class': 'css-y4udm8'})
            Url = soup.find_all('h2', attrs={'class': 'css-m604qf'})

            page_len = len(company_name)

            try:
                for i in range(page_len):
                    job_titles.append(job_title[i].text.replace(
                        '.css-o171kl{-webkit-text-decoration:none;text-decoration:none;color:inherit;}', ''))
                    company_names.append(
                        company_name[i].text.replace(' -', ''))
                    location_names.append(
                        location_name[i].text.replace(', Egypt', ''))
                    Job_posting_time.append(Job_posting_times[i].text)
                    Job_type.append(Job_types[i].text.replace(e, ''))
                    Level_Of_Jobs.append(Level_Of_Job[i].find(
                        'a',  class_="css-o171kl").text)
                    Experience_Years.append(
                        Experience_Year[i].find('span',  class_=False).text)
                    Urls.append(Url[i].find('a')['href'])
            except:
                Experience_Years.append("0")
                Urls.append("0")

            page += 1
            Endpage = mm
            reached_ad = int(
                soup.find('li', class_='css-8neukt').text.split()[3])
            print(f'Page: {page}, ads: {reached_ad}')

            if reached_ad >= ad_number:
                print('get out')
                break
            if page >= Endpage:
                print('get out')
                break
            time.sleep(1)
    except NameError:
        st.write('')

    for i in range(len(Urls)):
        Urls[i] = "https://wuzzuf.net"+Urls[i]
    for i in range(len(Urls)):
        Urls[i] = Urls[i].replace(
            '?o=1&l=sp&t=sj&a=Machine Learning  jobs|search-v3|hpb|spbl', '')
    for i in range(len(Experience_Years)):
        Experience_Years[i] = Experience_Years[i].replace('· ', '')
    for i in range(len(Job_type)):
        Job_type[i] = Job_type[i].replace('Full Time', 'Full Time  ')
        Job_type[i] = Job_type[i].replace('Work From Home', 'Work From Home  ')
        Job_type[i] = Job_type[i].replace('Shift Based', 'Shift Based  ')
        Job_type[i] = Job_type[i].replace('Freelance / Project', 'Freelance / Project  ')
        Job_type[i] = Job_type[i].replace('Part Time', 'Part Time  ')
    for i in range(len(location_names)):
        Loc = location_names[i].split(',')
        if len(Loc) > 1:
            City_Name.append(Loc[1])
        else:
            City_Name.append('Null')

        location_names[i] = Loc[0]
    if len(job_titles) > 0:
        Data_File = pd.DataFrame({'Title': job_titles, 'Company': company_names, 'Location': location_names, 'City': City_Name, 'Job type': Job_type,
                                 'posting time': Job_posting_time, 'Career Level': Level_Of_Jobs, 'Experience Needed': Experience_Years, "Job_Link": Urls})
        st.write(Data_File)
    try:
        @st.cache
        def convert_df(df):
            return Data_File.to_csv().encode('utf-8')

        csv = convert_df(Data_File)

        st.download_button(
            label="Download File as CSV",
            data=csv,
            file_name='Data_File.csv',
            mime='text/csv',
        )
    except:
        st.write('')

try:
    with st.container():
            st.subheader("Here Some Plots about  Collected Data")
            left_column1, right_column1 = st.columns(2)
            with left_column1:
                plt.figure(figsize=[13, 7])
                plt.xticks(rotation=90)
                ax1 = sns.countplot(
                    Data_File, x='Experience Needed', orient="h")
                ax1.set_title('Number of Most Experience Needed')
                st.pyplot(ax1.get_figure())
            with right_column1:
                ax2 = sns.countplot(Data_File, x='Career Level')
                ax2.set_title('Number of Most Career Level Needed')
                st.pyplot(ax2.get_figure())
    with st.container():
            st.write('---------------------------')
            left_column2, right_column2 = st.columns(2)
            with left_column2:
                plt.figure(figsize=[13, 7])
                plt.xticks(rotation=90)
                ax3 = sns.countplot(Data_File, x='posting time', orient="h")
                ax3.set_title('Distribution of posting time')
                st.pyplot(ax3.get_figure())
            with right_column2:
                ax4 = sns.countplot(Data_File, x='City', orient="h")
                ax4.set_title('Distribution of City')
                st.pyplot(ax4.get_figure())
except:
    st.write('')
try:
    with st.container():
            st.write('---------------------------')
            plt.xticks(rotation=90)
            ax5 = sns.countplot(Data_File, x='Location', orient="h")
            ax5.set_title('Distribution of Location')
            st.pyplot(ax5.get_figure())
except:
        st.write('')
