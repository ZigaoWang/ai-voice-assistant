# AI Voice Assistant

This project is an AI Voice Assistant that uses OpenAI's GPT-4o models for natural language processing and Whisper for speech-to-text transcription. The assistant can have a back-and-forth conversation with the user, converting spoken input into text, generating a response, and converting the response back into speech.

## Features

- **Record Audio**: Record user input via a microphone.
- **Transcribe Audio**: Convert the recorded audio into text using OpenAI's Whisper model.
- **Generate Response**: Generate a response to the user's input using OpenAI's GPT-4 model.
- **Text-to-Speech**: Convert the generated text response back into speech.
- **Play Audio**: Play the generated speech response.
- **Continuous Conversation**: Maintain a conversation until the user decides to exit.

## Prerequisites

- Python 3.6 or later
- An OpenAI API key
- Required Python libraries: `openai`, `pyaudio`, `wave`, `simpleaudio`, `dotenv`, `pathlib`, `uuid`, `asyncio`

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ZigaoWang/ai-voice-assistant.git
    cd ai-voice-assistant
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory of the project and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your-openai-api-key
    OPENAI_BASE_URL=https://api.openai.com/v1
    ```

## Usage

1. **Run the script**:
    ```bash
    python main.py
    ```

2. **Interact with the assistant**:
    - The assistant will record your voice for 5 seconds.
    - It will transcribe your speech into text and generate a response.
    - The response will be converted to speech and played back to you.
    - The conversation will continue until you say "exit".

## Example Output

```plaintext
Recording...
Finished recording.
Transcription response: Hello.

User: Hello.

Assistant: Hello! How can I assist you today?
Recording...
Finished recording.
Transcription response: Can you tell me a joke?

User: Can you tell me a joke?

Assistant: Sure! Why don't scientists trust atoms? Because they make up everything!
...
```

## Contributing

1. **Fork the repository**.
2. **Create a new branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Make your changes**.
4. **Commit your changes**:
    ```bash
    git commit -m 'Add some feature'
    ```
5. **Push to the branch**:
    ```bash
    git push origin feature/your-feature-name
    ```
6. **Create a new Pull Request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://www.openai.com/) for providing the GPT-4 and Whisper models.
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) for audio recording.
- [SimpleAudio](https://simpleaudio.readthedocs.io/en/latest/) for audio playback.
- [dotenv](https://pypi.org/project/python-dotenv/) for managing environment variables.
