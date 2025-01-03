import sys
import requests
from requests import HTTPError
import json
from bs4 import BeautifulSoup
import os

HOME = os.getenv("HOME")
BASE_URL = "https://en.wiktionary.org/api/rest_v1/page/definition/"
BASE_URL_HTML = "https://en.wiktionary.org/wiki/"
CONFIG_PATH = f"{HOME}/.config/meaning/config.json"
CONFIG = {
    "definitions_per_part_of_speech": 3,
    "examples_per_definition": 3,
    "language": "en",
}


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            try:
                temp_config = {}
                config_file_data = json.loads(f.read())
                if "definitions_per_part_of_speech" in config_file_data.keys():
                    temp_config["definitions_per_part_of_speech"] = config_file_data[
                        "definitions_per_part_of_speech"
                    ]
                if "examples_per_definition" in config_file_data.keys():
                    temp_config["examples_per_definition"] = config_file_data[
                        "examples_per_definition"
                    ]
                if "language" in config_file_data.keys():
                    temp_config["language"] = config_file_data["language"]

                for key in temp_config.keys():
                    CONFIG[key] = temp_config[key]

            except Exception as e:
                print("Configuration file is not valid json. Using default config.")


def load_options(options):
    for option in options:
        if option in [
            "-af",
            "-ast",
            "-bar",
            "-br",
            "-ca",
            "-ceb",
            "-da",
            "-de",
            "-en",
            "-es",
            "-et",
            "=eu",
            "-ff",
            "-fr",
            "-fy",
            "-gd",
            "-gl",
            "-ia",
            "-kw",
            "-la",
            "-nl",
            "-pam",
            "-pap",
            "-pi",
            "-pt",
            "-ro",
            "-tl",
            "-tpi",
            "-uz",
            "-vi",
            "-zh",
        ]:
            CONFIG["language"] = option[1:]

        if option.startswith("-d"):
            try:
                CONFIG["definitions_per_part_of_speech"] = int(option[2:])
            except:
                pass

        if option.startswith("-e"):
            try:
                CONFIG["examples_per_definition"] = int(option[2:])
            except:
                pass


def print_help():
    print(
        """
    Usage: meaning [options] <query>
    Options:
        -h, --help                Show this help message and exit
        -d<num>                   Set the number of definitions per part of speech (default: 3)
        -e<num>                   Set the number of examples per definition (default: 3)
        -<language_code>          Set the language for the definitions (default: en)
                                  Supported language codes: af, ast, bar, br, ca, ceb, da, de, en, es, et,
                                  eu, ff, fr, fy, gd, gl, ia, kw, la, nl, pam, pap, pi, pt, ro, tl, tpi, uz, vi, zh
    Default configuration file location: ~/.config/meaning/config.json
    Example:
        meaning -d5 -e2 -en apple
    """
    )
    sys.exit(0)


def fetch_definition(query):
    data = requests.get(BASE_URL + query)
    data.raise_for_status()
    json_data = json.loads(data.text)
    return json_data


def print_definition(definition_data):
    data = (
        definition_data[CONFIG["language"]]
        if CONFIG["language"] in definition_data.keys()
        else definition_data[next(iter(definition_data))]
    )
    language = data[0]["language"]
    print(f"Showing definition in {language}")

    if len(data) > 0:
        for data in data:
            print(data["partOfSpeech"] + "\n")
            definition_count = 1
            for definition in data["definitions"]:
                if len(definition["definition"]) > 0:

                    definition_text = (
                        BeautifulSoup(definition["definition"], "lxml")
                        .get_text()
                        .strip()
                    )

                    definition_text = definition_text.replace("\n", "\n\t")
                    print(f"{definition_count}:\t{definition_text}")

                    if "parsedExamples" in definition.keys():
                        example_count = 1
                        for parsedExample in definition["parsedExamples"]:
                            example = (
                                BeautifulSoup(parsedExample["example"], "lxml")
                                .get_text()
                                .strip()
                            )
                            print(f'\t->\t"{example}"')
                            if example_count < CONFIG["examples_per_definition"]:
                                example_count += 1
                            else:
                                break
                    if definition_count < CONFIG["definitions_per_part_of_speech"]:
                        definition_count += 1
                    else:
                        break
            print("-" * 50)


def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else sys.exit(-1)

    if "--help" in args or "-h" in args:
        print_help()

    options = []
    for arg in args:
        if arg.startswith("-"):
            options.append(arg)
    for arg in options:
        args.remove(arg)

    if len(args) < 1:
        print("No search query provided")
        sys.exit(-1)

    load_config()

    if len(options) > 0:
        load_options(options)

    try:
        query = args[0]
        definition_data = fetch_definition(query)
    except HTTPError as e:
        if e.response.status_code == 404:
            print(f"ERROR 404: Could not find definition for {query}")
        else:
            print(f"ERROR {e.response.status_code}: {e.response.text[:50]}")
        sys.exit(-1)
    except Exception as e:
        print(f"Error encountered: {e}")

    print_definition(definition_data)


if __name__ == "__main__":
    main()
    sys.exit(0)
