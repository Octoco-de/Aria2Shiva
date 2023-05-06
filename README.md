# Aria2Shiva

This is a Telegram bot that allows you to search for movies and download their torrents. It's built using the Python programming language, and it uses the Telegram Bot API to interact with users.

## Requirements

To run this bot, you need to have Python, tmux, and aria2c installed on your system.


### Installing tmux on Unix and macOS

* To install tmux on Unix and macOS, follow these steps:

1. Open a terminal window.
2. Enter the following command to install tmux: 

```bash
sudo apt-get install tmux
```

* On macOS you can install it using Homebrew :

```bash
brew install tmux
```

### Installing aria2c on Unix

* To install aria2c on Unix and macOS, follow these steps:

1. Open a terminal window.
2. Enter the following command to install aria2c:
    
```bash
sudo apt-get install aria2
```

* On macOS you can install it using Homebrew :

```bash
brew install aria2
```


## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r Requirements.txt`.
3. Copy the `config.sample.py` file to `config.py` and add your Telegram bot token and allowed chat IDs with their passwords.

## Run
To start the bot, you can run the startBot script
```bash
bash startBot.sh
```

To stop the bot, you can run the stopBot script
```bash
bash stopBot.sh
```

## Usage

The user will be prompted to verify their identity by provideding the password that matches the one associated with their chat ID. Successful authentication will grant the user access for a duration of 8 hours.

To use the bot, send one of the following commands in a chat where the bot is a member:

- `/start`: Starts the bot and shows a welcome message.
- `/search [movie title]`: Searches for the given movie title on YTS and returns a list of results. Click on a result to download its torrent.
- `/download [torrent URL or magnet link]`: Downloads the given torrent using aria2c. You can also send a magnet link to download the associated torrent.
- `/whoami`: Returns the chat ID of the current chat.
- `/help`: Shows a list of available commands and their descriptions.

# Recommended Setup

It is recommended to run this bot in a virtual environment or a Docker container.

## To run in a virtual environment:

1. Create and activate a new virtual environment

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

2. Install dependencies as above
3. Follow usage instructions as above, but prefix commands with `python3` (e.g. `python3 bot.py`)

## To run in a Docker container:

1. Install Docker
2. Build the image:

   ```bash
   docker build -t telegram-torrent-bot .
   ```

3. Run the container:

   ```bash
   docker run --name telegram-torrent-bot -d telegram-torrent-bot
   ```

4. Follow usage instructions as above, but replace `./bot_start.sh` with:

   ```bash
   docker start telegram-torrent-bot
   ```

   and `./bot_stop.sh` with:

   ```bash
   docker stop telegram-torrent-bot
   ```


## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on GitHub. If you want to contribute code, please fork the repository and create a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
