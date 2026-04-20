#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Segmentare parcele agricole din imagini aeriene oblice, folosind:
- mascarea overlay-urilor (compas, mini-hartă, telemetrie)
- uniformizare cromatică
- SLIC superpixels
- watershed
- calcul arie/perimetru în pixeli
- export imagine anotată + preview-uri

Utilizare:
    python detect_parcels_unified.py --input "3 test.jpg"

Opțional:
    python detect_parcels_unified.py --input "3 test.jpg" --gsd 0.5

Dacă specifici --gsd (metri/pixel), scriptul calculează și aria în m² și perimetrul în metri.
"""

import argparse
from pathlib import Path

import cv2
import numpy as np
from skimage.segmentation import slic, watershed, find_boundaries
from skimage.color import rgb2lab
from skimage.feature import peak_local_max
from scipy import ndimage as ndi


def build_overlay_mask(h: int, w: int,
                       compass=(0, 70, 430, 470),
                       minimap=(0, 930, 560, None),
                       telemetry=(1040, 820, None, None)) -> np.ndarray:
    """
    Creează o mască de validitate:
    255 = zonă analizabilă
    0   = overlay-uri grafice de ignorat
    """
    mask = np.ones((h, w), dtype=np.uint8) * 255

    cx1, cy1, cx2, cy2 = compass
    mx1, my1, mx2, my2 = minimap
    tx1, ty1, tx2, ty2 = telemetry

    cv2.rectangle(mask, (cx1, cy1), (cx2, cy2), 0, -1)
    cv2.rectangle(mask, (mx1, my1), (w if mx2 is None else mx2, h if my2 is None else my2), 0, -1)
    cv2.rectangle(mask, (tx1, ty1), (w if tx2 is None else tx2, h if ty2 is None else ty2), 0, -1)

    return mask


def segment_parcels(
    img_bgr: np.ndarray,
    valid_mask: np.ndarray,
    n_segments: int = 360,
    compactness: float = 12.0,
    sigma: float = 1.2,
    bright_thresh: int = 148,
    min_distance: int = 36,
    peak_threshold_abs: float = 0.12,
    min_area_px: int = 12000,
    max_aspect_ratio: float = 18.0,
    top_ignore_y: int = 100,
):
    """
    Returnează:
    - overlay imagine anotată
    - slic preview
    - land mask
    - elevation map
    - listă cu rezultate
    """
    valid_bool = valid_mask.astype(bool)

    # 1) netezire / uniformizare
    smoothed_bgr = cv2.pyrMeanShiftFiltering(img_bgr, sp=18, sr=28)
    smoothed_rgb = cv2.cvtColor(smoothed_bgr, cv2.COLOR_BGR2RGB)
    lab = rgb2lab(smoothed_rgb)

    # 2) SLIC
    segments = slic(
        lab,
        n_segments=n_segments,
        compactness=compactness,
        sigma=sigma,
        start_label=1,
        mask=valid_bool,
        channel_axis=-1
    )

    # 3) harta de relief pentru watershed
    gray = cv2.cvtColor(smoothed_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    grad = cv2.morphologyEx(
        gray,
        cv2.MORPH_GRADIENT,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )

    slic_bounds = find_boundaries(segments, mode="outer").astype(np.uint8) * 255

    _, bright = cv2.threshold(gray, bright_thresh, 255, cv2.THRESH_BINARY)
    bright = cv2.morphologyEx(
        bright,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),
        iterations=1
    )

    elevation = cv2.normalize(grad, None, 0, 255, cv2.NORM_MINMAX)
    elevation = cv2.addWeighted(elevation, 0.8, slic_bounds, 0.8, 0)
    elevation = cv2.addWeighted(elevation, 1.0, bright, 0.35, 0)
    elevation = np.where(valid_bool, elevation, 255).astype(np.uint8)

    # 4) mască teren, pe HSV
    hsv = cv2.cvtColor(smoothed_bgr, cv2.COLOR_BGR2HSV)

    mask_green = cv2.inRange(hsv, np.array([25, 15, 20]), np.array([100, 255, 255]))
    mask_brown = cv2.inRange(hsv, np.array([4, 15, 20]), np.array([30, 255, 220]))
    mask_darkveg = cv2.inRange(hsv, np.array([18, 5, 8]), np.array([90, 180, 135]))

    land = cv2.bitwise_or(mask_green, mask_brown)
    land = cv2.bitwise_or(land, mask_darkveg)
    land = cv2.bitwise_and(land, valid_mask)

    land = cv2.morphologyEx(
        land,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)),
        iterations=2
    )
    land = cv2.morphologyEx(
        land,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
        iterations=1
    )

    # 5) markeri pentru watershed
    dist = cv2.distanceTransform(land, cv2.DIST_L2, 5)
    dist_norm = cv2.normalize(dist, None, 0, 1.0, cv2.NORM_MINMAX)

    coords = peak_local_max(
        dist_norm,
        min_distance=min_distance,
        threshold_abs=peak_threshold_abs,
        labels=(land > 0)
    )

    markers = np.zeros_like(gray, dtype=np.int32)
    for i, (r, c) in enumerate(coords, start=1):
        markers[r, c] = i
    markers = ndi.label(markers > 0)[0]

    labels_ws = watershed(elevation, markers=markers, mask=(land > 0))

    # 6) vizualizări
    overlay = img_bgr.copy()
    slic_preview = img_bgr.copy()
    slic_preview[slic_bounds > 0] = (255, 255, 255)

    # 7) extragere parcele
    results = []
    parcel_id = 1

    for lbl in np.unique(labels_ws):
        if lbl == 0:
            continue

        reg = np.uint8(labels_ws == lbl) * 255
        area_px = int(cv2.countNonZero(reg))
        if area_px < min_area_px:
            continue

        contours, _ = cv2.findContours(reg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            continue

        cnt = max(contours, key=cv2.contourArea)
        cnt_area = cv2.contourArea(cnt)
        if cnt_area < min_area_px:
            continue

        x, y, ww, hh = cv2.boundingRect(cnt)
        if y < top_ignore_y:
            continue

        aspect = max(ww / max(hh, 1), hh / max(ww, 1))
        if aspect > max_aspect_ratio:
            continue

        perim = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.0035 * perim, True)

        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = x + ww // 2, y + hh // 2

        cv2.drawContours(overlay, [approx], -1, (255, 255, 255), 3)
        cv2.putText(
            overlay, f"P{parcel_id}",
            (max(10, cx - 28), max(25, cy - 15)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA
        )
        cv2.putText(
            overlay, f"A={int(cnt_area):,} px2",
            (max(10, cx - 85), max(45, cy + 12)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.54, (255, 255, 255), 2, cv2.LINE_AA
        )
        cv2.putText(
            overlay, f"P={int(perim):,} px",
            (max(10, cx - 70), max(65, cy + 36)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.54, (255, 255, 255), 2, cv2.LINE_AA
        )

        results.append({
            "parcel": parcel_id,
            "area_px2": int(cnt_area),
            "perimeter_px": float(perim),
            "bbox": [int(x), int(y), int(ww), int(hh)],
            "contour": approx.reshape(-1, 2).tolist()
        })
        parcel_id += 1

    return overlay, slic_preview, land, elevation, results


def save_results(base_path: Path, overlay, slic_preview, land, elevation, results, gsd=None):
    stem = base_path.stem
    parent = base_path.parent

    overlay_path = parent / f"{stem}_annotated.png"
    slic_path = parent / f"{stem}_slic_preview.png"
    land_path = parent / f"{stem}_land_mask.png"
    elev_path = parent / f"{stem}_elevation_map.png"
    txt_path = parent / f"{stem}_results.txt"

    cv2.imwrite(str(overlay_path), overlay)
    cv2.imwrite(str(slic_path), slic_preview)
    cv2.imwrite(str(land_path), land)
    cv2.imwrite(str(elev_path), elevation)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Imagine: {base_path.name}\n")
        f.write(f"Parcele detectate: {len(results)}\n\n")
        for r in results:
            f.write(f"Parcela P{r['parcel']}\n")
            f.write(f"  area_px2 = {r['area_px2']}\n")
            f.write(f"  perimeter_px = {r['perimeter_px']:.2f}\n")
            if gsd is not None:
                area_m2 = r["area_px2"] * (gsd ** 2)
                perimeter_m = r["perimeter_px"] * gsd
                f.write(f"  area_m2 = {area_m2:.2f}\n")
                f.write(f"  perimeter_m = {perimeter_m:.2f}\n")
            f.write(f"  bbox = {r['bbox']}\n")
            f.write("\n")

    return overlay_path, slic_path, land_path, elev_path, txt_path


def parse_args():
    parser = argparse.ArgumentParser(description="Detectare parcele agricole din imagini aeriene oblice.")
    parser.add_argument("--input", required=True, help="Calea către imagine.")
    parser.add_argument("--gsd", type=float, default=None, help="Ground Sampling Distance, metri/pixel.")
    parser.add_argument("--n_segments", type=int, default=360, help="Număr SLIC superpixeli.")
    parser.add_argument("--compactness", type=float, default=12.0, help="Compactness pentru SLIC.")
    parser.add_argument("--sigma", type=float, default=1.2, help="Sigma pentru SLIC.")
    parser.add_argument("--bright_thresh", type=int, default=148, help="Prag pentru zone luminoase.")
    parser.add_argument("--min_distance", type=int, default=36, help="Distanță minimă între markeri.")
    parser.add_argument("--peak_threshold_abs", type=float, default=0.12, help="Prag marker distanță.")
    parser.add_argument("--min_area_px", type=int, default=12000, help="Aria minimă a unei parcele.")
    parser.add_argument("--max_aspect_ratio", type=float, default=18.0, help="Raport maxim lățime/înălțime.")
    parser.add_argument("--top_ignore_y", type=int, default=100, help="Ignoră fragmentele de sus până la acest y.")
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)

    img_bgr = cv2.imread(str(input_path))
    if img_bgr is None:
        raise FileNotFoundError(f"Nu am găsit imaginea: {input_path}")

    h, w = img_bgr.shape[:2]

    # Mască generică pentru acest tip de capturi.
    valid_mask = build_overlay_mask(
        h, w,
        compass=(0, 70, 430, 470),
        minimap=(0, 930, 560, None),
        telemetry=(1040, 820, None, None)
    )

    overlay, slic_preview, land, elevation, results = segment_parcels(
        img_bgr=img_bgr,
        valid_mask=valid_mask,
        n_segments=args.n_segments,
        compactness=args.compactness,
        sigma=args.sigma,
        bright_thresh=args.bright_thresh,
        min_distance=args.min_distance,
        peak_threshold_abs=args.peak_threshold_abs,
        min_area_px=args.min_area_px,
        max_aspect_ratio=args.max_aspect_ratio,
        top_ignore_y=args.top_ignore_y,
    )

    overlay_path, slic_path, land_path, elev_path, txt_path = save_results(
        base_path=input_path,
        overlay=overlay,
        slic_preview=slic_preview,
        land=land,
        elevation=elevation,
        results=results,
        gsd=args.gsd
    )

    print(f"Procesare terminată pentru: {input_path.name}")
    print(f"Parcele detectate: {len(results)}")
    print(f"Imagine anotată: {overlay_path}")
    print(f"SLIC preview: {slic_path}")
    print(f"Land mask: {land_path}")
    print(f"Elevation map: {elev_path}")
    print(f"Raport text: {txt_path}")

    if results:
        print("\nPrimele rezultate:")
        for r in results[:10]:
            line = f"P{r['parcel']}: area={r['area_px2']} px2, perimeter={r['perimeter_px']:.2f} px"
            if args.gsd is not None:
                area_m2 = r["area_px2"] * (args.gsd ** 2)
                perimeter_m = r["perimeter_px"] * args.gsd
                line += f", area={area_m2:.2f} m2, perimeter={perimeter_m:.2f} m"
            print(line)


if __name__ == "__main__":
    main()
