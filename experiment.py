# experiment_fixed.py
from psychopy import visual, event, core
import subprocess
import random
import csv
import os

# ---------- Configuration ----------
WINDOW_SIZE = [800, 600]
SCENARIOS = [
    "You find a wallet on the street. What do you do?",
    "A friend cancels plans last minute. How do you feel?",
    "You see someone drop their phone. What happens next?"
]
LLM_MODEL = "llama2"
OUTPUT_FILE = "experiment_data.csv"

# ---------- Helper Functions ----------
def query_ollama_simple(prompt):
    """Call Ollama and return the response."""
    try:
        result = subprocess.run(
            ["ollama", "run", LLM_MODEL],
            input=prompt,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def log_data(scenario, participant, llm_responses, selected_level):
    file_exists = os.path.exists(OUTPUT_FILE)
    with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['scenario','participant','high','medium','low','selected'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'scenario': scenario,
            'participant': participant,
            'high': llm_responses['high'],
            'medium': llm_responses['medium'],
            'low': llm_responses['low'],
            'selected': selected_level
        })

# ---------- Initialize PsychoPy ----------
win = visual.Window(WINDOW_SIZE, color='black')
instruction_text = visual.TextStim(win, text="Press any key to begin.\n(Press ESC at any time to quit)", height=0.1, color='white')
instruction_text.draw()
win.flip()
keys = event.waitKeys()
if 'escape' in keys:
    win.close()
    core.quit()

# ---------- Experiment Loop ----------
for scenario_num, scenario in enumerate(SCENARIOS, 1):
    # Show scenario
    scenario_text = f"Scenario {scenario_num}/3:\n\n{scenario}\n\nPress SPACE to continue (ESC to quit)"
    scenario_stim = visual.TextStim(win, text=scenario_text, height=0.08, color='white')
    scenario_stim.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    if 'escape' in keys:
        win.close()
        core.quit()

    # Participant response input
    prompt_text = visual.TextStim(win, text="Type your response (press ENTER when done, ESC to quit):", 
                                pos=(0, 0.3), height=0.06, color='white')
    participant_response = ""
    
    done = False
    while not done:
        display_text = participant_response + "_"  # Show cursor
        response_display = visual.TextStim(win, text=display_text, pos=(0, 0), 
                                         height=0.06, color='yellow', wrapWidth=1.8)
        
        prompt_text.draw()
        response_display.draw()
        win.flip()
        
        keys = event.getKeys(modifiers=True)  # Get modifiers (Shift, Ctrl, etc.)
        for key_info in keys:
            # Handle key information (key_info is a tuple: (key, modifiers))
            if isinstance(key_info, tuple):
                key, modifiers = key_info
            else:
                key = key_info
                modifiers = {}
            
            if key == 'escape':
                win.close()
                core.quit()
            elif key == 'return':
                if participant_response.strip():
                    done = True
            elif key == 'backspace':
                participant_response = participant_response[:-1]
            elif key == 'space':
                participant_response += ' '
            else:
                # Handle German keyboard and special characters with Shift support
                shift_pressed = modifiers.get('shift', False) if isinstance(modifiers, dict) else False
                
                # Map common German keyboard punctuation
                key_mapping = {
                    'period': '.',
                    'comma': ',',
                    'semicolon': ';',
                    'colon': ':',
                    'apostrophe': "'",
                    'quotedbl': '"',
                    'question': '?',
                    'exclam': '!',
                    'hyphen': '-',
                    'underscore': '_',
                    'plus': '+',
                    'equal': '=',
                    'slash': '/',
                    'backslash': '\\',
                    'parenleft': '(',
                    'parenright': ')',
                    'bracketleft': '[',
                    'bracketright': ']',
                    'braceleft': '{',
                    'braceright': '}',
                    'at': '@',
                    'numbersign': '#',
                    'dollar': '$',
                    'percent': '%',
                    'ampersand': '&',
                    'asterisk': '*'
                }
                
                # Special handling for Shift + punctuation on German keyboards
                shift_key_mapping = {
                    'period': ':',
                    'comma': ';',
                    'hyphen': '_',
                    'plus': '*',
                    'equal': '+',
                    'slash': '&',
                    'backslash': '?',
                    '1': '!',
                    '2': '"',
                    '3': '§',
                    '4': '$',
                    '5': '%',
                    '6': '&',
                    '7': '/',
                    '8': '(',
                    '9': ')',
                    '0': '='
                }
                
                # Check if it's a punctuation key with shift
                if shift_pressed and key in shift_key_mapping:
                    participant_response += shift_key_mapping[key]
                # Check if key is in regular mapping
                elif key in key_mapping:
                    participant_response += key_mapping[key]
                # Handle letters with proper capitalization
                elif len(key) == 1 and key.isalpha():
                    if shift_pressed:
                        participant_response += key.upper()
                    else:
                        participant_response += key.lower()
                # Handle German characters with shift
                elif key in 'äöüß':
                    if shift_pressed:
                        char_map = {'ä': 'Ä', 'ö': 'Ö', 'ü': 'Ü', 'ß': 'ß'}  # ß doesn't have uppercase
                        participant_response += char_map[key]
                    else:
                        participant_response += key
                # Handle numbers and other characters
                elif len(key) == 1 and (key.isdigit() or key.isprintable()):
                    participant_response += key

    # Show loading message
    loading_text = visual.TextStim(win, text="Generating AI responses... Please wait (this may take some time).",
                                 height=0.08, color='white')
    loading_text.draw()
    win.flip()
    
    # Prepare prompts with scenario context
    prompts = {
        'high': f"Given the scenario: '{scenario}'\n\nA person responded: '{participant_response}'\n\nWrite a short alternative that is very similar in style, tone, and content to their response. 1 short sentence without additional explanation.",
        'medium': f"Given the scenario: '{scenario}'\n\nA person responded: '{participant_response}'\n\nWrite a short alternative that is somewhat similar in style and content to their response, but with some variations. 1 short sentence without additional explanation.",
        'low': f"Given the scenario: '{scenario}'\n\nA person responded: '{participant_response}'\n\nWrite a short alternative that is loosely related to their response but with different style or approach. 1 short sentence without additional explanation."
    }
    
    # Generate responses
    llm_responses = {}
    for level, prompt in prompts.items():
        status_text = visual.TextStim(win, text=f"Generating {level} similarity response...",
                                    height=0.08, color='white')
        status_text.draw()
        win.flip()
        
        response = query_ollama_simple(prompt)
        # Truncate if too long
        if len(response) > 200:
            response = response[:200] + "..."
        llm_responses[level] = response
    
    # Show completion
    complete_text = visual.TextStim(win, text="Responses ready! Press any key to continue.",
                                  height=0.08, color='white')
    complete_text.draw()
    win.flip()
    event.waitKeys()

    # Randomize order for participant selection
    levels = list(llm_responses.keys())
    random.shuffle(levels)
    
    # Display responses for rating
    while True:
        # Clear screen with black background
        win.color = 'black'
        
        rating_text = visual.TextStim(win, text="Which response best fits your answer? Press 1, 2, or 3.",
                                    pos=(0, 0.4), height=0.05, color='white', wrapWidth=1.8)
        rating_text.draw()
        
        # Display responses with consistent formatting
        response_colors = ['lightgreen', 'lightblue', 'lightyellow']
        for i, level in enumerate(levels):
            # Clean and format the response
            response = llm_responses[level].strip()
            
            # Remove common LLM artifacts
            if response.startswith('"') and response.endswith('"'):
                response = response[1:-1]
            if response.startswith("'") and response.endswith("'"):
                response = response[1:-1]
            
            # Truncate if too long but preserve complete sentences
            if len(response) > 120:
                # Try to cut at sentence end
                sentences = response.split('. ')
                if len(sentences) > 1:
                    response = sentences[0] + '.'
                else:
                    response = response[:120] + "..."
            
            # Format with consistent numbering
            response_text = f"{i+1}. {response}"
            y_pos = 0.2 - (i * 0.25)  # Consistent spacing
            
            # Create text stimulus with consistent properties
            resp_stim = visual.TextStim(
                win, 
                text=response_text, 
                pos=(0, y_pos),
                height=0.04, 
                color=response_colors[i], 
                wrapWidth=1.8,
                alignText='center'
            )
            resp_stim.draw()
        
        win.flip()
        
        keys = event.getKeys(keyList=['1','2','3', 'escape'])
        if 'escape' in keys:
            # Allow escape to quit
            win.close()
            core.quit()
        elif keys:
            selected_index = int(keys[0]) - 1
            selected_level = levels[selected_index]
            break

    # Log trial data
    log_data(scenario, participant_response, llm_responses, selected_level)
    
    # Show brief confirmation
    confirm_text = visual.TextStim(win, text=f"Response {keys[0]} recorded. Press any key for next scenario.",
                                 height=0.08, color='green')
    confirm_text.draw()
    win.flip()
    event.waitKeys()

# ---------- End ----------
thanks_text = visual.TextStim(win, text="Thank you for participating!\nData saved to experiment_data.csv",
                            height=0.1, color='white')
thanks_text.draw()
win.flip()
core.wait(3)
win.close()
core.quit()