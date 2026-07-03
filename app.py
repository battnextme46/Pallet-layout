import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Pallet Optimizer", layout="wide")

st.title("📦 Pallet Container Layout Optimizer")
st.write("เครื่องมือคำนวณการจัดวางพาเลทในตู้คอนเทนเนอร์แบบ Mixed Orientation")

# --- SIDEBAR INPUTS ---
st.sidebar.header("1. ข้อมูลพาเลท (cm)")
p_w = st.sidebar.number_input("ความกว้างพาเลท (Width)", value=80.0)
p_l = st.sidebar.number_input("ความยาวพาเลท (Length)", value=120.0)

st.sidebar.header("2. ข้อมูลตู้คอนเทนเนอร์")
c_type = st.sidebar.selectbox("ประเภทตู้", ["20ft", "40ft"])
c_w_raw = 235.0
c_l_raw = 590.0 if c_type == "20ft" else 1203.0

st.sidebar.header("3. ระยะเผื่อความปลอดภัย (Clearance)")
c_w_gap = st.sidebar.slider("ระยะเผื่อด้านกว้าง (Total W)", 0.0, 20.0, 5.0)
c_l_gap = st.sidebar.slider("ระยะเผื่อด้านยาว (Total L)", 0.0, 30.0, 10.0)

# --- CALCULATION LOGIC ---
def solve_layout(pw, pl, cw_raw, cl_raw, cw_clear, cl_clear):
    cw, cl = cw_raw - cw_clear, cl_raw - cl_clear
    
    # 1. Simple Grid
    o1 = (cw // pw) * (cl // pl)
    o2 = (cw // pl) * (cl // pw)
    if o1 >= o2:
        simple = {"n_rows": int(cw // pw), "n_type_w": pw, "n_type_l": pl, "n_per_row": int(cl // pl), "m_rows": 0, "total": int(o1)}
    else:
        simple = {"n_rows": int(cw // pl), "n_type_w": pl, "n_type_l": pw, "n_per_row": int(cl // pw), "m_rows": 0, "total": int(o2)}

    # 2. Mixed Orientation
    best_mixed = {"total": 0}
    for n in range(int(cw // pw) + 1):
        m = int((cw - (n * pw)) // pl)
        total = (n * (cl // pl)) + (m * (cl // pw))
        if total > best_mixed["total"]:
            best_mixed = {"n_rows": n, "n_type_w": pw, "n_type_l": pl, "n_per_row": int(cl // pl), "m_rows": m, "m_type_w": pl, "m_type_l": pw, "m_per_row": int(cl // pw), "total": int(total)}
    return simple, best_mixed

# --- EXECUTION & DISPLAY ---
simple_res, mixed_res = solve_layout(p_w, p_l, c_w_raw, c_l_raw, c_w_gap, c_l_gap)

col1, col2 = st.columns(2)

def draw_plot(res, title):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.add_patch(patches.Rectangle((0, 0), c_l_raw, c_w_raw, linewidth=3, edgecolor='black', facecolor='white'))
    usable_l, usable_w = c_l_raw - c_l_gap, c_w_raw - c_w_gap
    ax.add_patch(patches.Rectangle((c_l_gap/2, c_w_gap/2), usable_l, usable_w, linewidth=1, edgecolor='gray', facecolor='#f8fafc', linestyle='--'))
    
    used_w = (res["n_rows"] * res["n_type_w"]) + (res.get("m_rows", 0) * res.get("m_type_w", 0))
    curr_y = (c_w_raw - used_w) / 2
    
    def draw_g(n, n_p, pw, pl, sy):
        y = sy
        for i in range(n):
            off_x = (c_l_raw - (n_p * pl)) / 2
            for j in range(n_p):
                ax.add_patch(patches.Rectangle((off_x + j*pl, y), pl, pw, edgecolor='#0369a1', facecolor='#bae6fd'))
                ax.text(off_x + j*pl + pl/2, y + 2, f"{pl}", ha='center', va='bottom', fontsize=6)
                ax.text(off_x + j*pl + 2, y + pw/2, f"{pw}", ha='left', va='center', rotation=90, fontsize=6)
            y += pw
        return y

    ny = draw_g(res["n_rows"], res["n_per_row"], res["n_type_w"], res["n_type_l"], curr_y)
    if res.get("m_rows", 0) > 0:
        draw_g(res["m_rows"], res["m_per_row"], res["m_type_w"], res["m_type_l"], ny)
    
    ax.set_aspect('equal')
    ax.set_title(f"{title}: {res['total']} UNITS")
    return fig

with col1:
    st.pyplot(draw_plot(simple_res, "OPTION 1: SIMPLE GRID"))

if mixed_res["total"] > simple_res["total"]:
    with col2:
        st.pyplot(draw_plot(mixed_res, "OPTION 2: MIXED ORIENTATION"))
    st.success(f"แนะนำ Option 2: สามารถเพิ่มจำนวนได้อีก {mixed_res['total'] - simple_res['total']} ใบ!")

#### 2. สร้างไฟล์ `requirements.txt` บน GitHub แล้วพิมพ์ 2 บรรทัดนี้:
```text
streamlit
matplotlib

#### 3. กด "Deploy now" บนหน้าจอ Streamlit:
เลือก Repository ที่คุณอัปโหลดไฟล์ไป แล้วกดปุ่ม **Deploy!** ได้เลยครับ

ลองทำตามขั้นตอนในสไลด์ดูนะครับ หากติดตรงไหน หรือ GitHub สร้างยังไง แจ้งผมได้ทันทีครับ!
