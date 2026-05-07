import streamlit as st
import pandas as pd

st.set_page_config(page_title="Parent Student Dashboard", layout="wide")

st.title("Parent Student Dashboard")

# ========================= DATA LOAD =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")      # agar excel hai to pd.read_excel("data.xlsx")
    df = df.fillna("")
    return df

df = load_data()

# ========================= SUMMARY =========================
total_students = len(df)
total_parents = df["Father's Name"].nunique()

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

# ========================= PARENT WISE GROUPING =========================
# Group by Father
parent_group = df.groupby("Father's Name").agg(
    No_of_Children=('S.No', 'count'),
    Children=('Name', lambda x: ", ".join(x)),
    Classes=('New Class', lambda x: ", ".join(x)),
    Max_Class=('New Class', 'max'),   # Senior class ke liye
    Mobile=('Mobile No', 'first')
).reset_index()

# Better Sorting: Zyada bachay + Senior classes ko priority
# Simple sorting for now (aap chahein to aur advanced bhi kar sakte hain)
parent_group = parent_group.sort_values(by='No_of_Children', ascending=False)

st.subheader(f"Parents List ({len(parent_group)} Parents)")

# Search
search = st.text_input("🔍 Search Parent Name", "")

if search:
    filtered = parent_group[parent_group["Father's Name"].str.contains(search, case=False)]
else:
    filtered = parent_group

# Display Parents in Expandable Format
for _, parent in filtered.iterrows():
    with st.expander(f"👨‍👧‍👦 **{parent['Father\'s Name']}**  —  {parent['No_of_Children']} Children", expanded=False):
        st.write(f"**Mobile:** {parent['Mobile']}")
        st.write(f"**Children:** {parent['Children']}")
        st.write(f"**Classes:** {parent['Classes']}")
        
        # Show detailed table of this parent's children
        children_df = df[df["Father's Name"] == parent["Father's Name"]]
        st.dataframe(children_df, use_container_width=True, hide_index=True)

st.caption("Note: Parents with more children are shown on top.")
