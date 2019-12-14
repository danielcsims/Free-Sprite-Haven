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
	if message.content.startswith('$make_wiki_account'):
		if str(message.content).split()[1] in ("¬","`","!","\"","£","$","^","&","*","(",")","_","+","-","=","~","?","/",".",",",";",":","\'","@"):
			await message.channel.send("Invalid character in input")
		else:
			session = requests.Session()
			api_url = 'http://shadowhaven.info/api.php'
			# get login token
			r1 = session.get(api_url, params={
				'format': 'json',
				'action': 'query',
				'meta': 'tokens',
				'type': 'login',
			})
			r1.raise_for_status()

			# log in
			r2 = session.post(api_url, data={
				'format': 'json',
				'action': 'login',
				"lgname": script_config['Wiki_Username'],
				"lgpassword": script_config['Wiki_Password'],
				'lgtoken': r1.json()['query']['tokens']['logintoken'],
			})
			if r2.json()['login']['result'] != 'Success':
				raise RuntimeError(r2.json()['login']['reason'])

			r1.raise_for_status()

			r3 = session.get(api_url, params={
				'format': 'json',
				'action': 'query',
				'meta': 'tokens',
				'type': 'createaccount',
			})
			print(r3.content)
			#baseurl = "http://shadowhaven.info/"
			#payload = {'action': 'query', 'format': 'json', 'meta': 'tokens', 'type': 'createaccount'}
			#r1 = requests.post(baseurl + 'api.php', data=payload)
			#createaccount_token = r2.json()['query']['tokens']['createaccounttoken']
			r4 = session.post(api_url, data={
				'action': 'createaccount', 
				'format': 'json', 
				'username': str(message.content).split()[1], 
				'password': 'temp_pass_please_change',
				'retype': 'temp_pass_please_change',
				'reason': 'Bot created account',
				'createreturnurl': "http://Shadowhaven.info",
				'createtoken': r3.json()['query']['tokens']['createaccounttoken']
			})
			#r3 = requests.post(baseurl + 'api.php', data=payload)
			print(r4.content)
			if r4.json()['createaccount']['status'] != 'PASS':
				await message.channel.send("Something went wrong, contact @wiki if you need help. The API returned the following: " + r4.json()['createaccount']['message'])
			else: 
				await message.channel.send("A wiki account with the username " + str(message.content).split()[1] + " was made with default password `temp_pass_please_change` , please log in here https://www.shadowhaven.info/index.php?title=Special:UserLogin&returnto=Main+Page Then change this password by going to https://www.shadowhaven.info/Special:Preferences ")

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
	# if message.content.startswith('$Add_Contact'):
	# 	cmdln_args = message.content
	# 	args = shlex.split(cmdln_args)
	# 	addition_settings = {k: True if v.startswith('-') else v
	# 			   for k,v in zip(args, args[1:]+["--"]) if k.startswith('-')}

		
	# 	addition_valid = True
	

	# 	if "-runner" not in addition_settings:
	# 		await message.channel.send('Invalid addition, flag -runner not found.')
	# 		addition_valid = False
	# 	if "-contact" not in addition_settings:
	# 		await message.channel.send('Invalid addition, flag -contact not found.')
	# 		addition_valid = False
	# 	if "-loyalty" not in addition_settings:
	# 		await message.channel.send('Invalid contact, flag -loyalty not found.')
	# 		addition_valid = False
	# 	if "-chips" not in addition_settings:
	# 		await message.channel.send('Invalid addition, flag -chips not found.')
	# 		addition_valid = False
	# 	if addition_valid:
	# 		S = requests.Session()

	# 		URL = "https://www.shadowhaven.info/api.php"

	# 		# Step 1: GET request to fetch login token
	# 		PARAMS_0 = {
	# 			"action": "query",
	# 			"meta": "tokens",
	# 			"type": "login",
	# 			"format": "json"
	# 		}

	# 		R = S.get(url=URL, params=PARAMS_0)
	# 		DATA = R.json()

	# 		LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

	# 		# Step 2: POST request to log in. Use of main account for login is not
	# 		# supported. Obtain credentials via Special:BotPasswords
	# 		# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
	# 		PARAMS_1 = {
	# 			"action": "login",
	# 			"lgname": script_config['Wiki_Username'],
	# 			"lgpassword": script_config['Wiki_Password'],
	# 			"lgtoken": LOGIN_TOKEN,
	# 			"format": "json"
	# 		}

	# 		R = S.post(URL, data=PARAMS_1)

	# 		# Step 3: GET request to fetch CSRF token
	# 		PARAMS_2 = {
	# 			"action": "query",
	# 			"meta": "tokens",
	# 			"format": "json"
	# 		}

	# 		R = S.get(url=URL, params=PARAMS_2)
	# 		DATA = R.json()

	# 		CSRF_TOKEN = DATA['query']['tokens']['csrftoken']
	# 		# Step 4: POST request to edit a page
	# 		PARAMS_3 = {
	# 			"action": "edit",
	# 			"title": addition_settings["-contact"],
	# 			"token": CSRF_TOKEN,
	# 			"format": "json",
	# 			"appendtext": "{{#subobject:\n|HasConnectionName={PC_Name_As_Appears_On_Wiki}\n|HasLoyalty={Loyalty_Int}\n|Chips={Chips_Int}\n}}".format(PC_Name_As_Appears_On_Wiki=addition_settings["-runner"],Loyalty_Int=addition_settings["-loyalty"],Chips_Int=addition_settings["-chips"])
	# 		}


	# 		R = S.post(URL, data=PARAMS_3)
	# 		DATA = R.json()
	# 		await message.channel.send('Your PC has been added to a contact page, see https://www.shadowhaven.info/{name_string}'.format(name_string=addition_settings["-contact"]))


	if message.content.startswith('$New_Contact'):
		cmdln_args = message.content
		neg_aspects = []
		args = shlex.split(cmdln_args)
		contact_settings = {k: True if v.startswith('-') else v
				   for k,v in zip(args, args[1:]+["--"]) if k.startswith('-')}

		
		contact_valid = True
	

		if "-type" not in contact_settings:
			await message.channel.send('Invalid contact, flag -type not found.')
			contact_valid = False
		if "-faction" not in contact_settings:
			await message.channel.send('Invalid contact, flag -faction not found.')
			contact_valid = False
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
			if contact_settings["-type"] == "Fixer" or \
			contact_settings["-type"] == "Gear" or \
			contact_settings["-type"] == "Service" or \
			contact_settings["-type"] == "Legwork" or \
			contact_settings["-type"] == "Networking" or \
			contact_settings["-type"] == "Generalist":
				pass
			else:
				contact_valid = False
				await message.channel.send("Invalid contact type {}, must be one of the following: Fixer, Gear, Service, Legwork, Networking, Generalist".format(contact_settings["-type"]))
		if contact_valid:
			raw_aspects = contact_settings["-aspects"]
			aspects = shlex.split(raw_aspects)
			contact_settings["-aspects"] = aspects
			pprint(contact_settings)
			if (len(aspects)+len(neg_aspects)) != (int(contact_settings["-connection"])+1):
				await message.channel.send('Invalid contact, contact\'s aspects do not equal the connection + 1 plus negative aspects.')
				await message.channel.send('This could be a formating problem. I see the following aspects. ')
				for aspect in aspects:
					await message.channel.send('	-' + aspect)
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
				aspects_string = aspects_string + "*[[hasAspect::{}]]<BR>\n".format(aspect)
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
				"appendtext": "{{{{Infobox\n|title = [[has name::{name_string}]]\n|image= [[File:Default-welcomer.png|200px]]\n|header1= [[Profession::Undefined]]\n|header2=\n|header3=\n|header4=\n|label5 = Contact Owner\n|data5 = \n|label6 = Connection\n|data6 = [[Connection::{connection_string}]]\n|label9 = Aspects\n|data9 = {aspects_string}\n|label10 = Negative Aspects\n|data10 = {negative_aspects_string}\n|label30 = Public Contact?\n|data30= Yes\n|label7 = Archetype\n|data7 =  [[Archetype::{type_string}]]\n|label8 = Faction\n|data8 = [[Faction::{faction_string}]]\n|label11 = Location\n|data11= [[Location::Undefined]]\n|label12 = Metatype\n|data12 = [[Metatype::Undefined]]\n|label13 = Gender\n|data13 = [[Gender::Undefined]]\n|label14 = Age\n|data14= Undefined\n|label15= Preferred Payment Method\n|data15 = Undefined\n|label20 =  Hobbies/Vice\n|data20 = Undefined\n|label17 = Personal Life\n|data17 = Undefined\n}}}}\n==Overview==\n\nFill this out\n\n==Aspects Description==\n\n{aspect_description}\n\n==Network==\n\n===Characters with this Contact ===\n\n{{{{#ask: [[Category:Player Characters]][[HasContact::{{{{PAGENAME}}}}]]\n|mainlabel=-\n|format=table\n|headers=plain\n|default=None\n|link=subject\n|?=Name\n|?Loyalty{{{{PAGENAME}}}}=Loyalty\n|?Chips{{{{PAGENAME}}}}=Chips\n|limit=300\n}}}}\n[[Category:Contacts]]\n[[Category:Public Contacts]]\n__SHOWFACTBOX__".format(name_string=contact_settings["-name"],connection_string=contact_settings["-connection"],type_string=contact_settings["-type"],faction_string=contact_settings["-faction"],aspects_string=aspects_string,negative_aspects_string=negative_aspects_string,aspect_description=aspects_description_string)
			}




			R = S.post(URL, data=PARAMS_3)
			DATA = R.json()

			print(DATA)
			await message.channel.send('Contact Made, see https://www.shadowhaven.info/{name_string}'.format(name_string=contact_settings["-name"]))


client.run(script_config['Discord_API_Key'])