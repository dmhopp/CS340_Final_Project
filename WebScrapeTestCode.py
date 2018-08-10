import os
import sys
from bs4 import BeautifulSoup
from lxml import etree, objectify
import requests
import csv

# specify URL

def get_page(page_link):
	page = requests.get(page_link)
	return page

# parse into 

def main():

	page_link = 'https://www.coastalatlas.net/index.php?co=any&option=com_jumi&view=application&fileid=12&Itemid=109'

	html = get_page(page_link).content

	page_content = BeautifulSoup(html, 'lxml')

	tables = page_content.findChildren('table')
	table = tables[0]
	top_row = table.select('th')
	headers = [th.get_text().replace('\n', ' ').strip() for th in top_row]
	headers.insert(1, 'URL')
	headers.insert(2, 'imgURL')
	#print(headers)
	facilities_headers_text = ['Bathrooms', 'Handicap Access', 'Running Water', 'Showers', 'Camp Sites', 'Stairs to Beach', 'Boat Ramps']
	activities_headers_text = ['Tidepooling', 'Surfing', 'Hiking', 'Bicycling', 'Horseback Riding', 'Road Vehicle Access', 'Whale Watching']

	with open('beach-access-data.csv', 'w') as file:
		writer = csv.writer(file)
		#writer.writerow(headers)

		rows = table.select('tr')
		hcount = 1
		num_access_points = 1
		for row in rows:
			values = []
			i = 1
			for cell in row.select('td'):
				link = cell.find('a')
				if(link):
					values.append(cell.find('a').contents[0])
					link_name = link.get('href')
					values.append(link_name)
					#links.append(link_name)

					#print(page_link+link_name)
					second_html = get_page(page_link+link_name).content
					second_page_content = BeautifulSoup(second_html, 'lxml')
					second_tables = second_page_content.select('table')
					#print(second_tables)

					image_table = second_tables[1]

					image = image_table.select('img')[0]
					image_link = image['src'].split('src=')[-1]
					values.append(image_link)

					second_table = second_tables[4]
					#print(second_table)
					second_headers = []
					second_values = []

					for second_row in second_table.select('tr'):
						td1 = second_row.select('td')[0].get_text().replace(':', ' ').strip()
						td2 = second_row.select('td')[1].get_text()
						if(hcount == 1):
							headers.append(td1)
						values.append(td2)

					facilities_table = second_tables[6]
					#facilities_images = []
					facilities_values = []

					for facilities_row in facilities_table.select('tr'):
						#td1 = figure out how to scrape images
						#facilities_images.append(img for img in facilities_row.select('img'))
						td2 = facilities_row.select('td')[2].get_text()
						if td2 == 'none':
							td2 = 'no'
						facilities_values.append(td2)
					values.extend(facilities_values)

					activities_table = second_tables[7]
					#activities_images = []
					activities_values = []

					for activities_row in activities_table.select('tr'):
						#td1 = figure out how to scrape images
						#activities_images.append(img for img in activities_row.select('img'))
						td2 = activities_row.select('td')[2].get_text()
						if td2 == 'none':
							td2 = 'no'
						activities_values.append(td2)
					values.extend(activities_values)

				else:
					i+=2
					values.insert(i, (cell.get_text().strip()))

				if(hcount == 1):
					#print(headers)
					headers.extend(facilities_headers_text)
					headers.extend(activities_headers_text)
					writer.writerow(headers)
					hcount = 0
			
			#second_page = dict(zip(headers, values))
			#facilities = dict(zip(facilities_headers_text, facilities_values))

			#all_data = {**second_page, **facilities}
			#print(all_data)
			#print(headers)
			writer.writerow(values)
			print('%d written to file' % (num_access_points))
			num_access_points += 1
			#print(dict(zip(headers, values)))

if __name__ == '__main__':
	main()




