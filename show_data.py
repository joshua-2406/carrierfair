import streamlit as st
import psycopg2
import papermill as pm
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
import pandas as pd  # To display the data in Streamlit


# Function to execute Jupyter notebooks
def run_notebook(notebook_path, output_path):
    pm.execute_notebook(
        notebook_path,
        output_path,
        kernel_name='python3'  # Specify the kernel name
    )

# PostgreSQL connection function based on selected database
def get_db_connection(db_name):
    try:
        conn = psycopg2.connect(database = "github_project",user = "postgres",password = "admin",port = "5432",host = "127.0.0.1")
        return conn
    except Exception as e:
        st.error(f"Error connecting to {db_name}: {e}")
        return None

# PostgreSQL data migration function
def datamigration(selected_topic, db_name):
    conn = get_db_connection(db_name)
    if conn is None:
        return

    try:
        cursor = conn.cursor() 

        qry = "select * from " + selected_topic + ";"
        
        # Fetch and display data from the table        
        cursor.execute(qry)
        rows = cursor.fetchall()

        # Convert to pandas DataFrame for better display
        df = pd.DataFrame(rows)
        st.dataframe(df)  # Display the data in Streamlit

    except Exception as e:
        st.error(f"Error in data migration: {e}")
    
    finally:
        cursor.close()
        conn.close()

# Page for PostgreSQL Data Migration

def page_datamigration(is_chart):
    topics = [
        "All Data", "Machine Learning", "Web Development", "Data Science", "Blockchain", "DevOps",
        "Game Development", "Cybersecurity", "Internet of Things", "Mobile Development", "Open Source Tools"
    ]
    
    st.markdown(
        '<span style="color: orange; font-size: 30px; font-weight: bold;">Choose a topic to migrate data to PostgreSQL:</span>',
        unsafe_allow_html=True
    )
    
    selected_topic = st.selectbox("Select the topic", topics)
    st.write(f"You selected: {selected_topic} for PostgreSQL Migration")

    migrate = st.button("Migrate")
    if migrate:
        if is_chart: 
            charts(selected_topic.lower().replace(" ", ""), "github_project")
        else:
            datamigration(selected_topic.lower().replace(" ", ""), "github_project")

# Other pages remain unchanged
def page_DataProcess():
    st.markdown(
        '''
        <div style="background: linear-gradient(to right, #32CD32, #FFD700); padding: 20px; border-radius: 5px;">
            <h1 style="color:#FFF; text-align: center;">Fetch Pre-Process and clean Data here  </h1>
        </div><br>
        ''',
        unsafe_allow_html=True
    )
    # Similar to above, you could add options for processing based on databases as needed.
    

# Streamlit Navigation Menu
selected_page = option_menu(
    menu_title=None,
    options=["Data Process", "PostgreSQL Migration", "Charts", "Insights"],
    icons=["house", "file-earmark-text", "database", "bar-chart", "check-circle", "file-earmark-pdf"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "10!important", "background-color": "purple"},
        "icon": {"font-size": "18px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "text - align": "justify",
            "margin": "0px",
            "background-color": "purple",
            "color": "#FFC0CB",
            "border-radius": "5px",
            "padding": "5px",
        },
        "nav-link-selected": {"background-color": "#FFED20", "font-size": "16px", "font-weight": "10px", "text-align": "center", "color": "#00008A"},
    }
)



def charts(selected_topic, db_name):
    # Read the CSV data
    conn = get_db_connection(db_name)
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        qry = "select * from " + selected_topic + ";"
        
        # Fetch and display data from the table        
        cursor.execute(qry)
        rows = cursor.fetchall()

        # Convert to pandas DataFrame for better display
        data = pd.DataFrame(rows)
        

    except Exception as e:
        st.error(f"Error in data migration: {e}")
    
    finally:
        cursor.close()
        conn.close()
    
    # data.drop('Unnamed: 0', axis=1, inplace=True)

    # Setup Matplotlib style
   #plt.style.use('seaborn-darkgrid')

    # Bar chart for popular programming languages
    x = data['1'].value_counts()
    language_counts_df = x.reset_index()
    language_counts_df.columns = ['1', 'Frequency']

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(language_counts_df['1'], language_counts_df['Frequency'], color='skyblue')
    ax.set_title("Popular Programming Language")
    ax.set_xlabel("Repository Name")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

   
if selected_page == "Data Process":
    page_DataProcess()
elif selected_page == "PostgreSQL Migration":
    page_datamigration(False)
elif selected_page == "Charts":
    page_datamigration(True)
elif selected_page == "Insights":
    page_Insights()

