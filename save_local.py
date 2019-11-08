#This is a quick python script to grab a webpage and save it locally
#useful for quick testing of scraping scripts

# takes url as command line argument
# takes filename as command line argument (optional)
# saves file in directory the script is run

import requests, argparse

parser = argparse.ArgumentParser(description="Save webpage HTML locally.")
parser.add_argument('url', metavar="url", type=str, help="url you want saved")
parser.add_argument('-f', metavar="filename", type=str, required = False, default='page_content.html', help="filename")
args = parser.parse_args()

page = requests.get(args.url, headers={'content-type' : 'application/json'})

f = open(args.f, 'w')
f.write(page.text)
f.close()
