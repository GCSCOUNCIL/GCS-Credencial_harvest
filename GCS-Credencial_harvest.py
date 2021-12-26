
print('''

░██████╗░░█████╗░░██████╗░█████╗░░█████╗░██╗░░░██╗███╗░░██╗░█████╗░██╗██╗░░░░░
██╔════╝░██╔══██╗██╔════╝██╔══██╗██╔══██╗██║░░░██║████╗░██║██╔══██╗██║██║░░░░░
██║░░██╗░██║░░╚═╝╚█████╗░██║░░╚═╝██║░░██║██║░░░██║██╔██╗██║██║░░╚═╝██║██║░░░░░
██║░░╚██╗██║░░██╗░╚═══██╗██║░░██╗██║░░██║██║░░░██║██║╚████║██║░░██╗██║██║░░░░░
╚██████╔╝╚█████╔╝██████╔╝╚█████╔╝╚█████╔╝╚██████╔╝██║░╚███║╚█████╔╝██║███████╗
░╚═════╝░░╚════╝░╚═════╝░░╚════╝░░╚════╝░░╚═════╝░╚═╝░░╚══╝░╚════╝░╚═╝╚══════╝
-----------------------------------------------------------------------------
Developed by: GCSCOUNCIL
Company: GCSCOUNCIL
'''
)


import os,argparse,requests,signal
from getpass import getpass
import mechanicalsoup as ms
from Core import ispwned
from Core.utils import *
from Core.color import *

def signal_handler(signal, frame):
	print(end+'\n')
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(prog='GCS-Credencial_harvest.py')
parser.add_argument("email", help="Email/username to check")
parser.add_argument("-p",action="store_true", help="Don't check for leaks or plain text passwords.")
parser.add_argument("-np",action="store_true", help="Don't check for plain text passwords.")
parser.add_argument("-q",action="store_true", help="Quiet mode (no banner).")
args    = parser.parse_args()
email   = args.email

def is_there_captcha(page_source):

	if any( w in page_source.lower() for w in ["recaptcha/api","grecaptcha"]):
		return True
	return False


def login( name ,dic ,email ,pwd ):
	url ,form,e_form ,p_form = dic["url"] ,dic["form"],dic["e_form"] ,dic["p_form"]
	browser = ms.StatefulBrowser()
	try:
		browser.open(url)
	except:
		error("[{:10s}] Couldn't even open the page! Do you have internet !?".format(name))
		return

	if is_there_captcha(browser.get_current_page().text):
		error("[{:10s}] Found captcha on page loading!".format(name))
		return

	try:
		browser.select_form(form)
		browser[e_form] = email
		browser[p_form] = pwd
		browser.submit_selected()
	except ms.utils.LinkNotFoundError:
		error("[{:10s}] Something wrong with the website maybe it's blocked!".format(name))
		return

	if is_there_captcha(browser.get_current_page().text):
		error("[{:10s}] Found captcha after submitting login page!".format(name))
		return

	try:
		browser.select_form(form)
		browser.close()
		error("[{:10s}] Login unsuccessful!".format(name))
	except ms.utils.LinkNotFoundError:
		browser.close()
		status("[{:10s}] Login successful!".format(name))


def custom_login( name ,dic ,email ,pwd ):
	url ,form1,form2,e_form ,p_form = dic["url"] ,dic["form1"],dic["form2"],dic["e_form"] ,dic["p_form"]
	browser = ms.StatefulBrowser()
	try:
		browser.open(url)
	except:
		error("[{:10s}] Couldn't even open the page! Do you have internet !?".format(name))
		return

	if is_there_captcha(browser.get_current_page().text):
		error("[{:10s}] Found captcha on page loading!".format(name))
		return

	try:
		browser.select_form(form1)
		browser[e_form] = email
	except ms.utils.LinkNotFoundError:
		error("[{:10s}] Something wrong in parsing, maybe it displayed captcha!".format(name))
		return

	try:
		browser.submit_selected()
		browser.select_form(form2)
		browser[p_form] = pwd
		browser.submit_selected()
	except ms.utils.LinkNotFoundError:
		browser.close()
		error("[{:10s}] Email not registered!".format(name))
		return

	if is_there_captcha(browser.get_current_page().text):
		error("[{:10s}] Found captcha after submitting login page!".format(name))
		return

	try:
		browser.select_form(form2)
		browser.close()
		error("[{:10s}] Login unsuccessful!".format(name))
	except:
		browser.close()
		status("[{:10s}] Login successful!".format(name))



def req_login( name ,dic ,email ,pwd ):
	url ,verify,e_form ,p_form = dic["url"] ,dic["verify"],dic["e_form"] ,dic["p_form"]
	data  = {e_form:email,p_form:pwd}
	req = requests.post(url,data=data).text
	if is_there_captcha(req):
		error("[{:10s}] Found captcha on page loading!".format(name))
		return

	if any( word in req for word in verify):
		error("[{:10s}] Login unsuccessful!".format(name))
		return
	status("[{:10s}] Login successful!".format(name))

def main():
	if not args.q:
		banner()
	if not args.p:
		status("Checking email in public leaks...")
		ispwned.parse_data(email,args.np)

	print(C+" │"+end)
	line =C+" └──=>Enter a password"+W+"─=> "
	if os.name=="nt":
		pwd   = getinput(line) 
	else:
		pwd   = getpass(line)

	print("")
	status("Testing email against {} website".format( Y+str(len(all_websites))+G ))
	for wd in list(websites.keys()):
		dic = websites[wd]
		login( wd ,dic ,email ,pwd )

	for wd in list(custom_websites.keys()):
		dic = custom_websites[wd]
		custom_login( wd ,dic ,email ,pwd )

	for wd in list(req_websites.keys()):
		dic = req_websites[wd]
		req_login( wd ,dic ,email ,pwd )

if __name__ == '__main__':
	main()
