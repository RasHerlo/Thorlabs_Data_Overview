# -*- coding: utf-8 -*-
"""
Walk a Thorlabs recording tree: stack TIFFs, make averages/stats/PNGs, then a PDF overview.
"""

import os
import time

import imageio
import numpy as np
import tifffile

from Thorlabs_tif_stks import read_tif_stack, stack_tif_images, tif2png
from image_stats_generator import calculate_snr_frequency_domain, calculate_simple_snr
from PDF_report_generator import create_pdf_report

CHANNELS = ("ChanA", "ChanB")
DATA_DIR_NAME = "DATA"


def _marker_name(chan):
    return f"{chan}_001_001_001_001.tif"


def _channel_data_dir(recording_dir, chan):
    return os.path.join(recording_dir, DATA_DIR_NAME, chan)


def _should_stop(should_stop):
    return bool(should_stop and should_stop())


def run_folder_walk(root_dir, log=print, should_stop=None):
    """
    Process all Thorlabs recordings under root_dir.

    Existing stack/average/stats/PNG files are skipped, not overwritten.
    The PDF overview is always rewritten at the end.

    Returns a dict with pdf_path, recordings, errors, and stopped.
    """
    result = {
        "pdf_path": None,
        "recordings": 0,
        "errors": [],
        "stopped": False,
    }

    if not root_dir:
        log("No folder selected.")
        result["errors"].append("No folder selected.")
        return result

    root_dir = os.path.abspath(root_dir)
    if not os.path.isdir(root_dir):
        msg = f"Folder does not exist: {root_dir}"
        log(msg)
        result["errors"].append(msg)
        return result

    log(f"Selected folder: {root_dir}")
    log("Looking for Thorlabs recordings (ChanA / ChanB)...")

    recording_dirs = []
    for dirpath, _, files in os.walk(root_dir):
        file_set = set(files)
        if any(_marker_name(chan) in file_set for chan in CHANNELS):
            recording_dirs.append(dirpath)

    if not recording_dirs:
        log(
            "No recordings found. Choose the parent folder that contains "
            "files named like ChanA_001_001_001_001.tif."
        )
        return result

    log(f"Found {len(recording_dirs)} recording folder(s).")

    for recording_dir in recording_dirs:
        if _should_stop(should_stop):
            result["stopped"] = True
            log("Stopped by user.")
            return result

        result["recordings"] += 1
        log(f"--- {recording_dir}")
        files = set(os.listdir(recording_dir))

        for chan in CHANNELS:
            if _should_stop(should_stop):
                result["stopped"] = True
                log("Stopped by user.")
                return result

            if _marker_name(chan) not in files:
                continue

            try:
                _process_channel(recording_dir, chan, log=log)
            except Exception as exc:
                msg = f"[{chan}] Failed in {recording_dir}: {exc}"
                log(msg)
                result["errors"].append(msg)

    if _should_stop(should_stop):
        result["stopped"] = True
        log("Stopped by user before PDF.")
        return result

    log("Writing PDF overview...")
    try:
        pdf_path = create_pdf_report(root_dir, log=log)
        result["pdf_path"] = pdf_path
        log(f"PDF saved: {pdf_path}")
    except Exception as exc:
        msg = f"PDF report failed: {exc}"
        log(msg)
        result["errors"].append(msg)

    if result["errors"]:
        log(f"Finished with {len(result['errors'])} error(s).")
    else:
        log("Done.")
    return result


def _process_channel(recording_dir, chan, log=print):
    chandir = _channel_data_dir(recording_dir, chan)
    os.makedirs(chandir, exist_ok=True)

    stk_path = os.path.join(chandir, f"{chan}_stk.tif")
    avg_tif = os.path.join(chandir, f"{chan}_stk_avg.tif")
    avg_jpg = os.path.join(chandir, f"{chan}_stk_avg.jpg")
    avg_png = os.path.join(chandir, f"{chan}_stk_avg.png")
    stats_path = os.path.join(chandir, "stats.txt")

    if not os.path.isfile(stk_path):
        log(f"[{chan}] Creating stack...")
        start_time = time.time()
        stack_tif_images(recording_dir, chan, output_dir=chandir, log=log)
        log(f"[{chan}] Stack completed in {time.time() - start_time:.1f}s")
    else:
        log(f"[{chan}] Stack already exists, skipping")

    if not os.path.isfile(stk_path):
        raise FileNotFoundError(f"Stack was not created: {stk_path}")

    if not os.path.isfile(avg_tif):
        log(f"[{chan}] Creating average TIFF...")
        tif_stk = read_tif_stack(stk_path)
        tif_stk_avg = np.mean(tif_stk, axis=0)
        tifffile.imwrite(avg_tif, tif_stk_avg.astype(np.uint16))
        log(f"[{chan}] Average TIFF written")
    else:
        log(f"[{chan}] Average TIFF already exists, skipping")

    if not os.path.isfile(avg_jpg):
        log(f"[{chan}] Creating average JPEG...")
        tif_stk = read_tif_stack(stk_path)
        tif_stk_avg = np.mean(tif_stk, axis=0)
        imageio.imwrite(avg_jpg, tif_stk_avg.astype(np.uint8))
    else:
        log(f"[{chan}] Average JPEG already exists, skipping")

    if not os.path.isfile(stats_path):
        log(f"[{chan}] Generating SNR stats...")
        tif_stk_avg = read_tif_stack(avg_tif)
        snr_ft = calculate_snr_frequency_domain(tif_stk_avg)
        snr_basic = calculate_simple_snr(tif_stk_avg)
        with open(stats_path, "w") as file:
            file.write(f"SNR_basic = {snr_basic}\n")
            file.write(f"SNR_FT = {snr_ft}\n")
        log(f"[{chan}] SNR_basic = {snr_basic}")
        log(f"[{chan}] SNR_FT = {snr_ft}")
    else:
        log(f"[{chan}] Stats already exist, skipping")

    if os.path.isfile(avg_tif) and not os.path.isfile(avg_png):
        log(f"[{chan}] Creating PNG preview...")
        tif2png(avg_tif, avg_png)
        log(f"[{chan}] PNG written")
    elif os.path.isfile(avg_png):
        log(f"[{chan}] PNG already exists, skipping")


if __name__ == "__main__":
    from app import main
    main()
