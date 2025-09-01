# Stickman From Video

This repository contains `stickman_from_video.py`, a script that uses MediaPipe Pose to create a stickman representation from a video.

## Quick start

1. Install dependencies (recommended inside a virtual environment):

```bash
python -m pip install -r requirements.txt
```

2. Run the script from the project directory. Full path and personal username are redacted below:

```bash
cd '/Users/<redacted>/Desktop/Desktop - <redacted>\u2019s MacBook Pro/chappelleroan_dancemoves' \
&& /Users/<redacted>/.pyenv/versions/3.11.5/bin/python stickman_from_video.py -i hottogo.mp4 -o hottogo_stickman.mp4 --overlay
```

3. Portable alternative (if your Python is on PATH or using a venv):

```bash
cd /path/to/chappelleroan_dancemoves
python stickman_from_video.py -i hottogo.mp4 -o hottogo_stickman.mp4 --overlay
```

## Outputs

- The `-o/--output` argument specifies the white-background stickman output file (e.g. `hottogo_stickman.mp4`).
- If `--overlay` is provided, the script also writes an overlay video named `<output>_overlay.mp4` (stickman drawn over the original frames).

## Notes

- Use quotes or run the command from the directory if your path contains spaces or special characters.
- The script uses MediaPipe Pose which performs best with single-person videos.
- To change styling (colors, thickness, transparency) edit `stickman_from_video.py`.

## Contact

If you want additional features (semi-transparent overlay, JSON keypoints output, multi-person support), open an issue or request them here.
