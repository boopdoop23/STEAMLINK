# Steam Link Bot

A Discord bot to link Steam accounts to Discord for VIP users and export GUIDs.

## Setup

1. Clone this repository to your local machine.
2. Create a `.env` file with the following content:
    ```env
    DISCORD_TOKEN=your_bot_token_here
    VIP_ROLE_ID=your_vip_role_id_here
    ADMIN_ROLE_ID=your_admin_role_id_here
    ```
3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Run the bot:
    ```
    python bot.py
    ```

## Commands

- `/sendembed`: Send an embed to the channel to link Steam account (Admin only).
- `/exportguids`: Export all linked Steam GUIDs (Admin only).
