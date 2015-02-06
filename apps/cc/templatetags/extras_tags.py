# -*- coding:utf8 -*-

from django import template

import datetime

register = template.Library()

def page_recipe(pages, adjacent_pages=3):
	paginator = pages.paginator
	page_numbers = [n for n in range(pages.number-adjacent_pages, pages.number+adjacent_pages+1) if n > 0 and n <= paginator.num_pages]

	return page_numbers

register.filter('page_recipe', page_recipe)
