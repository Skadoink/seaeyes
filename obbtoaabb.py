from pathlib import Path

# === CONFIG ===
OBB_LABELS_DIR = Path(r"d:\seaeyes-data-obb\labels")   # original OBB labels
OUT_LABELS_DIR = Path(r"d:\seaeyes-data-aabb\labels") # new AABB labels

# =================

def convert_file(src, dst):
    lines_out = []

    with src.open("r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 9:
                # skip malformed lines
                continue

            cls = parts[0]
            coords = list(map(float, parts[1:]))

            xs = coords[0::2]
            ys = coords[1::2]

            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)

            # skip degenerate boxes
            if xmax <= xmin or ymax <= ymin:
                continue

            xc = (xmin + xmax) / 2
            yc = (ymin + ymax) / 2
            w = xmax - xmin
            h = ymax - ymin

            lines_out.append(
                f"{cls} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}"
            )

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("\n".join(lines_out))


def convert_all():
    for label_file in OBB_LABELS_DIR.rglob("*.txt"):
        rel = label_file.relative_to(OBB_LABELS_DIR)
        out_file = OUT_LABELS_DIR / rel
        convert_file(label_file, out_file)


if __name__ == "__main__":
    convert_all()
    print("✅ OBB → AABB conversion complete")
