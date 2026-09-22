import os
import tempfile
import unittest
from pathlib import Path

import numpy as np
import tifffile

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Main_Folder_Walk import run_folder_walk


class FolderWalkTests(unittest.TestCase):
    def test_missing_folder(self):
        result = run_folder_walk("Z:\\this_folder_should_not_exist_thorlabs", log=lambda *_: None)
        self.assertIsNone(result["pdf_path"])
        self.assertTrue(result["errors"])

    def test_no_recordings(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_folder_walk(tmp, log=lambda *_: None)
            self.assertEqual(result["recordings"], 0)
            self.assertIsNone(result["pdf_path"])

    def test_creates_stack_avg_stats_png_and_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            rec = Path(tmp) / "sample_recording"
            rec.mkdir()
            frame = np.arange(64, dtype=np.uint16).reshape(8, 8)
            tifffile.imwrite(rec / "ChanA_001_001_001_001.tif", frame)
            tifffile.imwrite(rec / "ChanA_001_001_001_002.tif", frame + 1)

            logs = []
            result = run_folder_walk(tmp, log=logs.append)

            self.assertEqual(result["recordings"], 1)
            self.assertFalse(result["errors"], msg="\n".join(result["errors"]))
            self.assertTrue(os.path.isfile(result["pdf_path"]))

            chan_dir = rec / "DATA" / "ChanA"
            self.assertTrue((chan_dir / "ChanA_stk.tif").is_file())
            self.assertTrue((chan_dir / "ChanA_stk_avg.tif").is_file())
            self.assertTrue((chan_dir / "stats.txt").is_file())
            self.assertTrue((chan_dir / "ChanA_stk_avg.png").is_file())

            logs.clear()
            second = run_folder_walk(tmp, log=logs.append)
            self.assertFalse(second["errors"])
            self.assertTrue(any("Stack already exists" in line for line in logs))


if __name__ == "__main__":
    unittest.main()
