# Bot Downloader
<hr>
This is a bot downloader for the [***Telegram Bot Framework***](https://core.telegram.org/bots/api).

## Installation

Create a new directory and clone the repository.
### Create and activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```
## Configuration
```bash
touch config/.env
echo "TOKEN=<your_token>" >> config/.env
```
### Configure the database
```bash
python manage.py migrate
```
## Run the bot
```bash
python manage.py run
```
## Test the bot
send a message to the bot with the command /start

Enjoy!