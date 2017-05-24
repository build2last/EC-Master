# coding:utf-8
# design data item
from __future__ import unicode_literals
from __future__ import division
		
class ReviewRating:
	"""
		rating value:评分
		best_rating:评分上限
		worst_rating:评分下限
	"""
	def __init__(self, rating_value, best_rating, worst_rating):
		self.rating_value = rating_value
		self.best_rating = best_rating
		self.worst_rating = worst_rating

	def normalize(self):
		return self.rating_value/(self.best_rating - self.worst_rating)


class Review:
	def __init__(self, review_id, item_id, review_body, author, date_published, review_rating, publisher, key_word):
		self.review_id = review_id
		self.item_id = item_id
		self.review_body = review_body
		self.author = author
		self.date_published = date_published
		self.review_rating = review_rating
		self.publisher = publisher
		self.key_word = key_word

	def tans_to_dict(self):
		item_dict = {"review_id":str(self.review_id), "item_id":str(self.item_id), "review_body":self.review_body,
					 "author":self.author, "date_published":self.date_published, 
					 "review_rating":str(self.review_rating), "publisher":self.publisher, "key_word":self.key_word
					}
		return item_dict