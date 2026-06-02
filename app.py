import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 定義 11 種立方體展開圖的相對座標
cube_nets = [
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (1, 3)],  # 1. 十字型
    [(0, 0), (0, 1), (1, 1), (2, 1), (1, 2), (1, 3)],  # 2.
    [(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (1, 2)],  # 3.
    [(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (2, 2)],  # 4.
    [(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (3, 2)],  # 5.
    [(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (2, 2)],  # 6.
    [(0, 1), (1, 1), (2, 1), (1, 2), (2, 2), (2, 3)],  # 7.
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)],  # 8.
    [(0, 1), (1, 1), (1, 2), (2, 2), (2, 3), (3, 3)],  # 9.
    [(0, 2), (1, 2), (1, 1), (2, 1), (2, 0), (3, 0)],  # 10.
    [(0, 1), (1, 1), (2, 1), (1, 0), (2, 2), (3, 2)]   # 11.
]

def draw_net(ax, net, target_face, line_type):
    """繪製單一展開圖並加上線條"""
    ax.set_aspect('equal')
    ax.axis('off')
    
    xs = [p[0] for p in net]
    ys = [p[1] for p in net]
    ax.set_xlim(min(xs) - 0.5, max(xs) + 1.5)
    ax.set_ylim(min(ys) - 0.5, max(ys) + 1.5)
    
    for j, (x, y) in enumerate(net):
        # 預設面顏色
        facecolor = 'lightblue'
        
        # 目標面變更顏色並畫線
        if j == target_face:
            facecolor = 'lightyellow'
            
        rect = patches.Rectangle((x, y), 1, 1, linewidth=2, edgecolor='black', facecolor=facecolor)
        ax.add_patch(rect)
        
        # 在目標面上畫線
        if j == target_face:
            if line_type == "左上到右下對角線":
                ax.plot([x, x + 1], [y + 1, y], color='red', linewidth=3)
            elif line_type == "左下到右上對角線":
                ax.plot([x, x + 1], [y, y + 1], color='red', linewidth=3)
            elif line_type == "水平線 (中分)":
                ax.plot([x, x + 1], [y + 0.5, y + 0.5], color='red', linewidth=3)
            elif line_type == "垂直線 (中分)":
                ax.plot([x + 0.5, x + 0.5], [y, y + 1], color='red', linewidth=3)

def main():
    st.set_page_config(page_title="立方體展開與分割線展示", layout="wide")
    st.title("立方體平面展開圖與分割線互動展示 🧊")
    st.markdown("透過左側面板調整設定，觀察線上在不同展開結構上的相對位置。")

    # 側邊欄設定
    st.sidebar.header("控制面板")
    
    view_mode = st.sidebar.radio("檢視模式", ["顯示所有 11 種展開圖", "顯示單一展開圖"])
    
    selected_net = None
    if view_mode == "顯示單一展開圖":
        # 讓使用者選擇 1~11 種的哪一種
        net_idx = st.sidebar.selectbox("選擇展開圖類型", range(1, 12))
        selected_net = net_idx - 1
    
    # 選擇要把線畫在哪一個面上 (0-5)
    target_face = st.sidebar.slider("選擇要畫線的面 (Index 0 ~ 5)", 0, 5, 1)
    
    # 選擇線的種類
    line_type = st.sidebar.selectbox(
        "選擇線條種類", 
        ["左上到右下對角線", "左下到右上對角線", "水平線 (中分)", "垂直線 (中分)"]
    )

    st.divider()

    # 繪圖區塊
    if view_mode == "顯示所有 11 種展開圖":
        fig, axes = plt.subplots(3, 4, figsize=(16, 12))
        axes = axes.flatten()
        
        for i, net in enumerate(cube_nets):
            draw_net(axes[i], net, target_face, line_type)
            axes[i].set_title(f"Net {i+1}")
            
        # 隱藏第12個空白子圖
        axes[11].axis('off')
        
        plt.tight_layout()
        st.pyplot(fig)
        
    else:
        # 顯示單一展開圖 (較大)
        fig, ax = plt.subplots(figsize=(6, 6))
        draw_net(ax, cube_nets[selected_net], target_face, line_type)
        ax.set_title(f"展開圖類型 {selected_net + 1}")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
