import argparse
import cv2
import numpy as np
import mediapipe as mp
import sys


def draw_stickman(frame, landmarks, connections, color=(0, 0, 0), thickness=4):
    h, w = frame.shape[:2]
    # blank white background
    canvas = 255 * np.ones_like(frame)

    # draw connections
    for a, b in connections:
        if a < len(landmarks) and b < len(landmarks):
            xa, ya = int(landmarks[a].x * w), int(landmarks[a].y * h)
            xb, yb = int(landmarks[b].x * w), int(landmarks[b].y * h)
            cv2.line(canvas, (xa, ya), (xb, yb), color, thickness)

    # draw keypoints
    for lm in landmarks:
        x, y = int(lm.x * w), int(lm.y * h)
        cv2.circle(canvas, (x, y), 5, (200, 0, 200), -1)

    return canvas


def main():
    parser = argparse.ArgumentParser(description="Create stickman video from input using MediaPipe Pose")
    parser.add_argument("--input", "-i", default="hottogo.mp4", help="Input video path")
    parser.add_argument("--output", "-o", default="stickman_mediapipe.mp4", help="Output video path for white-background stickman")
    parser.add_argument("--overlay", "-v", action="store_true", help="Also produce an overlay video with stickman drawn over original frames (output will be <output>_overlay.mp4)")
    parser.add_argument("--max_num_people", type=int, default=1, help="Max people to process (MediaPipe supports single-pose primarily)")
    args = parser.parse_args()

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        print(f"Failed to open input video: {args.input}")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

    # optionally create overlay writer
    overlay_writer = None
    if args.overlay:
        overlay_path = args.output.replace('.mp4', '') + '_overlay.mp4'
        overlay_writer = cv2.VideoWriter(overlay_path, fourcc, fps, (width, height))

    # Use MediaPipe Pose (33 keypoints)
    pose_connections = mp_pose.POSE_CONNECTIONS

    with mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                canvas = draw_stickman(frame, results.pose_landmarks.landmark, pose_connections)
                # create overlay by drawing same lines on a copy of original frame
                if overlay_writer is not None:
                    overlay_frame = frame.copy()
                    # draw connections on overlay_frame
                    h, w = overlay_frame.shape[:2]
                    for a, b in pose_connections:
                        if a < len(results.pose_landmarks.landmark) and b < len(results.pose_landmarks.landmark):
                            xa, ya = int(results.pose_landmarks.landmark[a].x * w), int(results.pose_landmarks.landmark[a].y * h)
                            xb, yb = int(results.pose_landmarks.landmark[b].x * w), int(results.pose_landmarks.landmark[b].y * h)
                            cv2.line(overlay_frame, (xa, ya), (xb, yb), (0, 0, 0), 4)
                    for lm in results.pose_landmarks.landmark:
                        x, y = int(lm.x * w), int(lm.y * h)
                        cv2.circle(overlay_frame, (x, y), 5, (200, 0, 200), -1)
                    overlay_writer.write(overlay_frame)
            else:
                canvas = 255 * np.ones_like(frame)
                if overlay_writer is not None:
                    overlay_writer.write(frame)

            out.write(canvas)
            frame_idx += 1

    cap.release()
    out.release()
    if overlay_writer is not None:
        overlay_writer.release()
    if overlay_writer is not None:
        print("✅ Stickman white canvas saved as", args.output)
        print("✅ Stickman overlay saved as", overlay_path)
    else:
        print("✅ Stickman dance saved as", args.output)


if __name__ == "__main__":
    main()