import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bahria College EAB-1", layout="wide")

# ================== LIGHT NAVY BLUE THEME ==================
st.markdown("""
    <style>
    .stApp {
        background-color: #002B5B;   /* Light Navy Blue */
        color: white;
    }
    .stMetric {
        background-color: #003D80;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #ffffff33;
    }
    h1, h2, h3, .stMarkdown, label {
        color: white !important;
    }
    .stExpander {
        background-color: #003D80;
        border-radius: 12px;
        border: 1px solid #ffffff33;
    }
    .stTextInput input {
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://seeklogo.com/images/P/pakistan-navy-logo-0B0B0B0B0B-seeklogo.com.png", width=120)

with col2:
    st.title("Bahria College EAB-1 Parents Dashboard")
    st.subheader("Principal Ma'am Sabiha Haider")

st.markdown("---")

# ========================= DATA LOAD =========================
@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv("data.csv")
    df = df.fillna("")
    return df

df = load_data()

# ================== SAFE COLUMN DETECTION ==================
def find_column(df, possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

father_col = find_column(df, ["Father's Name", "Father Name", "Fathers Name"])
mobile_col = find_column(df, ["Mobile No", "Mobile", "mobile_no", "Mobile_No"])
fee_col    = find_column(df, ["Fee #", "Fee#", "Fee", "fee_no"])
class_col  = find_column(df, ["New Class", "Class", "new_class"])

# Unique Parent ID (Mobile Number se)
if mobile_col:
    df['Parent_ID'] = df[mobile_col].astype(str) + " - " + df[father_col].astype(str)
else:
    df['Parent_ID'] = df[father_col].astype(str)

# ========================= SUMMARY =========================
total_students = len(df)
total_parents = df['Parent_ID'].nunique()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Students", f"{total_students:,}")
with c2:
    st.metric("Total Unique Parents", f"{total_parents:,}")
with c3:
    st.metric("Average Children per Parent", f"{total_students/total_parents:.2f}")
with c4:
    st.metric("Classes", df[class_col].nunique() if class_col else "N/A")

st.markdown("---")

# ========================= PARENT GROUPING =========================
agg_dict = {
    'Father_Name': (father_col, 'first'),
    'No_of_Children': ('S.No', 'count'),
    'Children': ('Name', lambda x: ", ".join(x)),
    'Classes': (class_col, lambda x: ", ".join(sorted(x))) if class_col else None,
    'Mobile': (mobile_col, 'first') if mobile_col else None,
    'Fee_Number': (fee_col, 'first') if fee_col else None
}
agg_dict = {k: v for k, v in agg_dict.items() if v is not None}

parent_group = df.groupby('Parent_ID').agg(**agg_dict).reset_index()

parent_group = parent_group.sort_values(by='No_of_Children', ascending=False)

st.subheader(f"Parents List ({len(parent_group)} Unique Parents)")

search = st.text_input("🔍 Search Parent Name", "")

if search:
    filtered = parent_group[parent_group["Father_Name"].str.contains(search, case=False)]
else:
    filtered = parent_group

for _, parent in filtered.iterrows():
    with st.expander(f"👨‍👧‍👦 **{parent['Father_Name']}** — {parent['No_of_Children']} Children", expanded=False):
        if mobile_col and 'Mobile' in parent:
            st.write(f"**Mobile:** {parent['Mobile']}")
        if fee_col and 'Fee_Number' in parent:
            st.write(f"**Fee #:** {parent['Fee_Number']}")
        st.write(f"**Children:** {parent['Children']}")
        st.write(f"**Classes:** {parent.get('Classes', 'N/A')}")
        
        children_df = df[df['Parent_ID'] == parent['Parent_ID']]
        st.dataframe(children_df.drop(columns=['Parent_ID'], errors='ignore'), 
                    use_container_width=True, hide_index=True)

# ================== FOOTER ==================
st.markdown("---")
st.markdown("**Powered by HOD Computer Department BC EAB-1**")
st.caption("© Bahria College EAB-1 | All Rights Reserved")
