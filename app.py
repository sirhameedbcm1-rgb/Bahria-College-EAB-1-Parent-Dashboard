import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bahria College EAB-1", layout="wide")

# ================== LIGHT BLUE THEME ==================
st.markdown("""
    <style>
    .stApp {
        background-color: #E6F0FF;
        color: #003366;
    }
    h1, h2, h3 {
        color: #003366 !important;
    }
    .stMetric {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 2px solid #003366;
    }
    .stExpander {
        background-color: white;
        border: 1px solid #003366;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.title("Bahria College EAB-1 Parents Dashboard")
st.subheader("Principal Ma'am Sabiha Haider")
st.markdown("**Powered by HOD Computer Department BC EAB-1**")
st.markdown("---")

# ========================= DATA LOAD =========================
@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv("data.csv")
    df = df.fillna("")
    return df

df = load_data()

# ================== UNIQUE PARENT ID USING S.No ==================
df['Parent_ID'] = df['S.No'].astype(str) + " - " + df["Father's Name"].astype(str)

# ========================= SUMMARY =========================
total_students = len(df)
total_parents = df['Parent_ID']

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Students", f"{total_students:,}")
with c2:
    st.metric("Total Unique Parents", f"{total_parents:,}")
with c3:
    st.metric("Average Children per Parent", f"{total_students/total_parents:.2f}")
with c4:
    st.metric("Classes", df["New Class"].nunique() if "New Class" in df.columns else "N/A")

st.markdown("---")

# ========================= PARENT GROUPING (Safe) =========================
parent_group = df.groupby('Parent_ID').agg(
    Father_Name=("Father's Name", "first"),
    No_of_Children=("S.No", "count"),
    Children=("Name", lambda x: ", ".join(x)),
    Classes=("New Class", lambda x: ", ".join(sorted(x))),
    Mobile=("Mobile No", "first"),
).reset_index()

# Fee column agar ho to add kar do (safe way)
if "Fee #" in df.columns:
    parent_group["Fee_Number"] = df.groupby('Parent_ID')["Fee #"].first().values
elif "Fee" in df.columns:
    parent_group["Fee_Number"] = df.groupby('Parent_ID')["Fee"].first().values

parent_group = parent_group.sort_values(by="No_of_Children", ascending=False)

st.subheader(f"Parents List ({len(parent_group)} Unique Parents)")

# Search
search = st.text_input("🔍 Search Parent Name", "")

if search:
    filtered = parent_group[parent_group["Father_Name"].str.contains(search, case=False)]
else:
    filtered = parent_group

# ================== SHOW PARENTS & THEIR CHILDREN ==================
for _, parent in filtered.iterrows():
    with st.expander(f"👨‍👧‍👦 **{parent['Father_Name']}** — {parent['No_of_Children']} Children", expanded=False):
        
        if 'Mobile' in parent:
            st.write(f"**Mobile:** {parent['Mobile']}")
        if 'Fee_Number' in parent:
            st.write(f"**Fee #:** {parent['Fee_Number']}")
            
        st.write(f"**Children:** {parent['Children']}")
        st.write(f"**Classes:** {parent['Classes']}")
        
        # Show full details of children
        children_df = df[df['Parent_ID'] == parent['Parent_ID']]
        st.dataframe(children_df.drop(columns=['Parent_ID'], errors='ignore'), 
                    use_container_width=True, hide_index=True)

# ================== FOOTER ==================
st.markdown("---")
st.markdown("**Powered by HOD Computer Department BC EAB-1**")
st.caption("© Bahria College EAB-1 | All Rights Reserved")
