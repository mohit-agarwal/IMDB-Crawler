import urllib2

#Defining Global Variables
SEED_URL="http://www.imdb.com/chart/top"
HOST_URL="http://www.imdb.com"
cast_KnowledgeBase={}

# This function will return the HTML page for a given URL.
def getHTMLpage(url):
	c=urllib2.urlopen(url)
	contents=c.read()
	return contents

# This function will print the Knowledge Base of the Cast Members.
def print_KnowledgeBase():
	for dkey, dvalue in cast_KnowledgeBase.iteritems():
		print dkey, dvalue

# Function for evaluating the queries.
def query():
	print "Enter the name of a cast member : ",
	query_name=raw_input()
	if cast_KnowledgeBase.has_key(query_name):
		print cast_KnowledgeBase[query_name]
	else:
		print "Given name does not exist in the Knowledge Base."

# Function will parse the HTML page of a movie and return a list of all the Cast Members of that movie.
def parse_MoviePage(movieUrl):
	contents=getHTMLpage(movieUrl)
	split_contents=contents.split('<h2>Cast</h2>')[1].split('\n')
	html_elements_with_CastNames=filter(lambda x: x.find('class="itemprop" itemprop="name"') is not -1,split_contents)
	filtered_elements=filter(lambda x: x.find("/company/") is -1,html_elements_with_CastNames)
	cast_members=map(lambda x:x.split('itemprop="name"')[1][1:-7],filtered_elements)
	return cast_members

# Funtion will process the Movie Url and will add all the cast members of that movie to the Knowledge Base.
def getCast(movie_tuple):
	movieName=movie_tuple[0]
	movieUrl=HOST_URL+movie_tuple[1]
	Cast_Members=parse_MoviePage(movieUrl)
	for cast_member in Cast_Members:
		if cast_KnowledgeBase.has_key(cast_member):
			cast_KnowledgeBase[cast_member].append(movieName)
		else:
			cast_KnowledgeBase[cast_member]=[movieName]

# This function will parse the SEED_URL and return a list of top 250 movies.
def parse_SeedUrl():
	page_contents=getHTMLpage(SEED_URL)
	split_contents = page_contents.split('\n')
	html_elements_with_MovieNames= filter(lambda x: x.find("titleColumn") is not -1,split_contents)
	movie_tuples=map(lambda x : (x.split('"')[6][2:-17],x.split('"')[3]), html_elements_with_MovieNames)
	return movie_tuples

# Function process first N movies in the SEED_URL and builds the Knowledge Base.
def build_KnowledgeBase(N):
	print "Parsing the Seed Urls...."
	movie_tuples=parse_SeedUrl()
	for movie_id in range(N):
		getCast(movie_tuples[movie_id])

# Main function
def main():
	print "Enter N : ",
	N=int(raw_input())
	build_KnowledgeBase(N)
	
	print_KnowledgeBase()
	
	print "Enter number of queries : ",
	num_queries=int(raw_input())
	for i in range(num_queries):
		query()


if __name__ == '__main__':
	main()

