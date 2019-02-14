# GOAT-Discord-Bot

Uses GOAT's algolia search API to search products then uses that information in their own API to return sneaker data.

It returns an embed with:
- Product name/link
- Thumbnail Picture
- SKU/PID
- Release Date (yyyy-mm-dd)
- Retail Price
- Size | Lowest Ask | Highest Bid
- 6 Recent Sales with yyyy-mm-dd and GMT (Sizes not included)

This uses discordpy so generate your own discord bot token and replace 'YOUR TOKEN HERE' in goat.py
Feel free to edit the command prefix too.

![image](https://user-images.githubusercontent.com/30479452/52813458-d08a4c80-3067-11e9-8aa2-993d37a4d322.png)
