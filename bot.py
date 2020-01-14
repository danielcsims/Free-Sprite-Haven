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
			contact_settings["-type"] == "Generalist" or \
			contact_settings["-type"] == "Custom(K,A,G,N)" or \
			contact_settings["-type"] == "Custom(K,A,N,G)" or \
			contact_settings["-type"] == "Custom(K,G,A,N)" or \
			contact_settings["-type"] == "Custom(K,G,N,A)" or \
			contact_settings["-type"] == "Custom(K,N,A,G)" or \
			contact_settings["-type"] == "Custom(K,N,G,A)" or \
			contact_settings["-type"] == "Custom(A,K,G,N)" or \
			contact_settings["-type"] == "Custom(A,K,N,G)" or \
			contact_settings["-type"] == "Custom(A,G,K,N)" or \
			contact_settings["-type"] == "Custom(A,G,N,K)" or \
			contact_settings["-type"] == "Custom(A,N,K,G)" or \
			contact_settings["-type"] == "Custom(A,N,G,K)" or \
			contact_settings["-type"] == "Custom(G,K,A,N)" or \
			contact_settings["-type"] == "Custom(G,K,N,A)" or \
			contact_settings["-type"] == "Custom(G,A,K,N)" or \
			contact_settings["-type"] == "Custom(G,A,N,K)" or \
			contact_settings["-type"] == "Custom(G,N,K,A)" or \
			contact_settings["-type"] == "Custom(G,N,A,K)" or \
			contact_settings["-type"] == "Custom(N,K,A,G)" or \
			contact_settings["-type"] == "Custom(N,K,G,A)" or \
			contact_settings["-type"] == "Custom(N,A,K,G)" or \
			contact_settings["-type"] == "Custom(N,A,G,K)" or \
			contact_settings["-type"] == "Custom(N,G,K,A)" or \
			contact_settings["-type"] == "Custom(N,G,A,K)" or \
			contact_settings["-type"] == "Fixer(K,A,G,N)" or \
			contact_settings["-type"] == "Fixer(K,A,N,G)" or \
			contact_settings["-type"] == "Fixer(K,G,A,N)" or \
			contact_settings["-type"] == "Fixer(K,G,N,A)" or \
			contact_settings["-type"] == "Fixer(K,N,A,G)" or \
			contact_settings["-type"] == "Fixer(K,N,G,A)" or \
			contact_settings["-type"] == "Fixer(A,K,G,N)" or \
			contact_settings["-type"] == "Fixer(A,K,N,G)" or \
			contact_settings["-type"] == "Fixer(A,G,K,N)" or \
			contact_settings["-type"] == "Fixer(A,G,N,K)" or \
			contact_settings["-type"] == "Fixer(A,N,K,G)" or \
			contact_settings["-type"] == "Fixer(A,N,G,K)" or \
			contact_settings["-type"] == "Fixer(G,K,A,N)" or \
			contact_settings["-type"] == "Fixer(G,K,N,A)" or \
			contact_settings["-type"] == "Fixer(G,A,K,N)" or \
			contact_settings["-type"] == "Fixer(G,A,N,K)" or \
			contact_settings["-type"] == "Fixer(G,N,K,A)" or \
			contact_settings["-type"] == "Fixer(G,N,A,K)" or \
			contact_settings["-type"] == "Fixer(N,K,A,G)" or \
			contact_settings["-type"] == "Fixer(N,K,G,A)" or \
			contact_settings["-type"] == "Fixer(N,A,K,G)" or \
			contact_settings["-type"] == "Fixer(N,A,G,K)" or \
			contact_settings["-type"] == "Fixer(N,G,K,A)" or \
			contact_settings["-type"] == "Fixer(N,G,A,K)":
				pass
			else:
				contact_valid = False
				await message.channel.send("Invalid contact type {}, must be one of the following: Fixer, Gear, Service, Legwork, Networking, Generalist or a valid custom or custom fixer contact".format(contact_settings["-type"]))
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
				aspect.replace(',', 'Comma removed due to mediawiki constraints')
				aspects_description_string =aspects_description_string + "{{PositiveAspect|\n" + \
						"|Aspect={}\n".format(aspect) +\
						"|Description=This is an example description for the {} positive aspect. You can write the fluff in here. Duplicate this section as many times as needed for your contact.\n".format(aspect) +\
						"|}}\n"

			# Step 4: POST request to edit a page
			PARAMS_3 = {
				"action": "edit",
				"title": contact_settings["-name"],
				"token": CSRF_TOKEN,
				"format": "json",
				"appendtext": "{{Infobox\n" + \
							"|title = {{PAGENAME}}  <!-- You don't need to change the title. This auto-generates for you. -->\n" + \
							"|image= [[File:Placeholder2.jpg|200px]] <!-- You can upload your own image for your contact. Replace Placeholder2.jpg with the name of the image you'd like to use. After you create the page, click on the red link to upload the image. -->\n" +\
							"|header1= [[Profession::Undefined]] <!-- This is the \"official job\" of the contact. It is a good way to describe their skills and what sets them apart from all of the other contacts of the same Archetype. -->\n" +\
							"|header2= (Shortblurb) <!-- You can write a short description here. Also on the next couple header lines if you want. -->\n" +\
							"|header3= \n" +\
							"|header4= \n" +\
							"|label5 = Contact Owner <!-- Leave this alone --> \n" +\
							"|data5 = [https://www.reddit.com/user/Your_Handle_Here Your_Handle_Here] <!-- Here you can put your reddit name. Be sure to replace BOTH instances of Your_Handle_Here with your reddit name. -->\n" +\
							"|label6 = Connection <!-- Leave this alone -->\n" +\
							"|data6 = [[Connection::{connection_string}]] <!-- This is the connection for your contact. Remember that at chargen, your connection+loyalty can not exceed 7, raising contacts above connection 6 post-gen requires thematics approval. -->\n".format(connection_string=contact_settings["-connection"]) +\
							"|label8 = Public Contact? <!-- Leave this alone -->\n" +\
							"|data8= Yes <!-- If you want the contact to be public, where anyone can gain the contact, leave this alone. If you want the contact to be private where only your character has the contact, change this to \"no\" and remove Category:Public Contacts from the bottom of the page. -->\n" +\
							"|label9 = [[Contact_Rules#Contact_Archetype|Archetype]] <!-- Leave this alone -->\n" +\
							"|data9 =  [[Archetype::{type_string}]] <!-- This is where you define the Archetype. Default Archetypes are:  Fixer, Service, Gear, Legwork, Networking, Generalist. Custom Archetypes may be defined as denoted on the contact rules page. -->\n".format(type_string=contact_settings["-type"]) +\
							"|label10 = Location <!-- Leave this alone -->\n" +\
							"|data10= [[Location::XXX, XXX]] <!-- Where is your contact normally found? -->\n" +\
							"|label11 = Metatype <!-- Leave this alone -->\n" +\
							"|data11 = [[Metatype::Undefined]] <!-- Human, Elf, Ork, Naga, AI who inhabits an Animatronic Dancing Penguin Drone, ect. -->\n" +\
							"|label12 = Sex <!-- Leave this alone -->\n" +\
							"|data12 = [[Gender::Undefined]] <!-- You can set the gender here. But please don't be a wiseass and put \"yes please\" under Sex. We've done that joke already. -->\n" +\
							"|label13 = Age <!-- Leave this alone -->\n" +\
							"|data13= CONTACT AGE HERE <!-- How old is your contact? You can give them a specific age like 44, or a general age like \"mid-40s\" or \"middle-aged\" -->\n" +\
							"|label14= Preferred Payment Method <!-- Leave this alone -->\n" +\
							"|data14 = (Cash) <!-- How do they like to be compensated? -->\n" +\
							"|label15 =  Hobbies/Vice <!-- Leave this alone -->\n" +\
							"|data15 = Blackjack, and Hookers. Actually, forget the blackjack. <!-- What interests them? -->\n" +\
							"|label16 = Personal Life <!-- Leave this alone --> \n" +\
							"|data16 = Single/Divorced/None of your business <!-- This kinda explains itself. --> \n" +\
							"|label17 = Faction <!-- Leave this alone -->\n" +\
							"|data17 = [[Faction::{faction_string}]] <!-- If they belong to a faction or group, fill it in here by replacing XXX. Otherwise, delete this entire line. -->\n".format(faction_string=contact_settings["-faction"]) +\
							"|label19 = Aspects <!-- Leave this alone -->\n" +\
							"|data19 = {{GenerateAspectList}}  <!-- Leave this alone -->\n\n" +\
							"}}\n\n\n" +\


							"==Overview==\n" +\
							"This is where you would write a blurb about the contact.\n\n" +\

							"==Aspects Description==\n" +\
							"<!-- Do not remove the below text. It's super important for the Aspect table. -->\n" +\
							"{{AspectTable|\n" +\
							"<!-- Do not remove the above code. It's super important. You can add new aspects below using the PositiveAspect and NegativeAspect template you see below. To add additional aspects, simply copy/paste one of the blocks below and update it with the name of the aspect, and a short description.  -->\n\n\n" +\


						"<!-- Below is an example of a positive aspect. You may duplicate this as many times as necessary. For Negative Aspects, Replace {{PositiveAspect| With {{NegativeAspect|    -->\n" +\
						"{aspects_description_string}\n".format(aspects_description_string=aspects_description_string) +\
						"<!-- Above is an example of a positive aspect. You may duplicate this as many times as necessary. -->\n\n\n" +\



						"<!-- Do not remove the below text. It's super important for the Aspect table. All aspects should be listed above this line. -->\n" +\
						"}}\n" +\
						"<!-- Do not remove the above text. -->\n" +\

						"==Dicepools==\n" +\
						"{{ContactDicepools}}\n" +\
						"<!-- You do not need to mess with this. This template should automatically generate a table with dicepools based on the Archetype and the connection. If it comes up as a broken red link, don't panic and ask @wiki for help on the discord.-->\n\n" +

						"==Network==\n" +\
						"===Player Characters with this Contact===\n" +\
						"{{ContactPlayerConnections}}\n" +\
						"<!-- You do not need to mess with this. This template should automatically generate a table with everyone who has the contact on their wiki page. -->\n\n" +\

						"===NPC who know this contact===\n" +\
						"[[Category:Contacts]]\n" +\
						"[[Category:Public Contacts]]\n\n" +\

						"__SHOWFACTBOX__".format(name_string=contact_settings["-name"],connection_string=contact_settings["-connection"],type_string=contact_settings["-type"],faction_string=contact_settings["-faction"],aspects_description_string=aspects_description_string,negative_aspects_string=negative_aspects_string)
			}




			R = S.post(URL, data=PARAMS_3)
			DATA = R.json()

			print(DATA)
			await message.channel.send('Contact Made, see https://www.shadowhaven.info/{name_string}'.format(name_string=contact_settings["-name"]))
	if message.content.startswith('$make_wiki_account'):
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
			"format": "json",
			'type': 'createaccount',
		}
		R = S.get(url=URL, params=PARAMS_2)
		DATA = R.json()

		CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

client.run(script_config['Discord_API_Key'])