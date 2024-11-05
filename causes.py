import streamlit as st
import pandas as pd
import plotly.express as px

# Function to get data from Excel
@st.cache_resource
def get_data_from_excel():
    df = pd.read_excel("causes.xlsx", engine="openpyxl", sheet_name="causes", usecols="A:H", nrows=818)
    return df

# Set the Streamlit app theme to light

st.set_page_config(page_title="Causes", page_icon=":bar_chart:", layout="centered")

# Load the data using the function
df = get_data_from_excel()

# Load the data using the function
df = get_data_from_excel()

# Add filter widgets for "Cause", "Age", "Country", and "Rank" in the four columns
Risk = st.multiselect("Select the  Risk Factor:", options=df["Risk"].unique(), default=df["Risk"].unique())

col1, col2, col3 = st.columns(3)

# Get the unique age values
age_options = sorted(df["Age"].unique())

# Define the indices to hide
indices_to_hide = [1, 3, 5, 7]

# Create a filtered list of age options without the specified indices
filtered_age_options = [age for index, age in enumerate(age_options) if index not in indices_to_hide]

with col1:
    Age = st.selectbox("Select an Age:", options=filtered_age_options, index=0)

with col2:
    Nationality = st.selectbox("Select a Nationality:", options=sorted(df["Nationality"].unique()), index=0)

with col3:
    Rank = st.selectbox("Select a Rank:", options=sorted(df["Rank"].unique()), index=2)

# Filter the data based on user selections
df_selection = df.query(
    "Risk==@Risk & Age==@Age & Rank==@Rank & Nationality==@Nationality"
)

title = f"Risk Factors, {Rank}"
st.markdown(f"<h3 style='black: red;text-align: center'> {title}</h3>", unsafe_allow_html=True)

# Create a bar chart using Plotly with "Risk" as a legend and "95% CI" as labels

if not df_selection.empty:
    # Create a bar chart with 'Age' as a subplot
    fig = px.bar(df_selection, x='Nationality', y='Number of cases', color='Risk', text='Prevalence', facet_col='Age')
    
    # Adjust the width of the bars to center-align them
    fig.update_traces(marker=dict(line=dict(width=0)))  # Adjust the 'width' as needed

    left, middle, right = st.columns((1, 10, 1))
    with middle:
        st.plotly_chart(fig)
else:
    st.warning('No data available for the selected options.')



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)