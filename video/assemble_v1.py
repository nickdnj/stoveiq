#!/usr/bin/env python3
"""
StoveIQ Draft v1 Assembly Script
Builds stoveiq-draft-v1.mp4 from images, placeholder frames, and narration audio.

Structure:
  - Chapter title cards (white text on #111827, 3s each)
  - [VO] scenes: image + Ken Burns or gentle zoom + narration audio duration
  - [LIVE] placeholder scenes: dark frame + centered white text + specified duration
  - Background music mixed under everything (narration at 100%, music at ~12%)
  - Final mux: video-only concat + continuous audio track
"""

import subprocess
import os
import math
import sys

BASE     = os.path.expanduser("~/Workspaces/stoveiq-open/video")
IMAGES   = os.path.join(BASE, "assets/images")
NAR      = os.path.join(BASE, "audio/narration")
MUSIC    = os.path.join(BASE, "audio/music/ambient-pad.wav")
SEGS     = os.path.join(BASE, "assembly/segments")
NARNORM  = os.path.join(BASE, "assembly/narration_norm")
ASSEMBLY = os.path.join(BASE, "assembly")
OUTPUT   = os.path.join(BASE, "output/stoveiq-draft-v1.mp4")

FPS      = 30
W, H     = 1920, 1080
BG_COLOR = "0x111827"   # dark navy for placeholders / chapter cards
BG_HEX   = "#111827"    # same for ffmpeg color= filter


def run(cmd, label=""):
    """Run a shell command, print label, abort on failure."""
    print(f"\n>>> {label or cmd[:80]}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("STDERR:", result.stderr[-2000:])
        raise RuntimeError(f"Command failed ({label}): {cmd}")
    return result.stdout


def nar_path(scene_num):
    return os.path.join(NAR, f"scene_{scene_num:02d}.wav")


def seg_path(name):
    return os.path.join(SEGS, f"{name}.mp4")


# ---------------------------------------------------------------------------
# Segment generators
# ---------------------------------------------------------------------------

def make_placeholder(name, duration, label, note_text=None):
    """Dark background with centered label text (and optional second line)."""
    out = seg_path(name)
    safe_label = label.replace("'", "\\'").replace(":", "\\:")
    # Split long labels across two lines if needed
    drawtext = (
        f"drawtext=text='{safe_label}'"
        f":fontsize=38:fontcolor=white"
        f":x=(w-text_w)/2:y=(h-text_h)/2-20"
        f":borderw=2:bordercolor=black"
    )
    if note_text:
        safe_note = note_text.replace("'", "\\'").replace(":", "\\:")
        drawtext += (
            f",drawtext=text='{safe_note}'"
            f":fontsize=28:fontcolor=#AAAAAA"
            f":x=(w-text_w)/2:y=(h-text_h)/2+30"
            f":borderw=1:bordercolor=black"
        )
    cmd = (
        f'ffmpeg -y -f lavfi -i "color=c={BG_HEX}:s={W}x{H}:r={FPS}:d={duration}" '
        f'-vf "{drawtext}" '
        f'-c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p -t {duration} '
        f'"{out}"'
    )
    run(cmd, f"placeholder: {name}")
    return out


def make_chapter_card(name, title, duration=3.0):
    """White text chapter title on dark background."""
    out = seg_path(name)
    safe_title = title.replace("'", "\\'")
    cmd = (
        f'ffmpeg -y -f lavfi -i "color=c={BG_HEX}:s={W}x{H}:r={FPS}:d={duration}" '
        f'-vf "drawtext=text=\'{safe_title}\':fontsize=72:fontcolor=white'
        f':x=(w-text_w)/2:y=(h-text_h)/2:borderw=3:bordercolor=black" '
        f'-c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p -t {duration} '
        f'"{out}"'
    )
    run(cmd, f"chapter card: {title}")
    return out


def make_gentle_zoom(name, image, duration):
    """Gentle 1.0→1.03 zoom, landscape image."""
    out = seg_path(name)
    d_frames = int(math.ceil(duration * FPS))
    cmd = (
        f'ffmpeg -y -loop 1 -i "{image}" '
        f'-vf "scale=8000:-1,zoompan=z=\'min(zoom+0.0001,1.03)\':'
        f'x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':'
        f'd={d_frames}:s={W}x{H}:fps={FPS}" '
        f'-t {duration} -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p '
        f'"{out}"'
    )
    run(cmd, f"gentle-zoom: {name}")
    return out


def make_ken_burns_zoom(name, image, duration):
    """Ken Burns 1.0→1.15 zoom-in, landscape image."""
    out = seg_path(name)
    d_frames = int(math.ceil(duration * FPS))
    cmd = (
        f'ffmpeg -y -loop 1 -i "{image}" '
        f'-vf "scale=8000:-1,zoompan=z=\'min(zoom+0.0005,1.15)\':'
        f'x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':'
        f'd={d_frames}:s={W}x{H}:fps={FPS}" '
        f'-t {duration} -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p '
        f'"{out}"'
    )
    run(cmd, f"ken-burns-zoom: {name}")
    return out


def make_static(name, image, duration):
    """Static image scaled/padded to 1920x1080."""
    out = seg_path(name)
    cmd = (
        f'ffmpeg -y -loop 1 -i "{image}" '
        f'-vf "scale={W}:{H}:force_original_aspect_ratio=decrease,'
        f'pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black" '
        f'-t {duration} -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p -r {FPS} '
        f'"{out}"'
    )
    run(cmd, f"static: {name}")
    return out


def make_gentle_zoom_with_overlay(name, image, duration, overlay_text):
    """Gentle zoom with a text overlay in the lower third."""
    out = seg_path(name)
    d_frames = int(math.ceil(duration * FPS))
    safe_text = overlay_text.replace("'", "\\'")
    cmd = (
        f'ffmpeg -y -loop 1 -i "{image}" '
        f'-vf "scale=8000:-1,zoompan=z=\'min(zoom+0.0001,1.03)\':'
        f'x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':'
        f'd={d_frames}:s={W}x{H}:fps={FPS},'
        f'drawtext=text=\'{safe_text}\':fontsize=64:fontcolor=white'
        f':x=(w-text_w)/2:y=h-text_h-60:borderw=3:bordercolor=black" '
        f'-t {duration} -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p '
        f'"{out}"'
    )
    run(cmd, f"gentle-zoom+overlay: {name}")
    return out


# ---------------------------------------------------------------------------
# Step 1: Normalize narration audio
# ---------------------------------------------------------------------------

def normalize_narration():
    print("\n=== Step 1: Normalize narration audio ===")
    scenes_with_nar = [1, 2, 3, 4, 5, 6, 9, 17, 18, 19, 21, 22, 23]
    for s in scenes_with_nar:
        src = nar_path(s)
        dst = os.path.join(NARNORM, f"scene_{s:02d}-norm.wav")
        if not os.path.exists(src):
            print(f"  SKIP (missing): {src}")
            continue
        cmd = (
            f'ffmpeg -y -i "{src}" '
            f'-af "loudnorm=I=-16:TP=-1.5:LRA=11" '
            f'"{dst}"'
        )
        run(cmd, f"normalize scene {s:02d}")


# ---------------------------------------------------------------------------
# Step 2: Build all video segments (video-only, no audio)
# ---------------------------------------------------------------------------

# Scene plan: each entry is (segment_name, type, params, duration_seconds)
# Types: 'chapter', 'placeholder', 'gentle_zoom', 'ken_burns', 'static',
#        'gentle_zoom_overlay', 'placeholder_star'
#
# For [VO] scenes: duration = narration duration (from ffprobe)
# For [LIVE] placeholder scenes: duration = specified in assembly plan

SCENE_PLAN = [
    # --- Chapter 1: The Problem ---
    ("ch1_card",      "chapter",            {"title": "THE PROBLEM"},                         3.0),
    ("s01",           "placeholder",        {"label": "[FILM] Phone timer app + pot on stove"}, 6.52),
    ("s02",           "placeholder",        {"label": "[FILM] Probe thermometer / boilover montage"}, 11.58),
    ("s03",           "gentle_zoom",        {"image": "title_card.png"},                      12.15),

    # --- Chapter 2: The Idea ---
    ("ch2_card",      "chapter",            {"title": "THE IDEA"},                            3.0),
    ("s04",           "ken_burns",          {"image": "sensor_closeup.png"},                  15.75),
    ("s05",           "gentle_zoom",        {"image": "esp32_board.png"},                     12.77),
    ("s06",           "gentle_zoom_overlay",{"image": "sensor_closeup.png", "overlay": "$95 -> $50"},  15.05),

    # --- Chapter 3: The Build ---
    ("ch3_card",      "chapter",            {"title": "THE BUILD"},                           3.0),
    ("s07",           "placeholder",        {"label": "[FILM] Parts laid out on workbench"},  15.0),
    ("s08",           "placeholder",        {"label": "[FILM] Breadboard wiring close-up"},   45.0),
    ("s09",           "placeholder",        {"label": "[SCREEN CAPTURE] PlatformIO terminal"}, 21.20),
    ("s10",           "placeholder",        {"label": "[FILM] BLE provisioning on phone"},    25.0),
    ("s11",           "placeholder",        {"label": "[FILM] FIRST LIGHT — turn on burner",
                                             "note": "★ THE MONEY SHOT ★"},                   15.0),
    ("s12",           "gentle_zoom",        {"image": "pvc_enclosure.png"},                   10.0),

    # --- Chapter 4: The Cooking Coach ---
    ("ch4_card",      "chapter",            {"title": "THE COOKING COACH"},                   3.0),
    ("s13",           "placeholder",        {"label": "[FILM] Dashboard tour on phone"},      30.0),
    ("s14",           "placeholder",        {"label": "[FILM] Burner calibration on phone"},  30.0),
    ("s15",           "placeholder",        {"label": "[FILM] PASTA RECIPE COOKING DEMO",
                                             "note": "★ HERO SEQUENCE ★"},                    55.0),
    ("s16",           "placeholder",        {"label": "[FILM] Multiple burners active"},      10.0),
    ("s17",           "static",             {"image": "comparison_split.png"},                 6.60),

    # --- Chapter 5: The Recipe System ---
    ("ch5_card",      "chapter",            {"title": "THE RECIPE SYSTEM"},                   3.0),
    ("s18",           "placeholder",        {"label": "[SCREEN CAPTURE] VS Code showing recipe JSON"}, 30.28),
    ("s19",           "placeholder",        {"label": "[SCREEN CAPTURE] GitHub /recipes directory"}, 22.66),
    ("s20",           "placeholder",        {"label": "[FILM] Simulation mode demo"},         20.0),
    ("s21",           "placeholder",        {"label": "[SCREEN CAPTURE] JSON + Dashboard split"}, 5.32),

    # --- Chapter 6: What's Next ---
    ("ch6_card",      "chapter",            {"title": "WHAT'S NEXT"},                         3.0),
    ("s22",           "placeholder",        {"label": "[SCREEN CAPTURE] Hackaday + GitHub"},  10.17),
    ("s23",           "gentle_zoom",        {"image": "pcb_teaser.png"},                      13.39),
    ("s24",           "placeholder",        {"label": "[FILM] On-camera CTA holding device"}, 15.0),
]


def build_segments():
    print("\n=== Step 2: Build video segments ===")
    segment_files = []
    for entry in SCENE_PLAN:
        name, stype, params, duration = entry

        if stype == "chapter":
            f = make_chapter_card(name, params["title"])
        elif stype == "placeholder":
            note = params.get("note")
            f = make_placeholder(name, duration, params["label"], note)
        elif stype == "gentle_zoom":
            img = os.path.join(IMAGES, params["image"])
            f = make_gentle_zoom(name, img, duration)
        elif stype == "ken_burns":
            img = os.path.join(IMAGES, params["image"])
            f = make_ken_burns_zoom(name, img, duration)
        elif stype == "static":
            img = os.path.join(IMAGES, params["image"])
            f = make_static(name, img, duration)
        elif stype == "gentle_zoom_overlay":
            img = os.path.join(IMAGES, params["image"])
            f = make_gentle_zoom_with_overlay(name, img, duration, params["overlay"])
        else:
            raise ValueError(f"Unknown segment type: {stype}")

        segment_files.append((name, f, duration))

    return segment_files


# ---------------------------------------------------------------------------
# Step 3: Write concat file and join video-only
# ---------------------------------------------------------------------------

def concat_video(segment_files):
    print("\n=== Step 3: Concat video segments (video-only) ===")
    concat_txt = os.path.join(ASSEMBLY, "concat.txt")
    with open(concat_txt, "w") as fh:
        for name, path, dur in segment_files:
            fh.write(f"file '{path}'\n")

    raw_video = os.path.join(ASSEMBLY, "video-only.mp4")
    cmd = (
        f'ffmpeg -y -f concat -safe 0 -i "{concat_txt}" '
        f'-c copy "{raw_video}"'
    )
    run(cmd, "concat video-only")
    return raw_video


# ---------------------------------------------------------------------------
# Step 4: Build continuous narration track using adelay
# ---------------------------------------------------------------------------

def build_narration_track(segment_files):
    """
    Walk the segment list, accumulate time offset for each segment,
    insert the matching normalized narration wav at the right offset.
    Only scenes with narration audio get an entry.
    """
    print("\n=== Step 4: Build continuous narration track ===")

    # Map segment name → narration file
    nar_map = {
        "s01": "scene_01-norm.wav",
        "s02": "scene_02-norm.wav",
        "s03": "scene_03-norm.wav",
        "s04": "scene_04-norm.wav",
        "s05": "scene_05-norm.wav",
        "s06": "scene_06-norm.wav",
        "s09": "scene_09-norm.wav",
        "s17": "scene_17-norm.wav",
        "s18": "scene_18-norm.wav",
        "s19": "scene_19-norm.wav",
        "s21": "scene_21-norm.wav",
        "s22": "scene_22-norm.wav",
        "s23": "scene_23-norm.wav",
    }

    # Calculate cumulative start offsets
    offsets = {}
    t = 0.0
    for name, path, dur in segment_files:
        if name in nar_map:
            offsets[name] = t
        t += dur

    total_duration = t
    print(f"  Total video duration: {total_duration:.2f}s ({total_duration/60:.1f}m)")

    # Build the ffmpeg command with adelay
    inputs = []
    filter_parts = []
    mix_labels = []

    nar_entries = [(name, nar_map[name], offsets[name])
                   for name in nar_map if name in offsets]
    nar_entries.sort(key=lambda x: x[2])  # sort by time offset

    for i, (seg_name, nar_file, offset_sec) in enumerate(nar_entries):
        nar_full = os.path.join(NARNORM, nar_file)
        delay_ms = int(round(offset_sec * 1000))
        inputs.append(f'-i "{nar_full}"')
        filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]")
        mix_labels.append(f"[a{i}]")
        print(f"  Scene {seg_name}: offset {offset_sec:.2f}s ({delay_ms}ms)")

    n = len(nar_entries)
    mix_inputs = "".join(mix_labels)
    filter_complex = "; ".join(filter_parts)
    filter_complex += f"; {mix_inputs}amix=inputs={n}:duration=longest:normalize=0[out]"

    nar_continuous = os.path.join(ASSEMBLY, "narration-continuous.wav")
    cmd = (
        f'ffmpeg -y '
        + " ".join(inputs) + " "
        + f'-filter_complex "{filter_complex}" '
        + f'-map "[out]" "{nar_continuous}"'
    )
    run(cmd, "build continuous narration track")
    return nar_continuous, total_duration


# ---------------------------------------------------------------------------
# Step 5: Mix narration + music using Python/numpy
# ---------------------------------------------------------------------------

def mix_audio(nar_continuous, total_duration):
    print("\n=== Step 5: Mix narration + background music ===")
    try:
        import numpy as np
        import soundfile as sf
    except ImportError:
        print("  numpy/soundfile not available — falling back to FFmpeg mix")
        return mix_audio_ffmpeg(nar_continuous, total_duration)

    # Load narration
    nar_data, sr = sf.read(nar_continuous)
    if nar_data.ndim == 1:
        nar_data = np.column_stack([nar_data, nar_data])  # mono → stereo

    # Load music
    music_data, sr_m = sf.read(MUSIC)
    if music_data.ndim == 1:
        music_data = np.column_stack([music_data, music_data])

    # Resample music to match narration sample rate if needed
    if sr_m != sr:
        print(f"  WARNING: music sample rate {sr_m} != narration {sr} — using FFmpeg fallback")
        return mix_audio_ffmpeg(nar_continuous, total_duration)

    n_nar = len(nar_data)

    # Tile/trim music to match narration length
    if len(music_data) < n_nar:
        repeats = math.ceil(n_nar / len(music_data))
        music_data = np.tile(music_data, (repeats, 1))
    music_data = music_data[:n_nar]

    # Fade music in (3s) and out (3s)
    fade_samples = int(3.0 * sr)
    fade_in  = np.linspace(0, 1, min(fade_samples, n_nar))
    fade_out = np.linspace(1, 0, min(fade_samples, n_nar))
    music_data[:len(fade_in)]  *= fade_in[:, None]
    music_data[-len(fade_out):] *= fade_out[:, None]

    # Mix: narration 100%, music at 12%
    music_level = 0.12
    mixed = nar_data + music_data * music_level

    # Normalize to prevent clipping
    peak = np.max(np.abs(mixed))
    if peak > 0.95:
        mixed = mixed * (0.95 / peak)
        print(f"  Peak {peak:.3f} > 0.95 — normalizing")

    out = os.path.join(ASSEMBLY, "final-audio.wav")
    sf.write(out, mixed, sr)
    print(f"  Mixed audio written: {out}")
    return out


def mix_audio_ffmpeg(nar_continuous, total_duration):
    """FFmpeg fallback for audio mixing."""
    out = os.path.join(ASSEMBLY, "final-audio.wav")
    fade_out_st = max(0, total_duration - 3)
    cmd = (
        f'ffmpeg -y -i "{nar_continuous}" -i "{MUSIC}" '
        f'-filter_complex '
        f'"[1:a]volume=0.12,afade=t=in:st=0:d=3,afade=t=out:st={fade_out_st:.1f}:d=3[music];'
        f'[0:a][music]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]" '
        f'-map "[aout]" "{out}"'
    )
    run(cmd, "mix narration + music (FFmpeg fallback)")
    return out


# ---------------------------------------------------------------------------
# Step 6: Mux final video + audio and encode
# ---------------------------------------------------------------------------

def final_encode(raw_video, final_audio):
    print("\n=== Step 6: Final encode ===")
    cmd = (
        f'ffmpeg -y -i "{raw_video}" -i "{final_audio}" '
        f'-c:v libx264 -preset slow -crf 18 '
        f'-c:a aac -b:a 192k '
        f'-movflags +faststart -pix_fmt yuv420p '
        f'-shortest "{OUTPUT}"'
    )
    run(cmd, "final encode → stoveiq-draft-v1.mp4")


# ---------------------------------------------------------------------------
# Step 7: Verify audio levels
# ---------------------------------------------------------------------------

def verify_audio():
    print("\n=== Step 7: Verify audio levels ===")
    cmd = (
        f'ffmpeg -i "{OUTPUT}" -af "volumedetect" -f null /dev/null 2>&1 | '
        f'grep -E "mean_volume|max_volume"'
    )
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr
    for line in output.splitlines():
        if "mean_volume" in line or "max_volume" in line:
            print(f"  {line.strip()}")

    # Also get final file size and duration
    cmd2 = f'ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "{OUTPUT}"'
    r2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
    for line in r2.stdout.splitlines():
        print(f"  {line.strip()}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("StoveIQ Draft v1 Assembly")
    print("=" * 60)

    try:
        # Step 1: Normalize narration
        normalize_narration()

        # Step 2: Build all video segments
        segment_files = build_segments()

        # Step 3: Concat video-only
        raw_video = concat_video(segment_files)

        # Step 4: Build continuous narration track
        nar_continuous, total_duration = build_narration_track(segment_files)

        # Step 5: Mix narration + music
        final_audio = mix_audio(nar_continuous, total_duration)

        # Step 6: Final encode
        final_encode(raw_video, final_audio)

        # Step 7: Verify
        verify_audio()

        print("\n" + "=" * 60)
        print(f"DONE: {OUTPUT}")
        print("=" * 60)

    except Exception as e:
        print(f"\n!!! ASSEMBLY FAILED: {e}")
        sys.exit(1)
