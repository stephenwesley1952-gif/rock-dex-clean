import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE CONFIGURATION & SESSION STATE
# ==========================================
st.set_page_config(
    page_title="RockDex - Mineral & Fossil Cataloger",
    page_icon="💎",
    layout="wide"
)

# Initialize Session State for Collection Catalog
if "collection" not in st.session_state:
    st.session_state.collection = []

# Initialize Session State for Test Wizard
if "test_hardness" not in st.session_state:
    st.session_state.test_hardness = "Unknown"
if "test_acid" not in st.session_state:
    st.session_state.test_acid = "No Reaction"
if "test_luster" not in st.session_state:
    st.session_state.test_luster = "Non-metallic"

# ==========================================
# 2. APP HEADER & NAVIGATION
# ==========================================
st.title("💎 RockDex")
st.caption("Mineral, Rock, and Fossil Identification & Cataloging Tool")

tab1, tab2, tab3 = st.tabs([
    "🔍 Rock & Mineral ID", 
    "🧪 Physical Test Wizard", 
    "📚 Personal Collection Catalog"
])

# ==========================================
# TAB 1: ROCK & MINERAL ID
# ==========================================
with tab1:
    st.header("Specimen Identification")
    st.write("Use the quick selector below to evaluate and classify your specimens based on key diagnostic features.")
    
    col_sel, col_out = st.columns([1, 1])
    
    with col_sel:
        category = st.selectbox(
            "Primary Specimen Category",
            ["Quartz / Silica Family", "Sulfide Minerals", "Carbonate Minerals", "Fossils / Host Rock"]
        )
        
        if category == "Quartz / Silica Family":
            sub_type = st.radio(
                "Observed Texture / Form",
                ["Banded / Smooth Chert", "Vuggy / Micro-druzy Quartz", "Fossiliferous Chert"]
            )
            if sub_type == "Banded / Smooth Chert":
                specimen_name = "Banded Chert"
                hardness_val = "7"
                desc = "Microcrystalline quartz displaying distinct color banding, dense fracture, and waxy to dull luster."
            elif sub_type == "Vuggy / Micro-druzy Quartz":
                specimen_name = "Micro-druzy Quartz in Vug"
                hardness_val = "7"
                desc = "Cavity (vug) lined with tiny, sparkling quartz crystals coating chert or limestone matrix."
            else:
                specimen_name = "Fossiliferous Chert"
                hardness_val = "7"
                desc = "Chert matrix replacing or embedding ancient marine fossils (crinoids, bryozoans, brachiopods)."
                
        elif category == "Sulfide Minerals":
            sub_type = st.radio(
                "Metallic Appearance & Color",
                ["Lead-gray / Cubic Cleavage (Galena)", "Resinous / Yellow-Brown-Black (Sphalerite)"]
            )
            if "Galena" in sub_type:
                specimen_name = "Galena"
                hardness_val = "2.5"
                desc = "Lead sulfide. High specific gravity (very heavy), bright metallic luster, perfect cubic cleavage."
            else:
                specimen_name = "Sphalerite"
                hardness_val = "3.5 - 4"
                desc = "Zinc sulfide. Resin-like to sub-metallic luster, light yellow to dark brown/black, pale yellow streak."
                
        elif category == "Carbonate Minerals":
            specimen_name = "Calcite"
            hardness_val = "3"
            desc = "Calcium carbonate. Rhombohedral cleavage, readily effervesces (fizzes) with weak acid."
            
        else:
            specimen_name = "Fossil Specimen (Marine)"
            hardness_val = "3 - 7 (depends on replacement)"
            desc = "Preserved remains or molds of prehistoric organisms commonly found in chert or limestone matrix."

    with col_out:
        st.subheader("Identification Summary")
        st.metric(label="Identified Specimen", value=specimen_name)
        st.write(f"**Mohs Hardness:** {hardness_val}")
        st.info(f"**Description:** {desc}")
        
        # Add to collection button
        if st.button("➕ Add Identified Specimen to Catalog"):
            new_entry = {
                "Specimen": specimen_name,
                "Hardness": hardness_val,
                "Category": category,
                "Notes": desc
            }
            st.session_state.collection.append(new_entry)
            st.success(f"Added **{specimen_name}** to your collection catalog!")

# ==========================================
# TAB 2: PHYSICAL TEST WIZARD
# ==========================================
with tab2:
    st.header("Physical Diagnostics & Scratch Tests")
    st.write("Perform standard physical tests on your unkown specimen to narrow down possible mineral matches.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("1. Scratch Test")
        hardness_test = st.selectbox(
            "Hardness Result",
            [
                "Scratched by fingernail (< 2.5)",
                "Scratched by copper penny (2.5 - 3.5)",
                "Scratched by steel nail/blade (3.5 - 5.5)",
                "Scratches glass knife/plate (> 5.5 - 7)",
                "Scratches quartz (> 7)"
            ],
            key="w_hardness"
        )
        
    with col2:
        st.subheader("2. Luster")
        luster_test = st.selectbox(
            "Surface Reflection",
            ["Metallic (Looks like metal)", "Waxy / Resinous", "Vitreous (Glassy)", "Dull / Earthy", "Sparkly / Micro-sparkling"],
            key="w_luster"
        )
        
    with col3:
        st.subheader("3. Acid Test")
        acid_test = st.selectbox(
            "Acid / Vinegar Reaction",
            ["No Reaction", "Weak Fizzing (Powdered)", "Strong Effervescence (Immediate)"],
            key="w_acid"
        )

    st.markdown("---")
    st.subheader("Diagnostic Suggestions")
    
    if "Fingernail" in hardness_test:
        st.write("📌 **Potential Matches:** Gypsum, Talc, Soft Clays.")
    elif "penny" in hardness_test:
        if "Effervescence" in acid_test or "Fizzing" in acid_test:
            st.write("📌 **Potential Matches:** Calcite, Dolomite, Soft Carbonates.")
        else:
            st.write("📌 **Potential Matches:** Galena, Native Copper, Soft Sulfides.")
    elif "steel" in hardness_test:
        if "Resinous" in luster_test:
            st.write("📌 **Potential Matches:** Sphalerite, Fluorite.")
        else:
            st.write("📌 **Potential Matches:** Apatite, Hematite, Hornblende.")
    elif "glass" in hardness_test:
        st.write("📌 **Potential Matches:** Quartz, Chert, Jasper, Agate, Micro-druzy Quartz.")
    else:
        st.write("📌 **Potential Matches:** Corundum, Topaz, Beryl.")

# ==========================================
# TAB 3: PERSONAL COLLECTION CATALOG
# ==========================================
with tab3:
    st.header("My Rock & Mineral Collection")
    
    if len(st.session_state.collection) == 0:
        st.info("Your catalog is currently empty. Identify specimens in Tab 1 to add them here!")
    else:
        df_catalog = pd.DataFrame(st.session_state.collection)
        st.dataframe(df_catalog, use_container_width=True)
        
        col_dl, col_clr = st.columns([1, 1])
        with col_dl:
            csv_data = df_catalog.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Collection as CSV",
                data=csv_data,
                file_name="rockdex_collection.csv",
                mime="text/csv"
            )
        with col_clr:
            if st.button("🗑️ Clear Entire Catalog"):
                st.session_state.collection = []
                st.rerun()