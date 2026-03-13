import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─────────────────────────────────────────────
# SOAL 1 — Modified Binary Search
# ─────────────────────────────────────────────

def countOccurrences(sortedList, target):
    def findLeft(arr, target):
        lo, hi = 0, len(arr) - 1
        result = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == target:   result = mid; hi = mid - 1
            elif arr[mid] < target:  lo = mid + 1
            else:                    hi = mid - 1
        return result

    def findRight(arr, target):
        lo, hi = 0, len(arr) - 1
        result = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == target:   result = mid; lo = mid + 1
            elif arr[mid] < target:  lo = mid + 1
            else:                    hi = mid - 1
        return result

    left = findLeft(sortedList, target)
    if left == -1:
        return 0
    right = findRight(sortedList, target)
    return right - left + 1


# ── Output teks ──────────────────────────────
arr = [1, 2, 4, 4, 4, 4, 7, 9, 12]
print("=" * 45)
print("SOAL 1 — Modified Binary Search")
print("=" * 45)
print(f"Array  : {arr}")
print(f"Target 4 → count = {countOccurrences(arr, 4)}")
print(f"Target 5 → count = {countOccurrences(arr, 5)}")

# ── Visualisasi ───────────────────────────────
def visualize_binary_search(arr, target):
    left_idx  = next((i for i, v in enumerate(arr) if v == target), -1)
    right_idx = len(arr) - 1 - next((i for i, v in enumerate(reversed(arr)) if v == target), -1)
    count     = countOccurrences(arr, target)

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(-0.5, len(arr) - 0.5)
    ax.set_ylim(-0.5, 1.5)
    ax.axis('off')
    ax.set_title(f'countOccurrences({arr}, {target})  →  {count}', fontsize=13, pad=12)

    colors = []
    for i, v in enumerate(arr):
        if v == target:
            colors.append('#B5D4F4')
        else:
            colors.append('#F1EFE8')

    for i, v in enumerate(arr):
        rect = mpatches.FancyBboxPatch((i - 0.4, 0.3), 0.8, 0.8,
                                        boxstyle="round,pad=0.05",
                                        facecolor=colors[i],
                                        edgecolor='#B4B2A9', linewidth=1)
        ax.add_patch(rect)
        ax.text(i, 0.7, str(v), ha='center', va='center', fontsize=13, fontweight='bold',
                color='#042C53' if v == target else '#2C2C2A')
        ax.text(i, 0.15, str(i), ha='center', va='center', fontsize=9, color='#888780')

    if left_idx != -1:
        ax.annotate('left', xy=(left_idx, 1.1), ha='center', fontsize=10,
                    color='#185FA5', fontweight='bold')
        ax.annotate('right', xy=(right_idx, 1.1), ha='center', fontsize=10,
                    color='#185FA5', fontweight='bold')
        ax.annotate('', xy=(left_idx, 1.05), xytext=(right_idx, 1.05),
                    arrowprops=dict(arrowstyle='<->', color='#185FA5', lw=1.5))
        ax.text((left_idx + right_idx) / 2, 1.35,
                f'count = {count}', ha='center', fontsize=11,
                color='#185FA5', fontweight='bold')

    blue_patch = mpatches.Patch(facecolor='#B5D4F4', edgecolor='#B4B2A9', label=f'target = {target}')
    gray_patch = mpatches.Patch(facecolor='#F1EFE8', edgecolor='#B4B2A9', label='lainnya')
    ax.legend(handles=[blue_patch, gray_patch], loc='lower right', fontsize=9)

    plt.tight_layout()
    plt.savefig('soal1_binary_search.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Diagram disimpan: soal1_binary_search.png")

visualize_binary_search(arr, 4)
