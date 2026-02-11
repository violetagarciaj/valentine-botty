import streamlit as st
import time
import random

# ================= CUSTOMIZE =================
APP_TITLE = "💘 Valentines Bot"
HIS_NAME = "Gordito"
YOUR_NAME = "Violeta"
PASSWORD = "020625"                 # anniversary DDMMYY
REVEAL_IMAGE_PATH = "reveal.jpg"    # put this file next to app.py

TEASE_MESSAGES = [
    "😈 Mmmm sospechoso...",
    "No acepto esa respuesta.",
    "Intentá otra vez Gordito 😌",
    "Dale… sabés cuál es.",
    "Yo esperando el ‘Obvio’ como una reina 👑",
]

TYPEWRITER_TEXT = f"Te amo, {HIS_NAME}. Te extraño. Volvé a mí 😌💘"
# ============================================

st.set_page_config(page_title=APP_TITLE, page_icon="💘", layout="centered")

# --- Password gate ---
def password_gate():
    if "ok" not in st.session_state:
        st.session_state.ok = False

    if not st.session_state.ok:
        st.title("🔒 Link secreto")
        st.write("Esto es solo para vos 💘")
        st.caption("Pista: nuestro aniversario 📅")
        st.caption("Formato: DDMMYY 😉")

        pw = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if pw == PASSWORD:
                st.session_state.ok = True
                st.rerun()
            else:
                st.error("Nope 😈 probá otra vez")
        st.stop()

password_gate()

# --- State ---
if "no_clicks" not in st.session_state:
    st.session_state.no_clicks = 0
if "solved" not in st.session_state:
    st.session_state.solved = False
if "hearts" not in st.session_state:
    st.session_state.hearts = 0
if "did_reveal_fx" not in st.session_state:
    st.session_state.did_reveal_fx = False

# --- UI ---
st.title(APP_TITLE)
st.caption(f"Para **{HIS_NAME}** — de **{YOUR_NAME}** 💌")

# Growing hearts (always visible)
st.subheader("❤️ Amor acumulado")
colh1, colh2 = st.columns([1, 3])
with colh1:
    if st.button("❤️ +1"):
        st.session_state.hearts += 1
with colh2:
    st.write(" ".join(["❤️"] * min(st.session_state.hearts, 30)))
    if st.session_state.hearts > 30:
        st.caption(f"(Ok, ya entendí 😌) Total: {st.session_state.hearts}")

st.divider()

# Main question
st.subheader("Pregunta importante 😌")
st.write("¿Me amás?")

col1, col2 = st.columns(2)

with col1:
    if st.button("No 😈"):
        st.session_state.no_clicks += 1
        # a cheeky toast every time he says no
        st.toast("Incorrecto 😈", icon="😈")

with col2:
    if st.button("Obvio 💘"):
        st.session_state.solved = True
        st.rerun()

# Teasing logic
if st.session_state.no_clicks > 0 and not st.session_state.solved:
    msg = TEASE_MESSAGES[(st.session_state.no_clicks - 1) % len(TEASE_MESSAGES)]
    st.warning(msg)

# --- Reveal section ---
if st.session_state.solved:
    st.success("Sabía 😌")

    # Effects (run once)
    if not st.session_state.did_reveal_fx:
        st.session_state.did_reveal_fx = True

        # Big celebration
        st.balloons()
        st.snow()  # looks like cute falling confetti

        # "Floating Te amos" (multiple toasts)
        for _ in range(8):
            st.toast("Te amo 💘", icon="💘")
            time.sleep(0.08)

    # Typewriter text
    st.subheader("💌 Mensaje")
    placeholder = st.empty()
    for i in range(len(TYPEWRITER_TEXT)):
        placeholder.markdown(f"### {TYPEWRITER_TEXT[:i+1]}")
        time.sleep(0.03)

    st.markdown(f"— **{YOUR_NAME}**")

    # Reveal image
    st.divider()
    st.subheader("📸 Sorpresa")
    try:
        st.image(REVEAL_IMAGE_PATH, use_container_width=True)
    except Exception:
        st.warning(
            f"No encontré '{REVEAL_IMAGE_PATH}'. "
            "Poné una foto en la carpeta y renombrala a reveal.jpg"
        )

    st.divider()
    st.caption("Ahora mandame un audio diciendo ‘yo también’ 😏")

    # Reset button for testing
    if st.button("🔄 Reiniciar (testing)"):
        st.session_state.no_clicks = 0
        st.session_state.solved = False
        st.session_state.did_reveal_fx = False
        st.session_state.hearts = 0
        st.rerun()
