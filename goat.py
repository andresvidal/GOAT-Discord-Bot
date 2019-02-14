import discord
from discord.ext import commands
import requests
import json

token = 'YOUR TOKEN HERE'
client = commands.Bot(command_prefix = '.')

@client.command(pass_context=True)
async def goat(ctx, *args):
    keywords = ''
    for word in args:
        keywords += word + '%20'
    json_string = json.dumps({"params": f"distinct=true&facetFilters=()&facets=%5B%22size%22%5D&hitsPerPage=20&numericFilters=%5B%5D&page=0&query={keywords}"})
    byte_payload = bytes(json_string, 'utf-8')
    x = {"x-algolia-agent": "Algolia for vanilla JavaScript 3.25.1", "x-algolia-application-id": "2FWOTDVM2O", "x-algolia-api-key": "ac96de6fef0e02bb95d433d8d5c7038a"}
    with requests.Session() as s:
        r = s.post("https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query", params=x, verify=False, data=byte_payload, timeout=30)
    try:
        results = r.json()["hits"][0]
        priceurl = f"https://www.goat.com/api/v1/product_templates/{results['slug']}/show_v2"
        recenturl = f"https://www.goat.com/api/v1/product_templates/{results['slug']}/recent_purchases?count=6"
        bidurl = f"https://www.goat.com/api/v1/product_templates/{results['slug']}/highest_offers"
        with requests.Session() as s2:
            header = {
                'accept': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'accept-language': 'en-us',
                'accept-encoding': 'br,gzip,deflate'
            }
    except:
        await client.say('An error occurred. Please check keywords again.')

    r2 = s2.get(priceurl, headers=header)
    prices = r2.json()
    priceformat = ''
    r4 = s2.get(bidurl, headers=header)
    bids = r4.json()
    for ask in prices['availableSizesNewV2']:
        if ask[0] in bids.keys():
            priceformat += f"Size {ask[0]} | Ask: ${ask[1][:-2]} | Bid: ${bids[ask[0]][:-2]}\n"

    r3 = s2.get(recenturl, headers=header)
    recent = r3.json()
    recentformat = ''
    for size in recent:
        recentformat += f"${str(int(size['priceCents']))[:-2]} at {size['purchasedAt'].split('T')[0]} {size['purchasedAt'].split('T')[1].split('.')[0]} GMT\n"

    embed = discord.Embed(title='GOAT App Checker', color=0x13e79e)
    embed.set_thumbnail(url=prices['pictureUrl'])
    embed.set_footer(text='@kxvxnc#6989')
    embed.add_field(name=prices['name'], value=f"https://goat.com/sneakers/{results['slug']}", inline=False)
    try:
        embed.add_field(name='SKU | Release Date | Retail', value=f"{results['sku']} | {results['release_date'].split('T')[0]} | ${str(results['special_display_price_cents'])[:-2]}", inline=False)
    except:
        embed.add_field(name='SKU | Release Date | Retail', value=f"{results['sku']} | {results['release_date']} | ${str(results['special_display_price_cents'])[:-2]}", inline=False)
    embed.add_field(name='Prices:', value=priceformat, inline=False)
    embed.add_field(name='Recent Sales:', value=recentformat, inline=False)
    await client.say(embed=embed)

client.run(token)
