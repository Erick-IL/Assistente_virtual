# Virtual Assistant 🤖 (V0.1-alpha)

This repository contains the source code for a **Virtual Assistant** in Python, version **V0.1-alpha**. The assistant is in its initial version, with basic features that allow the user to interact via voice or text.

### Main Features ⚙️:
- **AI-based Question Answering:** The assistant can answer general questions using AI to generate responses.
- **Spotify Control:** Integration with Spotify, allowing control of music playback directly through the assistant (play, pause, next track, etc.).
- **Speech to Text:** Converts voice commands into text so that the assistant can interpret and respond accordingly.
- **Text to Speech:** The assistant can speak responses aloud, providing an interactive experience.
- **PC Control (Not working):** A feature under development to control some actions on the PC, such as opening programs or executing commands, which is not functional yet.

### Technologies Used:
- **Language:** Python
- **Libraries:** 
  - `SpeechRecognition` (for speech-to-text conversion)
  - `edge-tts` (for text-to-speech synthesis)
  - `spotipy` (for Spotify integration)
  - `gemini-api` (for answering questions using AI)

### How to Use:
1. **Setup:**
   - Clone this repository.
      ```bash
       git clone Erick-IL/Assistente_virtual
       ```

   - Install the necessary dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```
2. **Spotify Setup:**
   - Set up your Spotify API credentials in the configuration file.
      - https://developer.spotify.com/documentation/web-api
3. **Gemini AI Setup**
   - Set up your Gemini AI API credentials in the configuration file.
     - https://ai.google.dev/gemini-api/docs/api-key
    
3. **Running the Assistant:**
   - Start the assistant by running the main script:
     ```bash
     python virtual_assistant.py
     ```
   - The assistant will begin listening to voice commands and respond either through voice or text.

### Version:
- **V0.1-alpha:** This is the first functional version of the assistant, with some features operational and others still under development. Additional functionalities will be added in future versions.

### Contributions:
This repository is in its early stages, and contributions are welcome! If you'd like to help improve the project, feel free to open a **pull request** or report bugs.

**Full Changelog**: https://github.com/Erick-IL/Assistente_virtual/commits/v0.1-alpha
