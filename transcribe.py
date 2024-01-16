from openai import OpenAI
from pydub import AudioSegment
import os
import shutil
import whisper

# 폴더 경로 설정
folder_path = "/Users/jeehyun/Desktop/Study/Transcription/AudioSegments"

# 폴더가 존재하고, 파일이 있는지 확인
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # 폴더 내의 모든 파일 삭제
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

client = OpenAI()

# Path to your audio file
audio_file_path = "/Users/jeehyun/Desktop/Compsci3AC3_Lec1.m4a"

# Load the audio file
audio = AudioSegment.from_file(audio_file_path, "mp4")

# Length of each segment in milliseconds (20 minutes)
segment_length = 20 * 60 * 1000

# Determine the number of segments
num_segments = len(audio) // segment_length + (1 if len(audio) % segment_length else 0)

# Loop through and create each segment
for i in range(num_segments):
    start = i * segment_length
    end = min((i + 1) * segment_length, len(audio))
    segment = audio[start:end]

    # Export segment as a separate file
    segment.export(f"/Users/jeehyun/Desktop/Study/Transcription/AudioSegments/segment_{i+1}.mp3", format="mp3")


for i in range(num_segments):
    start = i * segment_length
    end = min((i + 1) * segment_length, len(audio))
    segment = audio[start:end]

    # Export segment as a separate file
    segment_file_path = f"/Users/jeehyun/Desktop/Study/Transcription/AudioSegments/segment_{i+1}.mp3"
    segment.export(segment_file_path, format="mp3")

    with open(segment_file_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        print(transcript)


model = whisper.load_model("base")

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("audio.mp3")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)