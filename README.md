This program will show mismatches between locale schema translations and verified translations that were done by Gengo.

The purpose of this tool is to expose new redundant translations made since the original Gengo translations were done. Since the newer, redundant ones were mostly done using LLMs, their accuracy is less certain. Therefore, they should be corrected to use the corresponding Gengo translation.

Gengo translations are in /dictionaries.

Only works with de, es, fr, & it schema translations.

### How to use it
1. Put schema JSON files in /locales
2. Make sure Python is installed
2. Run `python check_translations.py` or `python3 check_translations.py`

### How it works
1. Checks English translations for identical values, storing keys for both dictionaries and locales.
2. Uses the matched keys to compare each language.
3. Checks if the values and, therefore, the translations are the same for each language.
4. Gathers a list of mismatched translations and prints them out.