import time
from collections import defaultdict

import mido
import pyautogui

from key_map import KEY_MAP

# === SETTINGS ===
MIDI_FILE = "assets\\Minecraft_OST_Aria_Math_-_C418.mid"

# === LOAD MIDI FILE ===
mid = mido.MidiFile(MIDI_FILE)
tempo = 500000  # Default tempo

# Extract tempo if present
for msg in mid:
    if msg.type == "set_tempo":
        tempo = msg.tempo
        break

ticks_per_beat = mid.ticks_per_beat

# === ACCUMULATE NOTE EVENTS WITH REAL TIME ACROSS TRACKS ===
note_events = []

for track in mid.tracks:
    abs_time_ticks = 0
    for msg in track:
        abs_time_ticks += msg.time
        if msg.type == "note_on" and msg.velocity > 0:
            abs_time_sec = mido.tick2second(abs_time_ticks, ticks_per_beat, tempo)
            note_events.append((abs_time_sec, msg.note))

# Sort by real time
note_events.sort(key=lambda x: x[0])

# === MERGE CHORDS INTO SINGLE EVENTS ===
TIME_RESOLUTION = 0.01
grouped = defaultdict(list)

for t, note in note_events:
    t_bucket = round(t / TIME_RESOLUTION) * TIME_RESOLUTION
    grouped[t_bucket].append(note)

grouped_events = sorted(grouped.items())

# === PLAY NOTES IN REAL TIME ===
print(f"Playing {len(note_events)} notes... Starting in 3 seconds.")
time.sleep(3)

start_time = time.time()

for event_time, note in grouped_events:
    delay = event_time - (time.time() - start_time)
    if delay > 0:
        time.sleep(delay)

    keys = [KEY_MAP[n] for n in note if n in KEY_MAP]
    if keys:
        pyautogui.press(keys)
        print(
            f"Played note {note} -> keys '{keys}' at {round(time.time() - start_time, 2)}s"
        )
    else:
        print(f"Skipped note {note} (not in mapping)")

print("Finished playing.")
