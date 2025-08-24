# valorant_flow_gui.py

import streamlit as st

# --- 勝敗パターンごとの基本ポイント ---
POINT_TABLE = {
    ("Win",  "Win",  "Win"):  2.71,
    ("Win",  "Win",  "Lose"): 0.83,
    ("Lose", "Lose", "Win"): -0.83,
    ("Lose", "Lose", "Lose"): -2.71,
    ("Win",  "Lose", "Win"):  0.10,
    ("Lose", "Win",  "Lose"): -0.10,
    ("Win",  "Lose", "Lose"): -1.65,
    ("Lose", "Win",  "Win"):  1.65,
}

# --- 取り方ごとの位置別ボーナス ---
BONUS_TABLE = {
    "Ace":       [0.31, 1.30, 0.97],
    "Thrifty":   [0.07, 0.24, 1.65],
    "Team Ace":  [0.07, 0.12, 0.76],
    "Clutch":    [-0.45, 0.12, 0.24],
    "Flawless":  [0.82, 2.33, 4.11],
    "Normal":    [0.0,  0.0,  0.0],
}

ROUND_LABELS = ["3つ前", "2つ前", "直前"]

def calculate_points(rounds):
    key = tuple(r["win"] for r in rounds)
    total = POINT_TABLE.get(key, 0.0)

    for i, r in enumerate(rounds):
        rtype = r["type"]
        bonus = BONUS_TABLE.get(rtype, [0.0, 0.0, 0.0])[i]
        if r["win"] == "Win":
            total += bonus
        else:
            total -= bonus
    return round(total, 2)

def points_to_winrate(points):
    rate = 50.0 + points
    rate = max(0.0, min(100.0, rate))
    return round(rate, 2)

# --- Streamlit GUI ---
st.set_page_config(page_title="VALORANT 勝率計算ツール", layout="centered")
st.title(" VALORANT 勝率計算ツール")

rounds = []
for i, lbl in enumerate(ROUND_LABELS):
    st.subheader(f"{lbl} のラウンド")
    col1, col2 = st.columns(2)

    with col1:
        win = st.selectbox(f"{lbl} の勝敗", ["Win", "Lose"], key=f"win_{i}")
    with col2:
        rtype = st.selectbox(
            f"{lbl} の取り方",
            ["Normal", "Ace", "Thrifty", "Team Ace", "Clutch", "Flawless"],
            key=f"type_{i}"
        )
    rounds.append({"win": win, "type": rtype})

if st.button("勝率を計算"):
    pts = calculate_points(rounds)
    winrate = points_to_winrate(pts)

    st.success(f"ポイント: {pts:+.2f}")
    st.metric("次ラウンド勝率", f"{winrate:.2f} %")

