# ----------------------------------------------------------------------------
# learn_today.py
#
# Reads from the user question from the command input and searches to google 
# 	depending on the user's system default localization.
# ----------------------------------------------------------------------------
# author: routarddev              
# ----------------------------------------------------------------------------

import locale
import webbrowser


# get current locale
locale = locale.getdefaultlocale()
# web domain by default
web_domain = 'cat'
language_code = "cat"

if locale!=None and locale[0]!= None:
	language_code = locale[0].split('_')[0]
	country_code = locale[0].split('_')[1]

if language_code == "en" and country_code=="GB":
	web_domain="co.uk"
elif language_code == "en" and country_code=="US":
	web_domain="com"

search_string = raw_input("What do you wanna know today? ")

words = search_string.split(' ')
query = '+'.join(words)

url = "http://www.google."+web_domain+"/search?site=&source=hp&q="+query

webbrowser.open(url)
