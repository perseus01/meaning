# Meaning

A Python script that fetches the meanings of words from [**Wiktionary.org**](https://www.wiktionary.org/) and displays them in a formatted manner directly on the command line. 

## Requirements

- **Python**: `>= 3.10`
- **Linux**: A C compiler is required to compile the script into a binary. Refer to the [Nuitka user manual](https://nuitka.net/user-documentation/user-manual.html#c-compiler) for detailed instructions.

## Features

- Fetch and display meanings of words from Wiktionary.
- Configurable settings via `config.json`.
- Compile the script into a standalone binary for easier execution.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/perseus01/meaning.git
cd meaning
```

### 2. Create a virtual environment
For **bash** or **zsh**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

For **fish** shell:
```fish
python3 -m venv .venv
source .venv/bin/activate.fish
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

### Fetch a word's meaning
To get the meaning of a word:
```bash
python3 meaning.py <word>
```

Example:
```bash
python3 meaning.py hello
```

### View the help menu
```bash
python3 meaning.py -h
```

---

## Configuration

You can customize the script using a `config.json` file.  
1. Copy the example `config.json` from the repository.
2. Place it in `~/.config/meaning/config.json`.
3. Modify it according to your preferences.

---

## Compiling the Script

To create a standalone binary:
1. Ensure you have a C compiler installed on your system (refer to [Nuitka user manual](https://nuitka.net/user-documentation/user-manual.html#c-compiler) for details).
2. Run the `build.sh` script:
   ```bash
   ./build.sh
   ```
3. The compiled binary will be available in the current directory. Execute it with:
   ```bash
   ./meaning <word>
   ```

---

## Example Commands

1. Fetching the meaning of a word:
   ```bash
   python3 meaning.py dictionary
   ```
2. Viewing the help menu:
   ```bash
   python3 meaning.py -h
   ```
3. Running the compiled binary:
   ```bash
   ./meaning universe
   ```

---

## Example Output

```
$ python3 meaning.py example
Showing definition in English
Noun

1:      Something that is representative of all such things in a group.
2:      Something that serves to illustrate or explain a rule.
3:      Something that serves as a pattern of behaviour to be imitated (a good example) or not to be imitated (a bad example).
        ->      "Nelson Mandela was an example for many to follow."
--------------------------------------------------
Verb

1:      To be illustrated or exemplified (by). (Can we add an example for this sense?)
--------------------------------------------------
```
