import argparse
from collections import Counter
import re

from scraper import scrape

def main():
	parser = argparse.ArgumentParser(description='Summarize a document from a file, or the command line if no file is provided.')
	parser.add_argument('location', metavar='location', type=str, nargs='?',
	                    help='location of the document file')
	parser.add_argument('--url', dest='url', action='store_true',
	                    default=False,
	                    help='pull an article from the web (default: from filesystem)')

	args = parser.parse_args()
	# print(args)

	title, text = "", ""
	
	if args.location:

		if args.url:
			title, text = scrape(args.location)

		else:
			with open(args.location, "r") as file:
				raw_text = file.read()
				title = raw_text.split('\n')[0]
				text = raw_text
				# [^(Mr)(Mrs)(Ms)(Dr)(M)(Prof)]

	else:

		title = input("Article Title:\n")
		text = input("Article Text:\n")

	# print("%s\n%s" % (title, text))

	def rank_sentence(sentence, bow):
		words = [special_chars.sub("", word) for word in re.split('\s+', sentence)]
		# print(words, sum([bow[word] for word in words]))
		return -sum([bow[word] for word in words])


	sentences = re.split('((?<=\.|\!|\?)\s|(?<=\.\")\s)', text)
	special_chars = re.compile('[^A-Za-z0-9]')
	bag_of_words = Counter([special_chars.sub("", word) for word in re.split('\s+', text)])
	# print(bag_of_words)

	ranked_sentences = sorted(sentences,
		key = lambda sentence: rank_sentence(sentence, bag_of_words))
	num_sentences = min(int(len(sentences) ** 0.5), len(sentences))
	print(num_sentences)
	top_sentences = ranked_sentences[:num_sentences]

	ordered_sentences = dict(zip(sentences, range(len(sentences))))

	top_sentences = sorted(top_sentences, key = lambda sentence: ordered_sentences[sentence])
	print('\n'.join(top_sentences))

if __name__ == "__main__":
    main()