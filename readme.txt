How to run stickman_from_video.py

1) From the project directory run the script (paths and username redacted):

cd '/Users/<redacted>/Desktop/Desktop - <redacted>\u2019s MacBook Pro/directorys' && /Users/<redacted>/.pyenv/versions/3.11.5/bin/python stickman_from_video.py -i video.mp4 -o video_stickman.mp4 --overlay

2) Portable alternative (if your Python is on PATH or you use a venv):

cd /path/to/directory
python stickman_from_video.py -i hottogo.mp4 -o hottogo_stickman.mp4 --overlay

Notes:
- The --overlay flag creates two files: the white-background stickman (specified by -o) and an overlay version named <output>_overlay.mp4.
- Install dependencies first (recommended in a virtual environment):

python -m pip install -r requirements.txt

- If your shell reports issues with spaces/apostrophes in directory names, run the commands from the directory instead of using the full path.
