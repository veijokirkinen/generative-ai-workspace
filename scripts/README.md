# Scripts Directory

Tässä kansiossa on CLI-skriptit ja automaatiotyökalut.

## Tiedostot (tulevat):
- `append_chat_log.py` - Lisää viestejä chat-lokiin aikaleimoilla
- `clipboard_watcher.py` - Tarkkailee leikepöytää ja tallentaa muutoksia automaattisesti

## Käyttö:
```bash
# Esimerkkikäyttö append_chat_log.py:lle
python scripts/append_chat_log.py --file logs/chat.log --author "Veijo" --message "Uusi viesti"

# Clipboard watcher käynnistys:
python scripts/clipboard_watcher.py --output logs/clipboard.log
```