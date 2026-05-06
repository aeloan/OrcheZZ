import io
import librosa
import numpy as np

from pydub import AudioSegment

NOTES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
]


def note_to_index(note):
    return NOTES.index(note)


def frequency_to_midi(freq):
    return round(69 + 12 * np.log2(freq / 440.0))


def midi_to_note(midi):
    return NOTES[midi % 12]


def detect_note_from_bytes(audio_bytes):

    # lecture du webm
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

    # conversion en mono numpy
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)

    if audio.channels == 2:
        samples = samples.reshape((-1, 2))
        samples = samples.mean(axis=1)

    sr = audio.frame_rate

    f0 = librosa.yin(
        samples,
        fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7'),
        sr=sr
    )

    # enlève valeurs invalides
    f0 = f0[np.isfinite(f0)]

    if len(f0) == 0:
        return None

    freq = np.median(f0)

    midi = frequency_to_midi(freq)

    return midi_to_note(midi)


def compare_notes(audio_bytes, target_note):

    detected_note = detect_note_from_bytes(audio_bytes)

    print("Detected:", detected_note)

    if detected_note is None:
        return 0.0

    target_index = note_to_index(target_note)
    detected_index = note_to_index(detected_note)

    distance = abs(target_index - detected_index)

    # distance circulaire
    distance = min(distance, 12 - distance)

    score = max(0, 1 - distance / 6)

    return score


def mix_audios(round_audios):
    # Filtrer les None et décoder les audios valides
    audios = [
        AudioSegment.from_file(io.BytesIO(b), format="webm")
        for b in round_audios if b is not None
    ]

    if not audios:
        return AudioSegment.empty()

    base = audios[0]

    for audio in audios[1:]:
        base = base.overlay(audio)

    return base

# Tests
if __name__ == "__main__":

    with open("si.webm", "rb") as f:
        dataSi = f.read()

    with open("do.webm", "rb") as f:
        dataDo = f.read()

    mixed = mix_audios([dataSi, dataDo])
    mixed.export("output.wav", format="wav")

    with open("output.wav", "rb") as f:
        data = f.read()

    score = compare_notes(data, "B")

    print("Score:", score)