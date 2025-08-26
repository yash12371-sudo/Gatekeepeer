import streamlit as st
import datetime
import random
from pathlib import Path

# ---------- CONFIG ----------
st.set_page_config(page_title="Pre Trade Gatekeeper", page_icon="📊", layout="centered")

# ---------- CONSTANTS ----------
MOTTO = "One safe trade is better than ten impulsive ones."
QUOTES = [
    "A missed trade costs nothing. An impulsive trade can cost peace, money, and confidence.",
    "I trade to protect my capital first; profits are the reward for patience, not the price of panic.",
    "If I cannot wait, it is not the setup speaking — it is my emotion. And emotion never pays.",
    "One disciplined trade builds me. One reckless trade destroys me. The choice is always mine.",
    "The market owes me nothing. My only edge is calm execution of my plan."
]
JOURNAL_PATH = Path("trade_journal.csv")

# ---------- STATE ----------
if "show_checklist" not in st.session_state:
    st.session_state["show_checklist"] = False
if "checklist_passed" not in st.session_state:
    st.session_state["checklist_passed"] = False
if "answers" not in st.session_state:
    st.session_state["answers"] = {}
if "quote" not in st.session_state:
    st.session_state["quote"] = None

# ---------- HELPERS ----------
def random_quote():
    return random.choice(QUOTES)

def write_journal(data: dict):
    header = ["date","ticker","state","process","emotion_reason","stop_loss","target_price","future_self","motto"]
    create_header = not JOURNAL_PATH.exists()
    try:
        with JOURNAL_PATH.open("a", encoding="utf-8") as f:
            if create_header:
                f.write(",".join(header) + "\n")
            row = [
                data["date"],
                data["ticker"],
                str(data["state"]),
                data["process"],
                data["emotion_reason"],
                data["stop_loss"],
                data["target_price"],
                '"' + data["future_self"].replace(",", ";") + '"',
                MOTTO
            ]
            f.write(",".join(row) + "\n")
        st.info("📝 Logged to trade_journal.csv")
    except Exception as e:
        st.warning(f"⚠️ Could not write to journal: {e}")

# ---------- CHECKLIST ----------
def show_checklist():
    st.subheader("🧾 Emotional Pre-Trade Checklist")

    with st.form("checklist_form"):
        st.markdown("### 🎯 Trade Setup")
        ticker = st.text_input("📌 Symbol / Instrument (e.g., NIFTY, RELIANCE)")

        st.markdown("### 🌡️ Emotional State")
        state = st.slider("How calm and detached do you feel?", 1, 5, 3,
                          format="%d",
                          help="1 = very stressed | 5 = fully calm")
        st.caption("1 😣 Stressed — 3 😐 Neutral — 5 😌 Calm")

        st.markdown("### 📜 System Discipline")
        process = st.radio("✅ Does this trade fully match your written system?", ["Yes", "No"], horizontal=True)

        st.markdown("### ❤️ Emotional Motive Check")
        emotion = st.radio("❓ Am I trading to win back money, prove something, or escape boredom?",
                           ["No", "Yes"], horizontal=True)

        st.markdown("### ⚖️ Risk Plan")
        sl = st.text_input("🛑 Stop Loss Price (e.g., 150)")
        tp = st.text_input("🎯 Target Price (e.g., 200)")

        capital = st.checkbox("⚠️ I accept: One trade cannot make me rich, but one bad trade can destroy my capital.")

        st.markdown("### 📝 Reflection")
        future = st.text_area("✍️ One sentence to your future self: WHY are you taking this trade?")

        submitted = st.form_submit_button("🔍 Validate My Mindset")

    if submitted:
        passed = (
            ticker.strip() and
            state >= 4 and
            process == "Yes" and
            emotion == "No" and
            sl.strip() and
            tp.strip() and
            capital and
            future.strip()
        )

        st.session_state["checklist_passed"] = passed
        st.session_state["answers"] = {
            "date": str(datetime.date.today()),
            "ticker": ticker.strip(),
            "state": state,
            "process": process,
            "emotion_reason": emotion,
            "stop_loss": sl.strip(),
            "target_price": tp.strip(),
            "future_self": future.strip()
        }

        if passed:
            st.success("✅ Checklist passed. Tap Confirm Trade to continue.")

            # Show quote in a highlighted card
            st.session_state["quote"] = random_quote()
            st.markdown(f"""
            <div style="padding:15px;border-radius:10px;
                        background-color:#f0f9ff;
                        border:1px solid #38bdf8;
                        font-size:16px;">
                💡 <b>Reflection:</b><br>
                <i>{st.session_state['quote']}</i>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("⛔ Checklist not complete or failed.")
            st.session_state["quote"] = None

# ---------- MAIN ----------
def main():
    # Title
    st.markdown("<h1 style='text-align: center;'>📊 Pre Trade Gatekeeper</h1>", unsafe_allow_html=True)
    st.info(f"🧭 **MOTTO: {MOTTO}**")
    st.divider()

    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Enter Trade"):
            st.session_state["show_checklist"] = True
    with col2:
        if st.button("🔄 Reset"):
            st.session_state["show_checklist"] = False
            st.session_state["checklist_passed"] = False
            st.session_state["answers"] = {}
            st.session_state["quote"] = None

    # Checklist logic
    if st.session_state["show_checklist"]:
        show_checklist()

        if st.session_state["checklist_passed"]:
            if st.button("✅ Confirm Trade"):
                st.success("🎉 Trade confirmed and placed.")

                # Motto Reminder
                st.info(f"🧭 **MOTTO REMINDER: {MOTTO}**")

                # Log trade
                write_journal(st.session_state["answers"])

                # Reset after confirmation
                st.session_state["show_checklist"] = False
                st.session_state["checklist_passed"] = False
                st.session_state["answers"] = {}
                st.session_state["quote"] = None
    else:
        st.caption("👉 Tap **Enter Trade** to start the checklist.")

if __name__ == "__main__":
    main()
