# PsychoPy Experiment with AI Response Generation

## Description
This is a psychological experiment built with PsychoPy that uses Ollama (Llama2) to generate AI responses with different similarity levels to participant inputs. The experiment presents scenarios to participants, collects their responses, generates AI alternatives, and asks participants to rate which AI response best matches their original answer.

## Features
- 3 predefined scenarios for psychological research
- Text input with German keyboard support
- AI response generation using Ollama/Llama2
- 3 similarity levels: high, medium, low
- Data collection and CSV export
- Multilingual support (German/English)

## Requirements
- Python 3.10+
- PsychoPy
- Ollama with Llama2 model
- Windows/macOS/Linux

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/psychopy-ai-experiment.git
cd psychopy-ai-experiment
```

### 2. Set up Python environment
```bash
python -m venv psychopy_env
# Windows:
psychopy_env\Scripts\activate
# macOS/Linux:
source psychopy_env/bin/activate
```

### 3. Install dependencies
```bash
pip install psychopy
```

### 4. Install Ollama
- Download and install Ollama from https://ollama.ai/
- Pull the Llama2 model: `ollama pull llama2`

## Usage

### Running the Experiment
```bash
python experiment.py
```

### Controls
- **ESC**: Quit experiment at any time
- **SPACE**: Continue to next screen
- **ENTER**: Submit response
- **1, 2, 3**: Select AI response rating
- **Backspace**: Delete characters while typing

### German Keyboard Support
- **Shift + Letter**: Capital letters (A, B, C...)
- **Shift + ä/ö/ü**: Capital umlauts (Ä, Ö, Ü)
- Full punctuation support for German keyboards

## File Structure
```
├── experiment.py          # Main experiment file
├── experiment_fixed.py    # Alternative version
├── experiment_data.csv    # Generated data (gitignored)
├── psychopy_env/         # Python environment (gitignored)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Data Output
The experiment saves data to `experiment_data.csv` with columns:
- `scenario`: The presented scenario
- `participant`: Participant's response
- `high`: High similarity AI response
- `medium`: Medium similarity AI response  
- `low`: Low similarity AI response
- `selected`: Which response the participant selected

## Customization

### Adding Scenarios
Edit the `SCENARIOS` list in `experiment.py`:
```python
SCENARIOS = [
    "Your custom scenario here...",
    "Another scenario...",
]
```

### Changing AI Model
Modify the `LLM_MODEL` variable:
```python
LLM_MODEL = "llama2"  # or "mistral", "codellama", etc.
```

## Troubleshooting

### Common Issues
1. **Ollama not found**: Make sure Ollama is installed and in PATH
2. **Model not available**: Run `ollama pull llama2`
3. **German characters not working**: Use the improved keyboard handling in experiment.py
4. **Text display issues**: Responses are automatically truncated and formatted

### Performance
- AI response generation may take 30-60 seconds per response
- Consider using a smaller model for faster generation
- Ensure adequate system resources (4GB+ RAM recommended)

## License
This project is for academic/research use. Please cite appropriately if used in publications.

## Contact
kimberly.eder@t-online.de
