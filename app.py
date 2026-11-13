import datetime

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

# Initialize Session State for the uploaded photo (session-only:
# the photo lives in memory while the app is open, and is gone
# when the app closes — that is expected for now)
if "photo_bytes" not in st.session_state:
    st.session_state.photo_bytes = None
if "photo_name" not in st.session_state:
    st.session_state.photo_name = None

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

        # --- NEW IN V2: photo upload ---
        st.markdown("---")
        photo_file = st.file_uploader(
            "Upload a photo of your rock",
            type=["jpg", "jpeg", "png"],
            key="rock_photo",
            help="Pick a photo from your phone gallery. The photo stays only while the app is open."
        )
        if photo_file is not None:
            st.session_state.photo_bytes = photo_file.getvalue()
            st.session_state.photo_name = photo_file.name

    with col_out:
        st.subheader("Identification Summary")
        # --- NEW IN V2: show the uploaded photo next to the answer ---
        if st.session_state.photo_bytes is not None:
            st.image(
                st.session_state.photo_bytes,
                caption="Your rock",
                use_container_width=True
            )
        st.metric(label="Identified Specimen", value=specimen_name)
        st.write(f"**Mohs Hardness:** {hardness_val}")
        st.info(f"**Description:** {desc}")

        # --- NEW IN V2: where and when it was found ---
        where_found = st.text_input(
            "Where did you find it?",
            placeholder="For example: a creek near home",
            key="where_found"
        )
        date_found = st.date_input(
            "Date found",
            value=datetime.date.today(),
            key="date_found"
        )

        # Add to collection button
        if st.button("➕ Add Identified Specimen to Catalog"):
            new_entry = {
                "Specimen": specimen_name,
                "Hardness": hardness_val,
                "Category": category,
                "Where Found": where_found,
                "Date Found": str(date_found),
                "Notes": desc,
                # The photo travels with the entry, in memory only.
                # It is kept out of the table and the CSV export.
                "Photo": st.session_state.photo_bytes,
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

    # --- NEW IN V2: deeper tests ---
    st.markdown("---")
    st.subheader("More Tests — Go a Little Deeper")
    st.write("Each test below is optional. Leave any test on its first choice if you have not done it yet.")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.subheader("4. Streak Test")
        st.write("Scrape the rock on the back of an unglazed flower pot. What color is the streak?")
        streak_test = st.selectbox(
            "Streak Color",
            [
                "I haven't done this test yet",
                "Red-brown",
                "Black (and a magnet pulls it)",
                "Lead-gray",
                "Greenish-black",
                "White to yellowish-brown (sometimes a sulfur smell)",
                "White",
                "No streak at all"
            ],
            key="w_streak"
        )

        st.subheader("5. Hydrogen Peroxide Test")
        st.write("Put a drop of hydrogen peroxide on the rock. What happens?")
        peroxide_test = st.selectbox(
            "Peroxide Reaction",
            [
                "I haven't done this test yet",
                "No fizz",
                "Fizzes a little",
                "Fizzes hard (on a black rock)"
            ],
            key="w_peroxide"
        )

    with col5:
        st.subheader("6. Vinegar Test")
        st.write("Put a drop of vinegar on the rock. (A separate test — not on the same rock at the same time as the peroxide.)")
        vinegar_test = st.selectbox(
            "Vinegar Reaction",
            [
                "I haven't done this test yet",
                "No fizz",
                "Weak fizz",
                "Strong fizz"
            ],
            key="w_vinegar"
        )

        st.subheader("7. Feel & Sound")
        hollow_test = st.selectbox(
            "Does it feel hollow?",
            ["Not sure", "Yes", "No"],
            key="w_hollow"
        )
        sound_test = st.selectbox(
            "Sound when tapped",
            ["Not sure", "Rings like a bell", "Dull thud"],
            key="w_sound"
        )
        heavy_test = st.selectbox(
            "Heavy for its size?",
            ["About right", "Yes, surprisingly heavy", "Light for its size"],
            key="w_heavy"
        )

    with col6:
        st.subheader("8. Sparkle Check")
        st.write("Turn the rock slowly in good light. Does it sparkle?")
        sparkle_test = st.selectbox(
            "Does it sparkle in the light?",
            ["No", "Yes, little sparkles"],
            key="w_sparkle"
        )

    st.markdown("---")
    st.subheader("Diagnostic Suggestions")

    # --- Original v1 logic, unchanged ---
    if "Fingernail" in hardness_test:
        base_matches = "Gypsum, Talc, Soft Clays."
    elif "penny" in hardness_test:
        if "Effervescence" in acid_test or "Fizzing" in acid_test:
            base_matches = "Calcite, Dolomite, Soft Carbonates."
        else:
            base_matches = "Galena, Native Copper, Soft Sulfides."
    elif "steel" in hardness_test:
        if "Resinous" in luster_test:
            base_matches = "Sphalerite, Fluorite."
        else:
            base_matches = "Apatite, Hematite, Hornblende."
    elif "glass" in hardness_test:
        base_matches = "Quartz, Chert, Jasper, Agate, Micro-druzy Quartz."
    else:
        base_matches = "Corundum, Topaz, Beryl."

    st.write(f"📌 **Potential Matches:** {base_matches}")

    # --- NEW IN V2: what the deeper tests say ---
    clues = []

    if streak_test == "Red-brown":
        clues.append("🔴 **Red-brown streak** points to **hematite**.")
    elif streak_test == "Black (and a magnet pulls it)":
        clues.append("🧲 **Black streak, and a magnet pulls it**, points to **magnetite**.")
    elif streak_test == "Lead-gray":
        clues.append("⬛ **Lead-gray streak** points to **galena**.")
    elif streak_test == "Greenish-black":
        clues.append("🟢 **Greenish-black streak** points to **pyrite**. (Real gold leaves a gold-yellow streak, not greenish-black.)")
    elif streak_test == "White to yellowish-brown (sometimes a sulfur smell)":
        clues.append("🟡 **White to yellowish-brown streak**, sometimes with a sulfur smell, points to **sphalerite**.")
    elif streak_test == "White":
        clues.append("⚪ A plain **white streak** tells us almost nothing — most rocks leave a white streak.")
    elif streak_test == "No streak at all":
        clues.append("🫙 **No streak at all** means your rock is harder than the flower pot — that itself is a clue.")

    if peroxide_test == "Fizzes hard (on a black rock)":
        clues.append("🫧 **Hard fizzing with peroxide on a black rock** points toward **pyrolusite**.")
    elif peroxide_test == "Fizzes a little":
        clues.append("🫧 A little fizz with peroxide is a small hint, not a strong one.")

    if vinegar_test == "Weak fizz":
        clues.append("🫧 **Weak fizz with vinegar** points to **calcite**.")
    elif vinegar_test == "Strong fizz":
        clues.append("🫧 **Strong fizz with vinegar** points to a carbonate mineral, like **calcite**.")
    elif vinegar_test == "No fizz":
        clues.append("🚫 **No fizz with vinegar** means it is probably not a carbonate — quartz, for example, does not fizz. (Dolomite only fizzes once it is powdered.)")

    if heavy_test == "Yes, surprisingly heavy":
        clues.append("⚖️ **Surprisingly heavy for its size** points toward **galena** and other dense minerals.")
    if hollow_test == "Yes":
        clues.append("🕳️ **Feeling hollow** can mean there is a pocket or cavity inside — sometimes where crystals grow.")
    if sound_test == "Rings like a bell":
        clues.append("🔔 A **clear ring when tapped** can mean the rock is solid and fine-grained.")
    if sparkle_test == "Yes, little sparkles":
        clues.append("✨ Those **little sparkles** are often tiny flakes of **mica** — a lovely clue, not a verdict.")

    if clues:
        st.markdown("**What your deeper tests say:**")
        for clue in clues:
            st.write(clue)
    else:
        st.write("Try one of the deeper tests above — the streak test is a great one to start with.")

    # If the streak points to a soft mineral but the hardness test says
    # hard (or the other way round), say so plainly. Streak and hardness
    # are the two tests to trust most.
    soft_streak = streak_test in (
        "Lead-gray",
        "White to yellowish-brown (sometimes a sulfur smell)",
    )
    hard_streak = streak_test in (
        "Red-brown",
        "Black (and a magnet pulls it)",
        "Greenish-black",
    )
    hard_scratch = hardness_test in (
        "Scratches glass knife/plate (> 5.5 - 7)",
        "Scratches quartz (> 7)",
    )
    soft_scratch = hardness_test in (
        "Scratched by fingernail (< 2.5)",
        "Scratched by copper penny (2.5 - 3.5)",
    )
    if (soft_streak and hard_scratch) or (hard_streak and soft_scratch):
        st.warning(
            "Your tests disagree a little — the streak points one way and the scratch test points another. "
            "Trust the **streak** and the **hardness** test most, and try both again on a fresh, clean spot."
        )

    # --- NEW IN V2: what might be hiding inside ---
    st.markdown("---")
    st.subheader("🔮 What Might Be Hiding Inside?")
    st.write("These are only chances — never a promise. The only way to know for sure is to look inside.")

    # Chances start from the kind of rock picked in Tab 1.
    if specimen_name in ("Fossiliferous Chert", "Fossil Specimen (Marine)"):
        fossils = ("Likely", "This kind of rock often holds the remains of little sea creatures.")
        crystals = ("Maybe", "Crystals sometimes grow in the cracks and pockets of this kind of rock.")
        geode = ("Unlikely", "This kind of rock is usually solid all the way through.")
    elif specimen_name == "Micro-druzy Quartz in Vug":
        fossils = ("Maybe", "A vug is a little pocket, and sea creatures sometimes ended up in pockets like this.")
        crystals = ("Likely", "A vug is a little pocket — and pockets are where crystals love to grow.")
        geode = ("Maybe", "A vug is a small pocket, not a big hollow geode — but it is the same idea, on a small scale.")
    elif specimen_name == "Banded Chert":
        fossils = ("Maybe", "Banded chert sometimes holds fossils, sometimes not.")
        crystals = ("Maybe", "Tiny quartz crystals sometimes hide in banded chert.")
        geode = ("Unlikely", "Banded chert is usually dense and solid, not hollow.")
    elif specimen_name == "Galena":
        fossils = ("Unlikely", "Galena grows in mineral veins, not in old sea beds full of fossils.")
        crystals = ("Maybe", "Galena often grows in neat little cubes — those are crystals you can already see.")
        geode = ("Unlikely", "Galena does not form hollow geodes.")
    elif specimen_name == "Sphalerite":
        fossils = ("Unlikely", "Sphalerite grows in mineral veins, not in old sea beds full of fossils.")
        crystals = ("Maybe", "Sphalerite sometimes grows in small, shiny crystals.")
        geode = ("Unlikely", "Sphalerite does not form hollow geodes.")
    else:  # Calcite
        fossils = ("Maybe", "Calcite sometimes replaces old shells and sea creatures.")
        crystals = ("Maybe", "Calcite often forms clear crystals in cracks.")
        geode = ("Unlikely", "Calcite does not usually form hollow geodes.")

    # A hollow feel or a clear ring lifts the chances of a pocket inside.
    if hollow_test == "Yes":
        if geode[0] == "Unlikely":
            geode = ("Maybe", "It feels hollow — that might mean there is a pocket inside.")
        if crystals[0] == "Unlikely":
            crystals = ("Maybe", "A hollow feel might mean there is a pocket where crystals could grow.")

    st.write(f"🦴 **Fossils inside: {fossils[0]}** — {fossils[1]}")
    st.write(f"💠 **Crystals inside: {crystals[0]}** — {crystals[1]}")
    st.write(f"🥚 **A geode inside: {geode[0]}** — {geode[1]}")

# ==========================================
# TAB 3: PERSONAL COLLECTION CATALOG
# ==========================================
with tab3:
    st.header("My Rock & Mineral Collection")
    st.caption("Entries and photos stay only while the app is open. Closing the app clears them — a lasting catalog is coming in a later version.")

    if len(st.session_state.collection) == 0:
        st.info("Your catalog is currently empty. Identify specimens in Tab 1 to add them here!")
    else:
        # The photo bytes are kept out of the table and the CSV file.
        display_entries = [
            {key: value for key, value in entry.items() if key != "Photo"}
            for entry in st.session_state.collection
        ]
        df_catalog = pd.DataFrame(display_entries)
        st.dataframe(df_catalog, use_container_width=True)

        # Show the photos that travelled with the entries.
        photos = [
            entry for entry in st.session_state.collection
            if entry.get("Photo") is not None
        ]
        if photos:
            st.subheader("📸 Your Specimen Photos")
            for entry in photos:
                caption = entry["Specimen"]
                if entry.get("Where Found"):
                    caption += f" — found at {entry['Where Found']}"
                st.image(entry["Photo"], caption=caption, use_container_width=True)

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
