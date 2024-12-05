import json
import os
from collections.abc import MutableMapping

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def flatten_locale(dictionary, parent_key='', separator='_'):
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten_locale(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items)

def compare_values(locale_data, dictionary_data):
    matches = []
    flat_locale = flatten_locale(locale_data)

    for dict_key, dict_value in dictionary_data.items():
        matching_locale = [{key: value} for key, value in flat_locale.items() if value == dict_value]
        if matching_locale:
            matches.append([
                dict_key,
                list(matching_locale[0].keys())[0]
            ])

    return matches

def get_mismatches(dictionaries_folder, locales_folder):
    en_dictionary_file = os.path.join(dictionaries_folder, f"en.dictionary.json")
    en_locale_file = os.path.join(locales_folder, f"en.default.schema.json")

    en_dictionary_data = load_json(en_dictionary_file)
    en_locale_data = load_json(en_locale_file)

    en_comparison = compare_values(en_locale_data, en_dictionary_data)
    en_matches = en_comparison

    languages = [file.split('.')[0] for file in os.listdir(dictionaries_folder) if file.endswith(".dictionary.json")]
    for language in languages:
        if language == "en": return

        dictionary_file = os.path.join(dictionaries_folder, f"{language}.dictionary.json")
        locale_file = os.path.join(locales_folder, f"{language}.schema.json")
        dictionary_data = load_json(dictionary_file)
        locale_data = load_json(locale_file)
        flat_locale = flatten_locale(locale_data)
        matches_count = 0
        mismatches = []

        for match in en_matches:
            dict_key = match[0]
            dict_val = dictionary_data[dict_key]
            loc_key = match[1]
            loc_val = flat_locale.get(loc_key, None)

            if dict_val != loc_val:
                mismatches.append([{dict_key: dict_val}, {loc_key: loc_val}])
            else:
                matches_count+= 1

        print('\n------------------------------------')
        print(f"{language} — matches {matches_count}, mismatches {len(mismatches)}")
        print('------------------------------------\n')
        print("Legend: [{Gengo translation}, {Newer translation}]\n")
        for mismatch in mismatches:
            print(mismatch)
        
if __name__ == "__main__":
    dictionaries_folder = "./dictionaries"
    locales_folder = "./locales"
    get_mismatches(dictionaries_folder, locales_folder)