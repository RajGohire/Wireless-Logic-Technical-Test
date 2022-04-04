from urllib import request
from bs4 import BeautifulSoup
import json
import pprint

# Return page soure
def get_html(url):
	req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	page = request.urlopen(req, timeout=10).read().decode('utf8', errors = "ignore")
	
	return BeautifulSoup(page, 'html.parser')

# Return price/year for given price in a package
def get_annual_price(price):
	# Calculate float number value in the price string
	amount = float(''.join((ch if ch in '0123456789' else ' ') for ch in price).strip().replace(' ','.'))
	
	if 'Month' in price:
		return amount*12
	
	return amount

# Return price for given package
def get_price(info):
	# Check if a discount is available
	if '</p>' in str(info):
		start_idx = str(info).find('"price-big">')
		price = str(info)[start_idx+len('"price-big">'):str(info).find('<p', start_idx)].replace('</span>', ' ').replace('<br/>', ' ').strip()
		start_idx = str(info).find('<p style="color: red">')
		discount = str(info)[start_idx+len('<p style="color: red">'):str(info).find('</p>', start_idx)].strip()
	else:
		price = info.text.strip()
		discount = 'N/A'
	
	return price,discount

def main():
	url = "https://wltest.dns-systems.net/"
	source = get_html(url)
	results_source = source.find_all('div', {'class': 'package'})
	product_options = {"packages": []}
	option_title = description = price = discount = ''
	
	# Iterate through each package found
	for package in results_source:
		for a, elem in enumerate(package):
			# Header Dark Bg Div
			if a == 1:
				option_title = elem.text.strip()
			
			# Package-features Div
			elif a == 3: 
				description = ''
				for b, _ in enumerate(elem):
					# Unordered List Elements
					if b==1:
						for c, info in enumerate(_):
							# 'package-name' and 'package-description' Divs
							if c in [1, 3]:
								description += f'{info.text.strip()} '
							
							# 'package-price' Div
							elif c==5:
								price, discount = get_price(info)
							
							# Skip unnecessary iterations to save computation
							elif c>5:
								break
					
					# Skip Choose Button Div to save computation
					elif b>1:
						break
				
				# Append to Dict
				product_options['packages'].append({'option title':option_title,
													'description':description,
													'price':price,
													'discount':discount})

	# Sort the Dict
	sorted_products = sorted(product_options['packages'], key=lambda x: (get_annual_price(x['price'])), reverse=True)
	
	# Convert Dict to JSON
	output = json.dumps(sorted_products, indent=4)
	
	# Print the JSON
	pprint.pprint(output)

if __name__ == '__main__':
	main()