import newspaper
from newspaper import Article

#The Basics of downloading the article to memory
link = "https://compositesweekly.com/discussing-fiber-patch-placement-technology-with-john-melilli-of-composite-automation/"
article = Article(link)
article.download()
article.parse()
article.nlp()

# To print out the full text
# print(article.text)
paragraph_list = (article.text.split('\n\n'))
print (paragraph_list[0])
print ("\n")
print (paragraph_list[1])
print (paragraph_list[2])
    




# To print out a summary of the text
# This works, because newspaper3k has built in NLP tools
#print(article.summary)

# To print out the list of authors
#print("Read more: " + link)

# To print out the list of keywords
#print(article.keywords)

#Other functions to gather the other useful bits of meta data in an article
article.title # Gives the title
article.publish_date #Gives the date the article was published
article.top_image # Gives the link to the main image of the article
article.images # Provides a set of image links

#print (article.title)
#print (article.images)