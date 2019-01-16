import discord
from discord.ext import commands
import requests
import json

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
        url = 'https://goat.com/sneakers/' + results['slug']
        product = results['name']
        sku = results['sku']
        date = results['release_date'].split('T')[0]
        lowest_used = '$' + str(results['lowest_price_cents'])[:-2]
    except:
        await client.say('An error occurred. Please check keywords again.')

    embed = discord.Embed(title='GOAT Info Checker', color=0x13e79e)
    embed.set_thumbnail(url=results['original_picture_url'])
    embed.set_footer(text='@kxvxnc#6989')
    embed.add_field(name='Product Name:', value=f'[{product}]({url})', inline=True)
    embed.add_field(name='SKU/PID:', value=sku, inline=True)
    embed.add_field(name='Retail Price:', value='$' + str(results['special_display_price_cents'])[:-2], inline=True)
    embed.add_field(name='Colorway:', value=results['details'], inline=True)
    embed.add_field(name='Release Date:', value=date, inline=True)
    embed.add_field(name='Lowest Used Price:', value=lowest_used, inline=True)
    await client.say(embed=embed)
