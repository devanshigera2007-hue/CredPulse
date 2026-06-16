import streamlit as st
import sqlite3
import database  # ensures shop_profile table is created before we query it

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0a0a12 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 700px; }
.stTextInput > div > div > input {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  color: #f1f5f9 !important;
}
label { color: #94a3b8 !important; font-size: 13px !important; font-weight: 500 !important; }
.stButton > button {
  background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:28px;">
  <div style="font-size:26px;font-weight:800;color:#f8fafc;">⚙️ Settings</div>
  <div style="font-size:13px;color:#475569;margin-top:2px;">Manage your shop profile</div>
</div>
""", unsafe_allow_html=True)

# ==========================
# LOAD PROFILE
# ==========================

with sqlite3.connect("credpulse.db") as conn:
    profile = conn.execute("SELECT * FROM shop_profile LIMIT 1").fetchone()

if not profile:
    st.warning("No profile found. Please go to the home page to set one up.")
    st.stop()

_, db_shop, db_owner, db_city, db_phone, db_upi = profile

# ==========================
# PROFILE CARD (read view)
# ==========================

st.markdown(f"""
<div style="background:rgba(124,58,237,0.07);border:1px solid rgba(124,58,237,0.2);
  border-radius:18px;padding:28px;margin-bottom:28px;">
  <div style="display:flex;align-items:center;gap:18px;margin-bottom:20px;">
    <div style="width:56px;height:56px;border-radius:50%;
      background:linear-gradient(135deg,#7c3aed,#a855f7);
      display:flex;align-items:center;justify-content:center;
      font-size:22px;font-weight:800;color:white;">
      {db_owner[0].upper() if db_owner else '?'}
    </div>
    <div>
      <div style="font-size:20px;font-weight:800;color:#f8fafc;">{db_shop}</div>
      <div style="font-size:13px;color:#64748b;">{db_owner} · {db_city or 'Location not set'}</div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
    <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:12px 14px;">
      <div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;">Phone</div>
      <div style="font-size:14px;font-weight:600;color:#cbd5e1;">{db_phone or '—'}</div>
    </div>
    <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:12px 14px;">
      <div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;">UPI ID</div>
      <div style="font-size:14px;font-weight:600;color:#cbd5e1;">{db_upi or '—'}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ==========================
# EDIT FORM
# ==========================

st.markdown("""
<div style="font-size:14px;font-weight:700;color:#a78bfa;margin-bottom:16px;">✏️ Edit Profile</div>
""", unsafe_allow_html=True)

shop_name  = st.text_input("Shop Name",    value=db_shop  or "")
owner_name = st.text_input("Owner Name",   value=db_owner or "")
city       = st.text_input("City / Town",  value=db_city  or "")
phone      = st.text_input("Phone Number", value=db_phone or "")
upi_id     = st.text_input("UPI ID",       value=db_upi   or "")

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

if st.button("💾  Save Changes"):
    if not shop_name.strip():
        st.error("Shop name cannot be empty.")
    elif not owner_name.strip():
        st.error("Owner name cannot be empty.")
    else:
        with sqlite3.connect("credpulse.db") as conn:
            conn.execute(
                """UPDATE shop_profile
                   SET shop_name=?, owner_name=?, city=?, phone=?, upi_id=?
                   WHERE id=1""",
                (shop_name.strip(), owner_name.strip(),
                 city.strip(), phone.strip(), upi_id.strip())
            )
            conn.commit()
        st.success("✅ Profile updated successfully!")
        st.rerun()

# ==========================
# DANGER ZONE
# ==========================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="border:1px solid rgba(239,68,68,0.2);border-radius:14px;padding:20px 22px;">
  <div style="font-size:13px;font-weight:700;color:#ef4444;margin-bottom:6px;">⚠️ Danger Zone</div>
  <div style="font-size:13px;color:#475569;margin-bottom:14px;">
    Resetting your profile will show the setup screen again on next visit. Your customer data will not be affected.
  </div>
""", unsafe_allow_html=True)

if st.button("🗑️  Reset Shop Profile"):
    with sqlite3.connect("credpulse.db") as conn:
        conn.execute("DELETE FROM shop_profile")
        conn.commit()
    st.warning("Profile reset. Go to the home page to set up again.")
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)