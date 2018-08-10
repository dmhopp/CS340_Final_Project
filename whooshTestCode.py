import sys
import whoosh
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser

#figure out how to download images via scraping to local computer
#store path to images in whoosh
#URL as ID

def index():
	schema = Schema(name=TEXT(stored=True), \
		URL=ID(stored = True), \
		imgURL=TEXT(stored=True), \
		county=TEXT(stored=True), \
		type=TEXT(stored=True), \
		location=TEXT(stored=True), \
		accessType=TEXT(stored=True), \
		path=TEXT(stored=True), \
		managedBy=TEXT(stored=True), \
		parking=TEXT(stored=True), \
		fee=TEXT(stored=True), \
		bathroom=TEXT(stored=True), \
		handicap=TEXT(stored=True), \
		water=TEXT(stored=True), \
		shower=TEXT(stored=True), \
		camp=TEXT(stored=True), \
		stairs=TEXT(stored=True), \
		boat=TEXT(stored=True), \
		tidepool=TEXT(stored=True), \
		surf=TEXT(stored=True), \
		hike=TEXT(stored=True), \
		bike=TEXT(stored=True), \
		horse=TEXT(stored=True), \
		vehicleAccess=TEXT(stored=True), \
		whale=TEXT(stored=True))

	indexer = create_in("indexDir", schema)

	writer = indexer.writer()