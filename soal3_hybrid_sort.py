import random
import matplotlib.pyplot as plt
import numpy as np

# ─────────────────────────────────────────────
# SOAL 3 — Hybrid Sort
# ─────────────────────────────────────────────

def insertionSort(arr, start=0, end=None):
    if end is None: end = len(arr)
    comparisons, swaps = 0, 0
    for i in range(start + 1, end):
        key = arr[i]
        j = i - 1
        while j >= start:
            comparisons += 1
            if arr[j] > key: arr[j + 1] = arr[j]; swaps += 1; j -= 1
            else: break
        arr[j + 1] = key
    return comparisons, swaps

def selectionSort(arr, start=0, end=None):
    if end is None: end = len(arr)
    comparisons, swaps = 0, 0
    for i in range(start, end - 1):
        min_idx = i
        for j in range(i + 1, end):
            comparisons += 1
            if arr[j] < arr[min_idx]: min_idx = j
        if min_idx != i: arr[i], arr[min_idx] = arr[min_idx], arr[i]; swaps += 1
    return comparisons, swaps

def hybridSort(theSeq, threshold=10):
    arr = theSeq.copy()
    n = len(arr)
    tc, ts = 0, 0
    for start in range(0, n, threshold):
        end = min(start + threshold, n)
        sub_len = end - start
        c, s = insertionSort(arr, start, end) if sub_len <= threshold else selectionSort(arr, start, end)
        tc += c; ts += s
    for size in range(threshold, n, threshold):
        c, s = insertionSort(arr, 0, min(size + threshold, n))
        tc += c; ts += s
    return arr, tc, ts

def pureInsertionSort(theSeq):
    arr = theSeq.copy()
    c, s = insertionSort(arr)
    return arr, c, s

def pureSelectionSort(theSeq):
    arr = theSeq.copy()
    c, s = selectionSort(arr)
    return arr, c, s


# ── Output teks ──────────────────────────────
print("=" * 65)
print("SOAL 3 — Hybrid Sort")
print("=" * 65)
print(f"{'Size':<6} | {'Algorithm':<20} | {'Comparisons':>12} | {'Swaps':>8} | {'Total Ops':>10}")
print("-" * 65)

sizes = [50, 100, 500]
results_data = {s: {} for s in sizes}

for size in sizes:
    data = [random.randint(1, 1000) for _ in range(size)]
    _, hc, hs = hybridSort(data)
    _, ic, is_ = pureInsertionSort(data)
    _, sc, ss = pureSelectionSort(data)
    results_data[size] = {
        'Hybrid':    (hc, hs, hc+hs),
        'Insertion': (ic, is_, ic+is_),
        'Selection': (sc, ss, sc+ss),
    }
    for i, (name, (comp, swap, total)) in enumerate(results_data[size].items()):
        label = str(size) if i == 0 else ''
        print(f"{label:<6} | {name + ' Sort':<20} | {comp:>12,} | {swap:>8,} | {total:>10,}")
    print("-" * 65)


# ── Visualisasi ───────────────────────────────
labels     = [str(s) for s in sizes]
hybrid_ops = [results_data[s]['Hybrid'][2]    for s in sizes]
insert_ops = [results_data[s]['Insertion'][2] for s in sizes]
select_ops = [results_data[s]['Selection'][2] for s in sizes]

x = np.arange(len(sizes))
w = 0.25

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('Soal 3 — Hybrid Sort: Perbandingan Total Operasi', fontsize=13)

# Bar chart
ax = axes[0]
b1 = ax.bar(x - w, hybrid_ops, w, label='Hybrid Sort',    color='#378ADD', edgecolor='white')
b2 = ax.bar(x,     insert_ops, w, label='Insertion Sort', color='#1D9E75', edgecolor='white')
b3 = ax.bar(x + w, select_ops, w, label='Selection Sort', color='#D85A30', edgecolor='white')
ax.set_xticks(x)
ax.set_xticklabels([f'n={s}' for s in sizes])
ax.set_ylabel('Total Operasi')
ax.set_title('Total Ops (Comparisons + Swaps)', fontsize=11)
ax.legend(fontsize=9)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{int(v):,}'))
for spine in ['top', 'right']: ax.spines[spine].set_visible(False)

# Stacked comparisons vs swaps untuk Hybrid
ax2 = axes[1]
hc_vals = [results_data[s]['Hybrid'][0] for s in sizes]
hs_vals = [results_data[s]['Hybrid'][1] for s in sizes]
ax2.bar(x, hc_vals, label='Comparisons', color='#378ADD', edgecolor='white')
ax2.bar(x, hs_vals, bottom=hc_vals, label='Swaps', color='#85B7EB', edgecolor='white')
ax2.set_xticks(x)
ax2.set_xticklabels([f'n={s}' for s in sizes])
ax2.set_ylabel('Operasi')
ax2.set_title('Hybrid Sort: Breakdown Comparisons vs Swaps', fontsize=11)
ax2.legend(fontsize=9)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{int(v):,}'))
for spine in ['top', 'right']: ax2.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig('soal3_hybrid_sort.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nDiagram disimpan: soal3_hybrid_sort.png")
