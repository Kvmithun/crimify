import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# reading the dataset
crime = pd.read_csv("crime.csv")

# replacing inconsistent district name
crime['DISTRICT'] = crime['DISTRICT'].replace('BANGALORE COMMR.', 'Bangalore Urban')


# function for overall level crime analysis
def overall_analysis():
    # total number of crimes from 2000 to 2012
    st.subheader(f'The total number of crimes from 2000–2012: {crime["TOTAL IPC CRIMES"].sum():,}')

    # year in which crime was maximum
    st.subheader(
        f'The year in which maximum crimes commited: {crime.groupby("YEAR")["TOTAL IPC CRIMES"].sum().idxmax()}')

    # creating two columns for displaying stats and chart
    col1, col2 = st.columns(2)

    with col1:
        # average crime per year as a table
        st.subheader("Average crime per year")
        st.dataframe(crime.groupby('YEAR')['TOTAL IPC CRIMES'].mean().astype("int"))

    with col2:
        # line graph showing crime trend over years
        st.subheader("Crime trend over years")
        yearly_crime = crime.groupby('YEAR')['TOTAL IPC CRIMES'].sum()
        fig, ax = plt.subplots()
        ax.plot(yearly_crime.index, yearly_crime.values, marker='o')
        ax.set_title("Total IPC Crimes per Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total IPC Crimes")
        ax.grid(True)
        st.pyplot(fig)

    # top 10 states by total ipc crimes
    st.subheader("Top 10 States by Total Crimes")

    # showing data of top 10 states
    st.subheader('Data')
    st.dataframe(crime.groupby('STATE/UT')['TOTAL IPC CRIMES'].sum().sort_values(ascending=False).head(10))

    # bar chart of top 10 states
    st.subheader('Graphical Representation')
    top_states = crime.groupby('STATE/UT')['TOTAL IPC CRIMES'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    top_states.plot(kind='bar', ax=ax, color='tomato')
    ax.set_title("Top 10 States/UTs by Total IPC Crimes")
    ax.set_xlabel("State/UT")
    ax.set_ylabel("Total IPC Crimes")
    ax.grid(True)
    st.pyplot(fig)

    # calculating percentage distribution of different crime types
    crime_types = [
        'MURDER', 'ATTEMPT TO MURDER', 'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER',
        'RAPE', 'CUSTODIAL RAPE', 'OTHER RAPE', 'KIDNAPPING & ABDUCTION',
        'KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS',
        'KIDNAPPING AND ABDUCTION OF OTHERS', 'DACOITY',
        'PREPARATION AND ASSEMBLY FOR DACOITY', 'ROBBERY', 'BURGLARY', 'THEFT',
        'AUTO THEFT', 'OTHER THEFT', 'RIOTS', 'CRIMINAL BREACH OF TRUST',
        'CHEATING', 'COUNTERFIETING', 'ARSON', 'HURT/GREVIOUS HURT',
        'DOWRY DEATHS', 'ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY',
        'INSULT TO MODESTY OF WOMEN', 'CRUELTY BY HUSBAND OR HIS RELATIVES',
        'IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES',
        'CAUSING DEATH BY NEGLIGENCE', 'OTHER IPC CRIMES'
    ]

    # pie chart of top 10 crime types by percentage
    st.subheader('Crime Distribution using Graph')
    crime_percent = ((crime[crime_types].sum().sort_values(ascending=False)) / crime['TOTAL IPC CRIMES'].sum()) * 100
    top_10_crime_percent = crime_percent.head(10)
    fig, ax = plt.subplots()
    ax.pie(top_10_crime_percent, labels=top_10_crime_percent.index, autopct='%1.1f%%', startangle=90)
    ax.set_title("Top 10 Crime Types by % Contribution to Total IPC Crimes")
    st.pyplot(fig)


# function to show state wise analysis
def state_analysis(state):
    # year in which most crimes were reported in the selected state
    Most = crime[crime['STATE/UT'] == state].groupby('YEAR')['TOTAL IPC CRIMES'].sum().idxmax()
    no = crime[crime['STATE/UT'] == state].groupby('YEAR')['TOTAL IPC CRIMES'].sum().max()
    st.text(f'The  Most  Crimes  Were  Recorded  in  {Most}  With :  {no} crimes')

    # total crimes in each district of that state
    st.subheader("Total crimes in Each District")
    st.dataframe(
        crime[crime['STATE/UT'] == state].groupby('DISTRICT')['TOTAL IPC CRIMES'].sum().sort_values(ascending=False))

    # crime trend over years in selected state
    st.subheader(f'Trend of Crime over the Years in : {state}')
    karnataka_crime_trend = crime[crime['STATE/UT'] == 'KARNATAKA'].groupby('YEAR')['TOTAL IPC CRIMES'].sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(karnataka_crime_trend.index, karnataka_crime_trend.values, marker='o', color='blue')
    ax.set_title("Crime Trend in Karnataka (2000–2012)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total IPC Crimes")
    ax.grid(True)
    st.pyplot(fig)

    # getting district with highest crime per year
    st.subheader("The City With Most No of Crimes Over Years")
    crime_clean = crime[(crime['STATE/UT'] == state) & (crime['DISTRICT'] != 'TOTAL')]
    a = crime_clean[crime['STATE/UT'] == state].groupby(['DISTRICT', 'YEAR'])['TOTAL IPC CRIMES'].sum().reset_index()
    b = a.loc[a.groupby('YEAR')['TOTAL IPC CRIMES'].idxmax()]
    st.dataframe(b)

    # top 5 districts with high crime
    st.subheader("Top 5 District Where Crime is High")
    aa = crime[crime["DISTRICT"] != "TOTAL"]
    st.dataframe(
        aa[aa['STATE/UT'] == state].groupby("DISTRICT")['TOTAL IPC CRIMES'].sum().sort_values(ascending=False).head(
            6).index)

    # top 5 districts by rape cases
    st.subheader("Top 5 District With Most No of Rape Cases")
    st.dataframe(aa[aa['STATE/UT'] == state].groupby("DISTRICT")['RAPE'].sum().sort_values()[::-1].head(5))


# function to show district level analysis
def district_analysis(state, district):
    # crime trend in selected district
    st.subheader(f" Crime Trend in {district}, {state}")
    district_df = crime[(crime['STATE/UT'] == state) & (crime['DISTRICT'] == district)]
    yearly = district_df.groupby('YEAR')['TOTAL IPC CRIMES'].sum()
    fig, ax = plt.subplots()
    ax.plot(yearly.index, yearly.values, marker='o', color='green')
    ax.set_title(f"Total IPC Crimes in {district}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Crimes")
    ax.grid(True)
    st.pyplot(fig)

    # rape case trend in that district
    st.subheader(f" Rape Cases in {district}")
    if 'RAPE' in district_df.columns:
        rape_trend = district_df.groupby('YEAR')['RAPE'].sum()
        st.line_chart(rape_trend)
    else:
        st.warning("RAPE column not found in data.")

    # top crime types in that district
    st.subheader(" Most Reported Crime Types")
    crime_columns = [
        'MURDER', 'RAPE', 'THEFT', 'RIOTS', 'BURGLARY', 'CHEATING',
        'ARSON', 'DOWRY DEATHS', 'KIDNAPPING & ABDUCTION',
        'CRUELTY BY HUSBAND OR HIS RELATIVES'
    ]
    existing = [col for col in crime_columns if col in district_df.columns]
    total_crime_types = district_df[existing].sum().sort_values(ascending=False)
    st.bar_chart(total_crime_types.head(7))


# sidebar menu
st.sidebar.title("Crime Pattern Analysis")
opt = st.sidebar.selectbox('', ['', 'Overall Analysis', 'State Wise Analysis', 'District Wise Analysis'])

# homepage content
if opt == '':
    st.title("crimify")
    st.subheader('India Crime Dashboard (2000–2012)')
    st.write("Crimify is an interactive dashboard designed to visualize district-wise "
             "IPC (Indian Penal Code) crime data across India from 2000 to 2012."
             " It enables users to explore national crime trends, analyze state and "
             "district-level data, and compare crime statistics across different years."
             " Crimify aims to provide clear insights into how various types of crimes"
             " have evolved over time, helping researchers, analysts, and policymakers identify patterns, "
             "hotspots, and areas of concern for better decision-making and public awareness.")

# when user selects overall analysis
elif opt == 'Overall Analysis':
    st.title("crimify")
    st.header('India Crime Dashboard (2000–2012)')
    st.header("Overall Analysis")
    overall_analysis()

# when user selects state wise analysis
elif opt == 'State Wise Analysis':
    st.title("crimify")
    st.header('India Crime Dashboard (2000–2012)')
    st.header("State Wise Analysis")
    state = st.sidebar.selectbox('Select the State', sorted(crime['STATE/UT'].unique()))
    btn2 = st.sidebar.button("Find State Details")
    if btn2:
        state_analysis(state)

# when user selects district wise analysis
elif opt == "District Wise Analysis":
    st.title("crimify")
    st.header('India Crime Dashboard (2000–2012)')
    st.header("District Wise Analysis")

    # select state and district from sidebar
    selected_state = st.sidebar.selectbox("Select State", sorted(crime['STATE/UT'].unique()))
    filtered_districts = crime[crime['STATE/UT'] == selected_state]['DISTRICT'].unique()
    selected_district = st.sidebar.selectbox("Select District", sorted(filtered_districts))

    # show analysis for selected district
    if st.sidebar.button("Show District Insights"):
        district_analysis(selected_state, selected_district)
