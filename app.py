import streamlit as st
import time
from PIL import Image, ImageOps

# ================= CUSTOMIZE =================
APP_TITLE = "💘 Valentines Bot"
HIS_NAME = "Gordito"
YOUR_NAME = "Violeta"
PASSWORD = "020625"

GIF_Q1 = "hug.gif"
GIF_Q2 = "kiss.gif"
GIF_Q3 = "hug_jump.gif"
GIF_FINAL_EXTRA = "moti-hearts.gif"

TEASE_MESSAGES = [
    "Mentira",
    "No acepto esa respuesta.",
    "Intentá otra vez Gordito 😌",
    "Dale… sabés cuál es.",
]

TYPEWRITER_TEXT = f"Te amo, {HIS_NAME}. y Te extraño muuuuuuucho 😌💘"

Q2_QUESTION = "Pregunta 2: What are you going to have when you come back? 😌"
Q2_OPTIONS = [
    "Muchos mimitos",
    "Muchos abrazos 🫂",
    "Un monton de besosssss",
    "Todas las anteriores 💘",
]
Q2_CORRECT = "Todas las anteriores 💘"

TARGET_KISSES = 20
TARGET_HUGS = 20

PHOTOS = [
    "Image_1.jpeg",
    "Image_2.jpeg",
    "Image_3.jpeg",
    "Image_4.jpeg",
    "Image_5.jpeg",
    "Image_6.jpeg",
    "Image_7.jpeg",
]
# ============================================

st.set_page_config(page_title=APP_TITLE, page_icon="💘", layout="centered")

# ---- Romantic CSS ----
st.markdown("""
<style>
.block-container {max-width: 900px;}
button {font-size:26px !important;padding:1rem 1.4rem !important;border-radius:18px !important;}
button[kind="primary"] {background-color:#ff4b91 !important;color:white !important;border:none !important;}
button[kind="primary"]:hover {background-color:#ff6aa8 !important;transform:scale(1.03);}
p, li {font-size:22px;}
.final-card {background: rgba(255,75,145,0.08);border-radius:18px;padding:18px;}
.big-title {font-size:34px;font-weight:700;}
.album-wrap {display:flex;justify-content:center;}
.album-card {width:min(860px,100%);border-radius:22px;padding:14px;box-shadow:0 10px 30px rgba(0,0,0,0.10);}
.album-caption {text-align:center;opacity:0.85;margin-top:8px;}
</style>
""", unsafe_allow_html=True)

# ---- Helpers ----
def smooth_transition(message="Loading… 💘", seconds=2.0):
    st.info(message)
    bar = st.progress(0)
    for i in range(41):
        bar.progress(i / 40)
        time.sleep(seconds / 40)

def burst_te_amo_once():
    for _ in range(3):
        st.toast("Te amo 💘")
        time.sleep(0.2)

def show_album_photo(path, caption=""):
    try:
        img = Image.open(path)
        img = ImageOps.exif_transpose(img)

        target_h = 700
        ratio = target_h / float(img.height)
        new_w = int(img.width * ratio)
        img = img.resize((new_w, target_h))

        st.markdown("<div class='album-wrap'><div class='album-card'>", unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

        if caption:
            st.markdown(f"<div class='album-caption'>{caption}</div>", unsafe_allow_html=True)
    except:
        st.warning(f"Could not open: {path}")

# ---- State ----
if "ok" not in st.session_state: st.session_state.ok = False
if "step" not in st.session_state: st.session_state.step = 0  # 0 pass, 1 q1, 2 q2, 3 clicks, 5 album, 6 ending
if "no_clicks" not in st.session_state: st.session_state.no_clicks = 0
if "kisses" not in st.session_state: st.session_state.kisses = 0
if "hugs" not in st.session_state: st.session_state.hugs = 0
if "photo_idx" not in st.session_state: st.session_state.photo_idx = 0

# ---- PASSWORD ----
def password_screen():
    st.title("🔒 Secret Link")
    st.caption("Hint: our anniversary 📅 (DDMMYY)")
    pw = st.text_input("Password", type="password")

    if st.button("Entrar 💘", type="primary"):
        if pw == PASSWORD:
            st.session_state.ok = True
            st.session_state.step = 1
            st.rerun()
        else:
            st.error("Nope 😈")

# ---- QUESTION 1 ----
def question_1():
    st.title(APP_TITLE)
    st.write("Do you miss me? 😌")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("No 😈"):
            st.session_state.no_clicks += 1
    with c2:
        if st.button("Obvio 💘", type="primary"):
            st.balloons()
            smooth_transition("Ok… next question 😌💘", 2)
            st.session_state.step = 2
            st.rerun()

    if st.session_state.no_clicks > 0:
        msg = TEASE_MESSAGES[(st.session_state.no_clicks - 1) % len(TEASE_MESSAGES)]
        st.warning(msg)

    try:
        st.image(GIF_Q1, use_container_width=True)
    except:
        pass

# ---- QUESTION 2 ----
def question_2():
    st.title("🧩 Mini quiz")
    choice = st.radio(Q2_QUESTION, Q2_OPTIONS)

    if st.button("Confirm 😌", type="primary"):
        if choice == Q2_CORRECT:
            st.balloons()
            burst_te_amo_once()
            smooth_transition("Ok… one more thing 😈💘", 2)
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("Mmm no 😈")

    try:
        st.image(GIF_Q2, use_container_width=True)
    except:
        pass

# ---- CLICK SECTION ----
def clicks_section():
    st.title("💋🫂 Final challenge")
    st.write("if you want to see the final surprise, give me MANY kisses and hugs 😌💘")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💋 Kiss +1", type="primary"):
            st.session_state.kisses += 1
    with c2:
        if st.button("🫂 Hug +1", type="primary"):
            st.session_state.hugs += 1

    st.progress(min(st.session_state.kisses / TARGET_KISSES, 1.0))
    st.progress(min(st.session_state.hugs / TARGET_HUGS, 1.0))

    if st.session_state.kisses >= TARGET_KISSES and st.session_state.hugs >= TARGET_HUGS:
        if st.button("🎁 Reveal", type="primary"):
            st.balloons()
            smooth_transition("Opening… 💘", 2)
            st.session_state.step = 5
            st.rerun()

    try:
        st.image(GIF_Q3, use_container_width=True)
    except:
        pass

# ---- ALBUM PAGE (PHOTOS ONLY) ----
def album_page():
    st.subheader("📸 Our moments")

    idx = max(0, min(st.session_state.photo_idx, len(PHOTOS) - 1))
    st.session_state.photo_idx = idx

    show_album_photo(PHOTOS[idx], caption=f"{idx + 1}/{len(PHOTOS)}")

    a, b, c = st.columns(3)
    with a:
        if st.button("⬅️ Prev"):
            st.session_state.photo_idx = max(0, st.session_state.photo_idx - 1)
            st.rerun()
    with b:
        if st.button("➡️ Next", type="primary"):
            st.session_state.photo_idx = min(len(PHOTOS) - 1, st.session_state.photo_idx + 1)
            st.rerun()
    with c:
        if st.button("🔁 Start"):
            st.session_state.photo_idx = 0
            st.rerun()

    # On last photo, show button to go to ending page
    if st.session_state.photo_idx == len(PHOTOS) - 1:
        st.divider()
        if st.button("💘 Final Message", type="primary"):
            smooth_transition("Last page… 😌💘", 2)
            st.session_state.step = 6
            st.rerun()

# ---- ENDING PAGE (MESSAGE + GIF) ----
def ending_page():
    st.markdown("<div class='big-title'>Happy Valentines day 💖</div>", unsafe_allow_html=True)

    st.markdown("<div class='final-card'>", unsafe_allow_html=True)

    placeholder = st.empty()
    for i in range(len(TYPEWRITER_TEXT)):
        placeholder.markdown(f"### {TYPEWRITER_TEXT[:i+1]}")
        time.sleep(0.03)

    st.markdown(f"— **{YOUR_NAME}**")

    try:
        st.image(GIF_FINAL_EXTRA, use_container_width=True)
    except:
        st.info("Missing moti-hearts.gif")

    st.markdown("</div>", unsafe_allow_html=True)

# ---- ROUTER ----
if not st.session_state.ok:
    password_screen()
else:
    if st.session_state.step == 1:
        question_1()
    elif st.session_state.step == 2:
        question_2()
    elif st.session_state.step == 3:
        clicks_section()
    elif st.session_state.step == 6:
        ending_page()
    else:
        album_page()
