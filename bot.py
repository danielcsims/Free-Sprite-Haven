import discord
import requests
import shlex
import json
from pprint import pprint

with open('config.json') as f:
    script_config = json.load(f)
print(script_config)
client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$canyouhearit?'):
		await message.channel.send('Hello, ShadowHaven user. I am connected to this host and to the resonance. You won\'t hear it on any other frequency.')

	if message.content.startswith('$Test_Edit'):
		S = requests.Session()

		URL = "https://www.shadowhaven.info/api.php"

		# Step 1: GET request to fetch login token
		PARAMS_0 = {
			"action": "query",
			"meta": "tokens",
			"type": "login",
			"format": "json"
		}

		R = S.get(url=URL, params=PARAMS_0)
		DATA = R.json()

		LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

		# Step 2: POST request to log in. Use of main account for login is not
		# supported. Obtain credentials via Special:BotPasswords
		# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
		PARAMS_1 = {
			"action": "login",
			"lgname": script_config['Wiki_Username'],
			"lgpassword": script_config['Wiki_Password'],
			"lgtoken": LOGIN_TOKEN,
			"format": "json"
		}

		R = S.post(URL, data=PARAMS_1)

		# Step 3: GET request to fetch CSRF token
		PARAMS_2 = {
			"action": "query",
			"meta": "tokens",
			"format": "json"
		}

		R = S.get(url=URL, params=PARAMS_2)
		DATA = R.json()

		CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

		# Step 4: POST request to edit a page
		PARAMS_3 = {
			"action": "edit",
			"title": "Sandbox",
			"token": CSRF_TOKEN,
			"format": "json",
			"appendtext": "Hello"
		}

		R = S.post(URL, data=PARAMS_3)
		DATA = R.json()

		print(DATA)

	if message.content.startswith('$New_Contact'):
		cmdln_args = message.content
		neg_aspects = []
		args = shlex.split(cmdln_args)
		contact_settings = {k: True if v.startswith('-') else v
		           for k,v in zip(args, args[1:]+["--"]) if k.startswith('-')}

		
		contact_valid = True
	

		if "-aspects" not in contact_settings:
			await message.channel.send('Invalid contact, flag -aspects not found.')
			contact_valid = False
		if "-name" not in contact_settings:
			await message.channel.send('Invalid contact, flag -name not found.')
			contact_valid = False
		if "-connection" not in contact_settings:
			await message.channel.send('Invalid contact, flag -connection not found.')
			contact_valid = False
		if contact_valid:
			raw_aspects = contact_settings["-aspects"]
			aspects = shlex.split(raw_aspects)
			contact_settings["-aspects"] = aspects
			pprint(contact_settings)
			if (len(aspects)+len(neg_aspects)) != int(contact_settings["-connection"]):
				await message.channel.send('Invalid contact, contact\'s aspects do not equal the connection plus negative aspects.')
				await message.channel.send('This could be a formating problem. I see the following aspect. ')
				for aspect in aspects:
					await message.channel.send('    -' + aspect)
				contact_value = False
		if contact_valid is True:
			S = requests.Session()

			URL = "https://www.shadowhaven.info/api.php"

			# Step 1: GET request to fetch login token
			PARAMS_0 = {
				"action": "query",
				"meta": "tokens",
				"type": "login",
				"format": "json"
			}

			R = S.get(url=URL, params=PARAMS_0)
			DATA = R.json()

			LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

			# Step 2: POST request to log in. Use of main account for login is not
			# supported. Obtain credentials via Special:BotPasswords
			# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
			PARAMS_1 = {
				"action": "login",
				"lgname": script_config['Wiki_Username'],
				"lgpassword": script_config['Wiki_Password'],
				"lgtoken": LOGIN_TOKEN,
				"format": "json"
			}

			R = S.post(URL, data=PARAMS_1)

			# Step 3: GET request to fetch CSRF token
			PARAMS_2 = {
				"action": "query",
				"meta": "tokens",
				"format": "json"
			}

			R = S.get(url=URL, params=PARAMS_2)
			DATA = R.json()

			CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

			aspects_string = ""
			aspects_description_string = ""
			negative_aspects_string = "None"
			for aspect in aspects:
				aspects_string = aspects_string + "[[hasAspect::{}]]<BR>\n".format(aspect)
			aspects_string = aspects_string[:-5]
			for aspect in aspects:
				aspects_description_string = aspects_description_string + "\'\'\'{}\'\'\' - Please describe how this aspect relates to this contact\n\n".format(aspect)
			aspects_description_string = aspects_description_string[:-1]

			# Step 4: POST request to edit a page
			PARAMS_3 = {
				"action": "edit",
				"title": contact_settings["-name"],
				"token": CSRF_TOKEN,
				"format": "json",
				"appendtext": "{{{{Infobox\n|title = [[has name::{name_string}]]\n|image= [[File:Default-welcomer.png|200px]]\n|header1= [[Profession::Undefined]]\n|header2=\n|header3=\n|header4=\n|label5 = Contact Owner\n|data5 = \n|label6 = Connection\n|data6 = [[Connection::{connection_string}]]\n|label8 = Aspects\n|data8 = {aspects_string}\n|label9 = Negative Aspects\n|data9 = {negative_aspects_string}\n|label20 = Public Contact?\n|data20= Yes\n|label7 = Archetype\n|data7 =  [[Archetype::{type_string}]]\n|label10 = Location\n|data10= [[Location::Undefined]]\n|label11 = Metatype\n|data11 = [[Metatype::Undefined]]\n|label12 = Gender\n|data12 = [[Gender::Undefined]]\n|label13 = Age\n|data13= Undefined\n|label14= Preferred Payment Method\n|data14 = Undefined\n|label15 =  Hobbies/Vice\n|data15 = Undefined\n|label16 = Personal Life\n|data16 = Undefined\n|label17 = Faction\n|data17 = [[Faction::{faction_string}]]\n}}}}\n\n==Overview==\n\nFill this out\n\n==Aspects Description==\n\n{aspect_description}\n\n==Network==\n\n===Characters with this Contact ===\n\n{{{{#ask:\n[[-Has subobject::{{{{PAGENAME}}}}]]\n| mainlabel=-\n| ?HasConnectionName = PC Name\n| ?HasLoyalty = Loyalty\n}}}}\n\n[[Category:Contacts]]\n[[Category:Public Contacts]]\n__SHOWFACTBOX__".format(name_string=contact_settings["-name"],connection_string=contact_settings["-connection"],type_string=contact_settings["-type"],faction_string="Undefined",aspects_string=aspects_string,negative_aspects_string=negative_aspects_string,aspect_description=aspects_description_string)
			}




			R = S.post(URL, data=PARAMS_3)
			DATA = R.json()

			print(DATA)
			await message.channel.send('Contact Made, see https://www.shadowhaven.info/{name_string}'.format(name_string=contact_settings["-name"]))


client.run(script_config['Discord_API_Key'])