import pandas as pd
import streamlit as st

# ====================== DATA LOAD ======================
@st.cache_data
def load_data():
    df = pd.read_excel("Final Secy PNET Meeting List.xlsx", sheet_name="Sheet1")
    return df

df = load_data()

# Cleaning
df["Father's Name"] = df["Father's Name"].astype(str).str.strip()
df["Mobile No"] = df["Mobile No"].astype(str).str.strip()

# Better Unique Grouping: Father's Name + Mobile Number
df['Unique_Parent'] = df["Father's Name"] + " | " + df["Mobile No"]

PARENT_COL = "Father's Name"
MOBILE_COL = "Mobile No"

# ====================== GROUPING ======================
parent_groups = df.groupby(['Unique_Parent', PARENT_COL, MOBILE_COL]).agg(
    Total_Children=('Name', 'count'),
    Students=('Name', lambda x: ' | '.join(x)),
    Classes=('New Class', lambda x: ' | '.join(x.astype(str))),
    Family_No=('Family No', 'first'),
    Wing=('Wing', 'first')
).reset_index()

# Sort by children count descending
parent_groups = parent_groups.sort_values(by='Total_Children', ascending=False)

# Drop helper column for display
parent_groups = parent_groups.drop(columns=['Unique_Parent'])

# ====================== STREAMLIT UI ======================
st.set_page_config(page_title="BAHRIA COLLEGE EAB-1 PNET Parent Dashboard", layout="wide")
st.title("🏫 PNET School - Parent Student Dashboard")

st.markdown("**Parents sorted by number of children (Accurate Grouping)**")

# Summary
col1, col2, col3 = st.columns(3)
col1.metric("Total Unique Parents", len(parent_groups))
col2.metric("Total Students", len(df))
col3.metric("Parents with 4+ Children", len(parent_groups[parent_groups['Total_Children'] >= 4]))

# Search
search = st.text_input("🔍 Search by Parent Name", "")

if search:
    filtered = parent_groups[parent_groups[PARENT_COL].str.contains(search, case=False, na=False)]
else:
    filtered = parent_groups

# Main Table
st.subheader(f"📋 Parents List (Total: {len(filtered)})")
st.dataframe(
    filtered,
    column_config={
        "Total_Children": st.column_config.NumberColumn("Bachay", format="%d", width=80),
        "Mobile No": st.column_config.TextColumn("Mobile", width=130),
        "Students": st.column_config.TextColumn("Students", width="large"),
        "Classes": st.column_config.TextColumn("Classes", width="medium"),
    },
    use_container_width=True,
    hide_index=True
)

# Detailed View
st.subheader("👨‍👩‍👧‍👦 Click to see full details")
for _, row in filtered.iterrows():
    with st.expander(f"👨 {row[PARENT_COL]} — **{row['Total_Children']}** bachay"):
        parent_df = df[(df[PARENT_COL] == row[PARENT_COL]) & 
                      (df[MOBILE_COL] == row[MOBILE_COL])]
        
        st.dataframe(
            parent_df[["Name", "New Class", "New Sec", "Mobile No", "Wing", "Fee  #", "Family No"]],
            use_container_width=True,
            hide_index=True
        )
        st.success(f"📞 Mobile: **{row[MOBILE_COL]}**")

st.caption("✅ Now each parent is uniquely identified by Name + Mobile")