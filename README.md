# Discord Account Generator Bot

A Discord bot for automated account generation and stock management.

## Features

- Account generation for various services
- Cooldown system (60 minutes between generations)
- VIP role with cooldown bypass
- Stock checking functionality
- Automatic DM delivery of generated accounts
- JSON-based cooldown tracking
- Beautiful embed messages
- Error handling and user feedback
- Channel restriction system

## Requirements

- Python 3.8 or higher
- discord.py library
- `config.json` configuration file

## Installation

1. Clone the repository
2. Install required libraries:
```bash
pip install discord.py
```

3. Create a `config.json` file with the following structure:
```json
{
    "bot_token": "your_bot_token",
    "gen_channel_id": "generation_channel_id",
    "no_cooldown_role_id": "vip_role_id"
}
```

4. Create `.txt` files for each service you want to support (e.g., `netflix.txt`, `spotify.txt`, etc.)
5. Add accounts/serials to each `.txt` file, one per line

## Usage

### Commands

- `!gen <service>` - Generates an account for the specified service
- `!stock` - Shows available stock for all services

### Examples

```
!gen netflix
!gen spotify
!stock
```

## File Structure

- `gen.py` - Main bot file
- `config.json` - Configuration file
- `cooldowns.json` - Cooldown tracking file
- `*.txt` - Account files for each service

## Security Features

- Channel restriction for commands
- Cooldown system to prevent abuse
- Private DM delivery of accounts
- VIP role system for cooldown bypass
- Error handling for missing permissions
- Input validation

## Technical Details

### Cooldown System
- 60-minute cooldown between generations
- Persistent storage using JSON
- VIP role bypass option
- Remaining time display

### Account Management
- Automatic removal of used accounts
- Stock tracking per service
- Empty stock detection
- Service availability checking

### Error Handling
- Missing argument detection
- Invalid service handling
- DM permission checking
- Channel permission verification

## Important Notes

- Ensure the bot has proper permissions on the server
- Users must have DMs enabled to receive generated accounts
- The system automatically removes used accounts from `.txt` files
- VIP role must be configured in `config.json`
- Generation channel must be specified in `config.json`

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
