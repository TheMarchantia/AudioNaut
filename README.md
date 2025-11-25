# AudioNaut
AudioNaut is a customizable voice-controlled gaming interface. It lets players control any PC game using spoken commands mapped to keyboard and mouse actions. Commands are fully editable, making it easy to add, remove, or modify controls for any game.
# AudioNaut

AudioNaut is a customizable voice-controlled gaming interface. It lets players control any PC game using spoken commands mapped to keyboard and mouse actions. Commands are fully editable, making it easy to add, remove, or modify controls for any game.

## Features
- Fullscreen gaming UI
- Real-time speech recognition
- Editable voice command list
- Image-based manual
- Supports any PC game

## How to Run
1. Install Python 3.10+
2. Install requirements:
pip install -r requirements.txt

markdown
Copy code
3. Run the UI:
python voiceUI.py

perl
Copy code

## Add Your Own Commands
Open `Voice_Commands.py` and edit the `commands = { ... }` dictionary.  
You can add new voice phrases or change the actions they perform.

Example:
"reload weapon": "r",
"drive fast": "shift",

markdown
Copy code

## Requirements
- Python 3.10+
- Microphone
- Internet connection for speech recognition
