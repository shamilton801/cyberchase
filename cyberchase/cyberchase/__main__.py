from .game import SeekerException, HiderException
from .match import Match
from .game import Game
import sys
import json

if len(sys.argv) != 4:
    print("Usage: \"python match.py seeker_file_name hider_file_name result_file_name\"")
    print("Requires that the seeker and hider files contain a first-letter-capitalized class with the same name as the file")
    sys.exit()

# Create Match 
seeker_file_name = sys.argv[1]
seeker_class_name = seeker_file_name.capitalize()

hider_file_name = sys.argv[2]
hider_class_name = hider_file_name.capitalize()

debug_message = "Match run sucessfully"
code_successful = True
failed_type = -1
try:
    try:
        exec(f"from {seeker_file_name} import {seeker_class_name}")
    except Exception as e:
        raise SeekerException(str(e))

    try:
        exec(f"from {hider_file_name} import {hider_class_name}")
    except Exception as e:
        raise HiderException(str(e))
    
    exec(f"match = Match({seeker_class_name}, {hider_class_name})")
    match.run()
except SeekerException as e:
    debug_message = f"Could not import Seeker code: {str(e)}"
    failed_type = Game.SEEKER
    code_successful = False
except HiderException as e:
    debug_message = f"Could not import Hider code: {str(e)}"
    failed_type = Game.HIDER
    code_successful = False
except Exception as e:
    debug_message = str(e)
    code_successful = False

result_file_name = sys.argv[3]
with open(f"{result_file_name}.json", "w") as f:
    result = {}
    if code_successful:
        result = match.get_result()
    else:
        result = Match.get_bad_launch(failed_type, debug_message)

    result["debug"] = debug_message
    json_str = json.dumps(result)
    f.write(json_str)