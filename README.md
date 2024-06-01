# Pokemon Card Bot/Terminal

This project aims to interact with users through a Discord bot or a quick terminal application to provide information about Pokemon cards.

## APIs Used

This project uses the following APIs:

- [Pokemon TCG API](https://pokemontcg.io/): This API is used to fetch information about Pokemon cards.

Remember to obtain your own API keys for these services and place them in the `secret.py` file as `TCG_API_KEY`.

## Structure

The project is structured into four main modules:

- `discordBot`: This folder contains the the Discord bot implementation.
- `terminalApp`: This folder contains the terminal application implementation.
- `APIs`: This folder contains the module that implements the interface to the Trading card game API.
- `classes`: This folder contains the `Card` class which is used to represent a Pokemon card.

## Usage

### Discord Bot

To use the Discord bot, you need to have a Discord bot token. This should be placed in the `secret.py` file as `DISCORD_KEY`.
To execute `bot.py` you could both use the command `python bot.py` depending from the path you execute the command from,
or you could simply open the script using a text editor with python debug extension such as vs code.

The bot responds to the following commands:

- `Get <Pokemon name>`: Search for all cards of the specified Pokemon. After showing the cards, the bot will ask you to choose a card by entering its ID. Finally, the bot will post the image and market prices of the chosen card. If you do not choose a card within 120 seconds, the conversation will be closed and you will need to send a Get command again.

- `Random`: Returns a random pokemon card

- `Help` Show this help message.

The commands are case-sensitive and make sure to write the names of the Pokemon correctly!

### Terminal Application

The aim of this part is so you can quickly test the functions of this project via CLI, without having to create a discord bot.

Run the `main.py` script in the `terminalApp` directory. To execute this you could both use the command `python main.py` 
depending from the path you execute the command from, or you could simply open and execute the script using a text editor with python debug extension such as vs code.

Depending on what feature you choose will be prompted to enter the name of a Pokemon or you will be returned a random pokemon card. In the first case, after entering the name, you will be shown a list of cards for that Pokemon. You can then enter the ID of a card to get more information about it.
Upon choosing or getting a card its image should pop up on image viewer utility.

## Dependencies

This project depends on the following Python libraries:

- `tabulate`
- `PIL`
- `requests`
- `io`
- `sys`
- `random` 

## Note

The `secret.py` file is ignored by git for security reasons. Make sure to create this file and add your API keys before running the bot.
