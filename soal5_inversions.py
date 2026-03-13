import random
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─────────────────────────────────────────────
# SOAL 5 — Inversions Counter
# ─────────────────────────────────────────────

def countInversionsNaive(arr):
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


def countInversionsSmart(arr):
    def mergeCount(left, right):
        result, inversions, i, j = [], 0, 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i]); i += 1
            else:
                result.append(right[j])
                inversions += len(left) - i
                j += 1
        result += left[i:]
        result += right[j:]
        return result, inversions

    def sortCount(arr):
        if len(arr) <= 1: return arr, 0
        mid = len(arr) // 2
        left,  inv_l = sortCount(arr[:mid])
        right, inv_r = sortCount(arr[mid:])
        merged, inv_s = mergeCount(left, right)
        return merged, inv_l + inv_r + inv_s

    _, total = sortCount(arr)
    return total


# ── Output teks — verifikasi ──────────────────
print("=" * 50)
print("SOAL 5 — Inversions Counter")
print("=" * 50)
print(f"{'Array':<25} | {'Naive':>6} | {'Smart':>6} | Match")
print("-" * 50)
for t in [[2,4,1,3,5], [5,4,3,2,1], [1,2,3,4,5], [3,1,2]]:
    n = countInversionsNaive(t)
    s = countInversionsSmart(t)
    print(f"{str(t):<25} | {n:>6} | {s:>6} | {'✓' if n == s else '✗'}")

# ── Output teks — benchmark ───────────────────
print(f"\n{'Size':<7} | {'Naive (ms)':>12} | {'Smart (ms)':>12} | {'Speedup':>8}")
print("-" * 50)
sizes = [1000, 5000, 10000]
naive_times, smart_times, speedups = [], [], []

for size in sizes:
    data = [random.randint(1, 100000) for _ in range(size)]

    t0 = time.perf_counter()
    r_naive = countInversionsNaive(data)
    naive_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    r_smart = countInversionsSmart(data)
    smart_ms = (time.perf_counter() - t0) * 1000

    sp = naive_ms / smart_ms
    naive_times.append(naive_ms)
    smart_times.append(smart_ms)
    speedups.append(sp)
    match = '✓' if r_naive == r_smart else '✗'
    print(f"{size:<7} | {naive_ms:>11.2f} | {smart_ms:>11.2f} | {sp:>7.1f}x  {match}")


# ── Visualisasi ───────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('Soal 5 — Inversions Counter: Naive vs Smart', fontsize=13)

# Chart 1: Waktu eksekusi
ax1 = axes[0]
ax1.plot(sizes, naive_times, 'o-', color='#D85A30', linewidth=2, markersize=7, label='Naive O(n²)')
ax1.plot(sizes, smart_times, 's-', color='#1D9E75', linewidth=2, markersize=7, label='Smart O(n log n)')
ax1.fill_between(sizes, naive_times, smart_times, alpha=0.1, color='#D85A30')
ax1.set_xlabel('Ukuran Array (n)')
ax1.set_ylabel('Waktu (ms)')
ax1.set_title('Waktu Eksekusi', fontsize=11)
ax1.legend(fontsize=9)
ax1.set_xticks(sizes)
ax1.set_xticklabels([f'{s:,}' for s in sizes])
for spine in ['top', 'right']: ax1.spines[spine].set_visible(False)

# Chart 2: Speedup bar
ax2 = axes[1]
bars = ax2.bar([f'n={s:,}' for s in sizes], speedups,
               color=['#B5D4F4', '#85B7EB', '#378ADD'], edgecolor='white', width=0.5)
for bar, sp in zip(bars, speedups):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
             f'{sp:.0f}x', ha='center', va='bottom', fontsize=12, fontweight='bold', color='#042C53')
ax2.set_ylabel('Speedup (kali lebih cepat)')
ax2.set_title('Speedup Smart vs Naive', fontsize=11)
for spine in ['top', 'right']: ax2.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig('soal5_inversions.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nDiagram disimpan: soal5_inversions.png")
