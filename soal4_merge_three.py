import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─────────────────────────────────────────────
# SOAL 4 — Merge Tiga Sorted Lists
# ─────────────────────────────────────────────

def mergeThreeSortedLists(listA, listB, listC):
    result = []
    i, j, k = 0, 0, 0
    lenA, lenB, lenC = len(listA), len(listB), len(listC)
    steps = []  # simpan langkah untuk visualisasi

    while i < lenA and j < lenB and k < lenC:
        a, b, c = listA[i], listB[j], listC[k]
        if a <= b and a <= c:
            steps.append(('A', i, a))
            result.append(a); i += 1
        elif b <= a and b <= c:
            steps.append(('B', j, b))
            result.append(b); j += 1
        else:
            steps.append(('C', k, c))
            result.append(c); k += 1

    while i < lenA and j < lenB:
        if listA[i] <= listB[j]: steps.append(('A', i, listA[i])); result.append(listA[i]); i += 1
        else: steps.append(('B', j, listB[j])); result.append(listB[j]); j += 1
    while i < lenA and k < lenC:
        if listA[i] <= listC[k]: steps.append(('A', i, listA[i])); result.append(listA[i]); i += 1
        else: steps.append(('C', k, listC[k])); result.append(listC[k]); k += 1
    while j < lenB and k < lenC:
        if listB[j] <= listC[k]: steps.append(('B', j, listB[j])); result.append(listB[j]); j += 1
        else: steps.append(('C', k, listC[k])); result.append(listC[k]); k += 1
    while i < lenA: steps.append(('A', i, listA[i])); result.append(listA[i]); i += 1
    while j < lenB: steps.append(('B', j, listB[j])); result.append(listB[j]); j += 1
    while k < lenC: steps.append(('C', k, listC[k])); result.append(listC[k]); k += 1

    return result, steps


# ── Output teks ──────────────────────────────
print("=" * 45)
print("SOAL 4 — Merge Tiga Sorted Lists")
print("=" * 45)

tests = [
    ([1, 5, 9], [2, 6, 10], [3, 4, 7]),
    ([1, 4, 7], [2, 5, 8], [3, 6, 9]),
    ([], [1, 3], [2, 4]),
    ([5], [1, 2], [3, 4, 6]),
]
for a, b, c in tests:
    result, _ = mergeThreeSortedLists(a, b, c)
    print(f"mergeThreeSortedLists({a}, {b}, {c})")
    print(f"  → {result}\n")


# ── Visualisasi ───────────────────────────────
def visualize_merge(listA, listB, listC):
    result, steps = mergeThreeSortedLists(listA, listB, listC)
    color_map = {'A': '#B5D4F4', 'B': '#9FE1CB', 'C': '#FAC775'}
    source_map = {v: s for s, _, v in reversed(steps)}  # warna per nilai hasil

    fig, axes = plt.subplots(4, 1, figsize=(11, 6))
    fig.suptitle(f'Merge Three Sorted Lists\n{listA} + {listB} + {listC}', fontsize=12)

    for ax, lst, label, color in zip(
        axes[:3],
        [listA, listB, listC],
        ['List A', 'List B', 'List C'],
        ['#B5D4F4', '#9FE1CB', '#FAC775']
    ):
        ax.set_xlim(-0.5, max(len(listA), len(listB), len(listC), len(result)) - 0.5)
        ax.set_ylim(0, 2)
        ax.axis('off')
        ax.set_title(label, fontsize=9, loc='left', pad=2)
        for i, v in enumerate(lst):
            rect = mpatches.FancyBboxPatch((i - 0.35, 0.4), 0.7, 0.9,
                                            boxstyle="round,pad=0.05",
                                            facecolor=color, edgecolor='#B4B2A9', linewidth=0.8)
            ax.add_patch(rect)
            ax.text(i, 0.85, str(v), ha='center', va='center', fontsize=12, fontweight='bold')

    ax4 = axes[3]
    ax4.set_xlim(-0.5, len(result) - 0.5)
    ax4.set_ylim(0, 2)
    ax4.axis('off')
    ax4.set_title('Result', fontsize=9, loc='left', pad=2)
    for i, v in enumerate(result):
        src = source_map.get(v, 'A')
        color = color_map[src]
        rect = mpatches.FancyBboxPatch((i - 0.35, 0.4), 0.7, 0.9,
                                        boxstyle="round,pad=0.05",
                                        facecolor=color, edgecolor='#B4B2A9', linewidth=0.8)
        ax4.add_patch(rect)
        ax4.text(i, 0.85, str(v), ha='center', va='center', fontsize=12, fontweight='bold')

    patches = [
        mpatches.Patch(color='#B5D4F4', label='dari List A'),
        mpatches.Patch(color='#9FE1CB', label='dari List B'),
        mpatches.Patch(color='#FAC775', label='dari List C'),
    ]
    fig.legend(handles=patches, loc='lower center', ncol=3, fontsize=9, frameon=False)
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig('soal4_merge_three.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Diagram disimpan: soal4_merge_three.png")

visualize_merge([1, 5, 9], [2, 6, 10], [3, 4, 7])
