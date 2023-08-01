import json
import re

def clean_emoticons(input):
    tempstring = input
    try:
        emoji_removed_string = re.sub(r'[^\x00-\x7F]+', '', tempstring)

        return emoji_removed_string.strip()
    
    except Exception as e:
        print (e)

        return tempstring
    

def iterate_json_dict_clean(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict) or isinstance(value, list):
                iterate_json_dict_clean(value)
            elif isinstance(value, str):
                obj[key] = clean_emoticons(value)
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict) or isinstance(item, list):
                iterate_json_dict_clean(item)
            elif isinstance(item, str):
                print("String found")
                idx = obj.index(item)
                obj[key] = clean_emoticons(value)
    return obj


def clean_json_file(file_path):
    print ('cleaning from input file')
    # Open the JSON file
    json_file_path = 'connections.json'
    with open(json_file_path, "r") as json_file:
        connect_map = json.load(json_file)

    pre_cleaned_array = connect_map
    cleaned_array = iterate_json_dict_clean(pre_cleaned_array)
    output_file_path = file_path[:file_path.find('.json')] + '__emoticons_removed.json'

    with open(output_file_path, 'w') as f:
        json.dump(cleaned_array, f, indent=4)

    print ('demoticoned connection file saved to', output_file_path)
    return output_file_path

def clean_json_obj(json_obj):
    print ('cleaning input object')

    pre_cleaned_array = json_obj
    cleaned_array = iterate_json_dict_clean(pre_cleaned_array)

    return cleaned_array









if __name__ == "__main__":
    print ('testing')