from .match import Match
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

code = [
    f"from {seeker_file_name} import {seeker_class_name}",
    f"from {hider_file_name} import {hider_class_name}",
    f"match = Match({seeker_class_name}, {hider_class_name})",
]
exec("\n".join(code))

match.run()
result_file_name = sys.argv[3]
with open(f"{result_file_name}.json", "w") as f:
    result = match.get_result()
    result["seeker_name"] = sys.argv[1]
    result["hider_name"] = sys.argv[2]
    json_str = json.dumps(match.get_result())
    f.write(json_str)