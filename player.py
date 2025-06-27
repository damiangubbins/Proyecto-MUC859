import time
from collections import defaultdict

import mido
import pyautogui

from console import BLU, CLR, GRN, YLW, clear, clear_line, fprint, top_print
from key_map import KEY_MAP


class Player:
    """A simple MIDI player that plays notes in real time using pyautogui."""

    midi_file: str
    mid: mido.MidiFile
    tempo: int = 500000
    ticks_per_beat: int
    note_events: list[tuple[float, int]] = []
    grouped_events: list[tuple[float, list[int]]] = []

    def __init__(self, midi_file_path: str):
        """Initialize the player with a MIDI file path."""
        clear()
        self.midi_file = midi_file_path
        self.load_song()
        self.read_metadata()
        self.read_notes()
        self.merge_chords()

    def load_song(self):
        """Load the MIDI file and process its metadata and notes."""
        fprint(2, BLU, "GIMidi Player v0.1.0")
        fprint(4, GRN, f"Loading song {self.midi_file}...")
        self.mid = mido.MidiFile(self.midi_file)

    def read_metadata(self):
        """Read metadata from the MIDI file, such as tempo and ticks per beat."""
        fprint(6, CLR, "Reading metadata...")

        for msg in self.mid:
            if msg.type == "set_tempo":
                self.tempo = msg.tempo
                break

        self.ticks_per_beat = self.mid.ticks_per_beat

    def read_notes(self):
        """Read note events from the MIDI file and accumulate them with real time."""
        fprint(7, CLR, "Reading notes...")

        for track in self.mid.tracks:
            abs_time_ticks = 0
            for msg in track:
                abs_time_ticks += msg.time
                if msg.type == "note_on" and msg.velocity > 0:
                    abs_time_sec = mido.tick2second(
                        abs_time_ticks, self.ticks_per_beat, self.tempo
                    )
                    self.note_events.append((abs_time_sec, msg.note))

        self.note_events.sort(key=lambda x: x[0])

    def merge_chords(self):
        """Merge chords into single events based on a time resolution."""
        fprint(8, CLR, "Merging notes...")

        TIME_RESOLUTION = 0.01
        grouped = defaultdict(list)

        for t, note in self.note_events:
            t_bucket = round(t / TIME_RESOLUTION) * TIME_RESOLUTION
            grouped[t_bucket].append(note)

        self.grouped_events = sorted(grouped.items())

    def play(self):
        """Play the MIDI file."""
        fprint(
            10,
            GRN,
            f"Done! Loaded {len(self.note_events)} notes ({len(self.grouped_events)} events)",
        )
        fprint(11, YLW, "Press enter to start playing...")
        input()
        fprint(14, CLR, "-" * 46)
        fprint(
            15, BLU, "Midi Notes".ljust(24), "Mapped Keys".ljust(16), "Time".ljust(6)
        )

        for i in range(3, 0, -1):
            fprint(13, CLR, f"Starting in {i} seconds...")
            time.sleep(1)
            clear_line()

        fprint(13, CLR, "Playing... Press Ctrl+C to stop.")

        start_time = time.time()
        for event_time, note in self.grouped_events:
            delay = event_time - (time.time() - start_time)
            if delay > 0:
                time.sleep(delay)

            keys = [KEY_MAP[n] for n in note if n in KEY_MAP]
            if keys:
                pyautogui.press(keys)
                notes_str = f"{' '.join(map(str, note))}".ljust(24)
                keys_str = f"{' '.join(map(lambda s: s.upper(), keys))}".ljust(16)
                time_elapsed = round(time.time() - start_time, 2)
                top_print(f"{notes_str}{keys_str}{time_elapsed}")
