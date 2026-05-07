import streamlit as st
import pandas as pd

# Page Configuration + Navy Blue Theme
st.set_page_config(page_title="Bahria College EAB-1", layout="wide")

# Custom CSS for Navy Blue Background
st.markdown("""
    <style>
    .stApp {
        background-color: #001F3F;
        color: white;
    }
    .stMetric {
        background-color: #003366;
        padding: 10px;
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #FFFFFF !important;
    }
    .stExpander {
        background-color: #003366;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header with Logo
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://seeklogo.com/images/P/pakistan-navy-logo-0B0B0B0B0B-seeklogo.com.png", width=120)

with col2:
    st.title("Bahria College EAB-1 Parents Dashboard")
    st.markdown("**Principal Ma'am Sabiha Haider**")

st.markdown("---")

# ========================= DATA LOAD =========================
@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv("data.csv")
    df = df.fillna("")
    return df

df = load_data()

# ====================== UNIQUE PARENT USING MOBILE ======================
df['Parent_ID'] = df['Mobile No'].astype(str) + " - " + df["Father's Name"].astype(str)

# ========================= SUMMARY =========================
total_students = len(df)
total_parents = df['Parent_ID'].nunique()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Students", f"{total_students:,}")
with col2:
    st.metric("Total Unique Parents", f"{total_parents:,}")
with col3:
    st.metric("Average Children per Parent", f"{total_students/total_parents:.2f}")
with col4:
    st.metric("Classes", df["New Class"].nunique())

st.markdown("---")

# ========================= PARENT GROUPING =========================
parent_group = df.groupby('Parent_ID').agg(
    Father_Name=("Father's Name", 'first'),
    No_of_Children=('S.No', 'count'),
    Children=('Name', lambda x: ", ".join(x)),
    Classes=('New Class', lambda x: ", ".join(sorted(x))),
    Mobile=('Mobile No', 'first'),
    Fee_Number=('Fee #', 'first')
).reset_index()

parent_group = parent_group.sort_values(by='No_of_Children', ascending=False)

st.subheader(f"Parents List ({len(parent_group)} Unique Parents)")

# Search
search = st.text_input("🔍 Search Parent Name", "")

if search:
    filtered = parent_group[parent_group["Father_Name"].str.contains(search, case=False)]
else:
    filtered = parent_group

# Display Parents with Expandable Children
for _, parent in filtered.iterrows():
    with st.expander(f"👨‍👧‍👦 **{parent['Father_Name']}**  —  {parent['No_of_Children']} Children | Mobile: {parent['Mobile']}", expanded=False):
        st.write(f"**Mobile:** {parent['Mobile']}")
        st.write(f"**Fee #:** {parent['Fee_Number']}")
        st.write(f"**Children:** {parent['Children']}")
        st.write(f"**Classes:** {parent['Classes']}")
        
        children_df = df[df['Parent_ID'] == parent['Parent_ID']]
        st.dataframe(children_df.drop(columns=['Parent_ID'], errors='ignore'), 
                    use_container_width=True, hide_index=True)

# ========================= HEADER & FOOTER =========================
st.markdown("---")
st.markdown("**Powered by HOD Computer Department BC EAB-1**")
st.caption("© Bahria College EAB-1 | All Rights Reserved | 2026")
