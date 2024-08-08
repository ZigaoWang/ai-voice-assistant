import os
import openai
import pyaudio
import wave
import simpleaudio as sa
from dotenv import load_dotenv
from pathlib import Path
import uuid

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI with API key and base URL
api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')
client = openai.OpenAI(api_key=api_key, base_url=base_url)


def record_audio(file_path):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    rate = 44100  # Record at 44100 samples per second
    record_seconds = 5

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print("Recording...")

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 5 seconds
    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print("Finished recording.")

    # Save the recorded data as a WAV file
    with wave.open(str(file_path), 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))


def play_audio(file_path):
    wave_obj = sa.WaveObject.from_wave_file(str(file_path))
    play_obj = wave_obj.play()
    play_obj.wait_done()


def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text"
        )
    print("Transcription response:", transcription)  # Debug print to see the response structure
    return transcription if isinstance(transcription, str) else transcription.get('text')


def generate_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=4096,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()


def text_to_speech(text, file_path):
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=text,
            response_format="wav"  # Request the response in WAV format
        )

        # Print response type and content for debugging
        print(f"Response Type: {type(response)}")
        print(f"Response: {response}")

        # Stream the response directly to the file
        response.stream_to_file(str(file_path))

        # Check if the file starts with 'RIFF'
        with open(file_path, 'rb') as f:
            header = f.read(4)
            if header != b'RIFF':
                raise wave.Error('file does not start with RIFF id')

    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        raise


def is_valid_wav(file_path):
    try:
        with wave.open(str(file_path), 'rb') as wf:
            return True
    except wave.Error as e:
        print(f"Invalid WAV file: {e}")
        return False


if __name__ == '__main__':
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    while True:
        # Record user input
        audio_file_path = Path(f"temp_{uuid.uuid4()}.wav")
        record_audio(audio_file_path)

        # Transcribe the audio to text
        user_input = transcribe_audio(audio_file_path)
        print(f"User: {user_input}")

        # Append user input to conversation
        conversation.append({"role": "user", "content": user_input})

        # Generate a response from the model
        assistant_response = generate_response(conversation)
        print(f"Assistant: {assistant_response}")

        # Append assistant response to conversation
        conversation.append({"role": "assistant", "content": assistant_response})

        # Convert the response to speech
        speech_file_path = Path(f"speech_{uuid.uuid4()}.wav")
        text_to_speech(assistant_response, speech_file_path)

        # Validate the generated speech file
        if is_valid_wav(speech_file_path):
            # Play the generated speech
            play_audio(speech_file_path)
        else:
            print("Generated speech file is not valid.")

        # Clean up temporary files
        os.remove(audio_file_path)
        os.remove(speech_file_path)