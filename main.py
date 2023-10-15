import openai
import os
from pydub import AudioSegment

# Set your OpenAI API key here
openai.api_key = "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"

# Define the path to your audio file
audio_file_path = r"C:\Users\Peter\Desktop\julia.m4a"

# Function to transcribe audio using OpenAI API
def transcribe_audio(audio_data):
    return openai.Audio.transcribe("whisper-1", audio_data)

# Function to save transcriptions to a text file
def save_transcriptions_to_file(transcriptions, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for i, transcription in enumerate(transcriptions):
            file.write(f"Transcript for chunk {i}:\n")
            file.write(str(transcription) + "\n\n")  # Convert the OpenAI object to a string

def summarize_text(text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Summarize the following text: '{text}'",
        max_tokens=50  # You can adjust the max_tokens for the desired length of the summary
    )
    return response.choices[0].text

def divide_into_chunks(audio):
    target_chunk_size_bytes = 25 * 1024 * 1024  # 25MB
    current_start = 0
    current_end = 0
    chunks = []

    while current_end < len(audio):
        current_end += target_chunk_size_bytes
        if current_end > len(audio):
            current_end = len(audio)
        chunk = audio[current_start:current_end]
        chunks.append(chunk)

        current_start = current_end

    return chunks

def main():
    try:
        # Check the size of the audio file
        file_size = os.path.getsize(audio_file_path)

        if file_size <= 25 * 1024 * 1024:
            # If the file is not larger than 25MB, transcribe it directly
            with open(audio_file_path, "rb") as audio_file:
                transcript = transcribe_audio(audio_file)
                # Save the transcription to a text file
                save_transcriptions_to_file([transcript], "transcriptions.txt")
        else:
            # Load the large audio file using PyDub
            audio = AudioSegment.from_file(audio_file_path)

            # List to store transcriptions
            transcriptions = []

            # Split the audio into chunks, ensuring they are less than 25MB
            chunks = divide_into_chunks(audio)

            for i, chunk in enumerate(chunks):
                # Export the chunk as a temporary WAV file
                temp_wav_file = f"temp_chunk_{i}.wav"
                chunk.export(temp_wav_file, format="wav")

                # Open and read the temporary WAV file in binary mode
                with open(temp_wav_file, "rb") as audio_file:
                    # Transcribe the audio chunk using the OpenAI API
                    transcript = transcribe_audio(audio_file)
                    transcriptions.append(transcript)

                # Clean up the temporary WAV file
                os.remove(temp_wav_file)

            # Save all transcriptions to a text file
            save_transcriptions_to_file(transcriptions, "transcriptions.txt")
            
        print(summarize_text())

        print("Audio processing and transcription completed.")
    except Exception as e:
        print("Error occurred:", str(e))

if __name__ == "__main__":
    main()
