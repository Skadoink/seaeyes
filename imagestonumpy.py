"""
Create a numpy calibration dataset from a folder of images.

Saves an array of shape (N, H, W, C) dtype=uint8 by default, suitable
for use as calibration input for Hailo DFC optimization. Defaults to
`D:\\seaeyes-data-aabb\\images` as requested.

Usage:
	python imagestonumpy.py --images_dir "D:\\seaeyes-data-aabb\\images" \
		--out calibration_images.npy --size 640 640

Options:
	--images_dir  Directory with images (default shown above)
	--out         Output .npy filename (default: calibration_images.npy)
	--size        Width Height to resize images (default: keep original if omitted)
	--max         Maximum number of images to include
	--bgr         Save channels in BGR order instead of RGB

The script uses Pillow and numpy. Both are commonly available; install with
`pip install pillow numpy` if needed.
"""

from __future__ import annotations

import argparse
import glob
import os
from typing import List, Optional, Tuple

import numpy as np
from PIL import Image


def find_images(path: str) -> List[str]:
	exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif", "*.tiff")
	files: List[str] = []
	for e in exts:
		files.extend(glob.glob(os.path.join(path, e)))
	files = sorted(files)
	return files


def load_and_preprocess(
	filepaths: List[str],
	size: Optional[Tuple[int, int]] = None,
	to_bgr: bool = False,
	max_images: Optional[int] = None,
) -> np.ndarray:
	imgs: List[np.ndarray] = []
	count = 0
	for p in filepaths:
		if max_images is not None and count >= max_images:
			break
		try:
			im = Image.open(p).convert("RGB")
		except Exception:
			continue
		if size is not None:
			im = im.resize(size, Image.BILINEAR)
		arr = np.array(im, dtype=np.uint8)
		if to_bgr:
			arr = arr[..., ::-1]
		imgs.append(arr)
		count += 1
		print("Images loaded:", count, end="\r")
	if len(imgs) == 0:
		raise RuntimeError("No images loaded. Check the images_dir path and contents.")
	stacked = np.stack(imgs, axis=0)
	return stacked


def parse_size(s: Optional[List[int]]) -> Optional[Tuple[int, int]]:
	if s is None:
		return None
	if len(s) != 2:
		raise ValueError("--size expects two integers: WIDTH HEIGHT")
	return (int(s[0]), int(s[1]))


def main() -> None:
	p = argparse.ArgumentParser(description="Save calibration images as a numpy array")
	p.add_argument("--images_dir", default=r"D:\\seaeyes-data-aabb\\images")
	p.add_argument("--out", default="calibration_images.npy")
	p.add_argument("--size", default=[640, 640], nargs=2, type=int, help="Width Height (e.g. 640 640)")
	p.add_argument("--max", default=1024, type=int, help="Maximum number of images to include")
	p.add_argument("--bgr", action="store_true", help="Save channels in BGR order")
	args = p.parse_args()

	images_dir = args.images_dir
	if not os.path.isdir(images_dir):
		raise SystemExit(f"images_dir does not exist: {images_dir}")

	files = find_images(images_dir)
	if len(files) == 0:
		raise SystemExit(f"No image files found in {images_dir}")

	size = parse_size(args.size)

	arr = load_and_preprocess(files, size=size, to_bgr=args.bgr, max_images=args.max)

	np.save(args.out, arr)
	print(f"Saved {arr.shape[0]} images -> {args.out} (shape={arr.shape}, dtype={arr.dtype})")


if __name__ == "__main__":
	main()

