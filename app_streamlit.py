# app_streamlit.py
import streamlit as st

# --- constants & logic (unchanged) ---
ANSH_PER_RASHI = 30
KALA_PER_ANSH = 60
VIPLA_PER_KALA = 60

def to_vipla_from_rashi(rashi, ansh, kala, vipla):
    return (
        rashi * ANSH_PER_RASHI * KALA_PER_ANSH * VIPLA_PER_KALA +
        ansh  * KALA_PER_ANSH * VIPLA_PER_KALA +
        kala  * VIPLA_PER_KALA +
        vipla
    )

def from_vipla_to_rashi_units(total_vipla):
    kala = int(total_vipla // VIPLA_PER_KALA)
    vipla = int(total_vipla % VIPLA_PER_KALA)

    ansh = int(kala // KALA_PER_ANSH)
    kala = int(kala % KALA_PER_ANSH)

    rashi = int(ansh // ANSH_PER_RASHI)
    ansh = int(ansh % ANSH_PER_RASHI)

    return rashi, ansh, kala, vipla

def compute_result(t1, t2, ishtkaal_pal):
    v1 = to_vipla_from_rashi(*t1)
    v2 = to_vipla_from_rashi(*t2)
    diff_vipla = abs(v1 - v2)

    combined = diff_vipla * ishtkaal_pal
    quotient = int(combined // 3600)
    remainder = combined % 3600
    if remainder > 1500:
        quotient += 1

    result_vipla = v2 + quotient
    return from_vipla_to_rashi_units(result_vipla)

# --- Streamlit UI ---
st.title("Ishtkaal Calculator (Mobile friendly)")

st.write("Enter Time 1 and Time 2 as: rashi ansh kala vipla (four integers)")

col1, col2 = st.columns(2)
with col1:
    t1_text = st.text_input("Time 1 (rashi ansh kala vipla)", value="0 0 0 0")
with col2:
    t2_text = st.text_input("Time 2 (rashi ansh kala vipla)", value="0 0 0 0")

st.write("Ishtkaal input — either enter single PAL, OR fill ghati, pal, vipal")

isht_single = st.text_input("Single PAL (leave empty to use ghati/pal/vipal)", value="")
gcol, pcol, vcol = st.columns(3)
with gcol:
    ghati_text = st.text_input("ghati", value="0")
with pcol:
    pal_text = st.text_input("pal", value="0")
with vcol:
    vipal_text = st.text_input("vipal", value="0")

# parse inputs and compute
def parse_rashi_str(s):
    parts = s.strip().split()
    if len(parts) != 4:
        raise ValueError("Enter four integers: rashi ansh kala vipla")
    return list(map(int, parts))

def parse_ishtkaal_streamlit(single, g, p, v):
    single = single.strip()
    if single != "":
        return float(single)
    # else use ghati/pal/vipal
    ghati = int(g); pal = int(p); vipal = int(v)
    total_pal = ghati * 60 + pal + vipal / 60.0
    return total_pal

if st.button("Compute"):
    try:
        t1 = parse_rashi_str(t1_text)
        t2 = parse_rashi_str(t2_text)
        isht_pal = parse_ishtkaal_streamlit(isht_single, ghati_text, pal_text, vipal_text)
        r,a,k,v = compute_result(t1, t2, isht_pal)
        st.success(f"Result: {r} rashi {a} ansh {k} kala {v} vipla")
    except Exception as e:
        st.error(f"Error: {e}")

st.write("Notes:")
st.write("- If single PAL is filled, ghati/pal/vipal are ignored.")
st.write("- If you enter single PAL = 0, result will be Time 2 (mathematically correct).")
