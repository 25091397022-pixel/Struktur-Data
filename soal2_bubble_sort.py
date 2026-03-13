import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec

# ─────────────────────────────────────────────
# SOAL 2 — Bubble Sort dengan Analisis Langkah
# ─────────────────────────────────────────────

def bubbleSort(arr):
    data = arr.copy()
    n = len(data)
    total_comparisons = 0
    total_swaps = 0
    passes_used = 0
    history = [data.copy()]

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            total_comparisons += 1
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                total_swaps += 1
                swapped = True
        passes_used += 1
        history.append(data.copy())
        print(f"Pass {passes_used}: {data}")
        if not swapped:
            break

    return data, total_comparisons, total_swaps, passes_used, history


# ── Output teks ──────────────────────────────
print("=" * 45)
print("SOAL 2 — Bubble Sort dengan Analisis Langkah")
print("=" * 45)

for label, test in [("Input [5,1,4,2,8]", [5,1,4,2,8]),
                    ("Input [1,2,3,4,5]", [1,2,3,4,5])]:
    print(f"\n=== {label} ===")
    sorted_arr, comps, swaps, passes, hist = bubbleSort(test)
    print(f"Sorted       : {sorted_arr}")
    print(f"Comparisons  : {comps}")
    print(f"Swaps        : {swaps}")
    print(f"Passes used  : {passes}")


# ── Visualisasi ───────────────────────────────
def draw_array(ax, arr, title, highlight=None):
    colors_map = highlight or {}
    ax.set_xlim(-0.5, len(arr) - 0.5)
    ax.set_ylim(0, max(arr) + 1)
    ax.set_title(title, fontsize=10, pad=6)
    ax.set_xticks(range(len(arr)))
    ax.set_xticklabels([str(v) for v in arr], fontsize=11)
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    for i, v in enumerate(arr):
        color = colors_map.get(i, '#B5D4F4')
        ax.bar(i, v, color=color, edgecolor='#B4B2A9', linewidth=0.8, width=0.6)
        ax.text(i, v + 0.1, str(v), ha='center', va='bottom', fontsize=10, fontweight='bold')

def visualize_bubble(arr, label):
    _, comps, swaps, passes, history = bubbleSort(arr)

    fig = plt.figure(figsize=(12, 3.5 * len(history)))
    fig.suptitle(f'Bubble Sort — {label}  |  Comparisons: {comps}  Swaps: {swaps}  Passes: {passes}',
                 fontsize=13, y=1.01)

    for idx, state in enumerate(history):
        ax = fig.add_subplot(len(history), 1, idx + 1)
        title = 'Array awal' if idx == 0 else f'Setelah pass {idx}'
        draw_array(ax, state, title)

    plt.tight_layout()
    fname = label.replace(' ', '_').replace('[', '').replace(']', '').replace(',', '')
    path = f'soal2_bubble_{fname}.png'
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Diagram disimpan: soal2_bubble_{fname}.png")

print("\n--- Generating diagrams ---")
visualize_bubble([5, 1, 4, 2, 8], "Input [5,1,4,2,8]")
visualize_bubble([1, 2, 3, 4, 5], "Input [1,2,3,4,5]")
