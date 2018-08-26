import re
from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string


class TastyKitchen(AbstractScraper):

    @classmethod
    def host(self):
        return 'tastykitchen.com'

    def title(self):
        return self.soup.find(
            'h1',
            {'itemprop': 'name'}
        ).get_text()

    def total_time(self):
        return sum([
            get_minutes(self.soup.find(
                'time',
                {'itemprop': 'prepTime'})
            ),

            get_minutes(self.soup.find(
                'time',
                {'itemprop': 'cookTime'})
            )
        ])

    def ingredients(self):
        ingredients = self.soup.find(
            'ul',
            {'class': "ingredients"}
        ).findAll('li')

        return '\n'.join([
            normalize_string(ingredient.get_text())
            for ingredient in ingredients
        ])

    def instructions(self):
        instructions = self.soup.find(
            'span',
            {'itemprop': 'instructions'}
        ).findAll('p')

        return '\n'.join([
            normalize_string(direction.get_text())
            for direction in instructions
        ])

    def total_review(self):
        total_review = self.soup.find('a',{'href': "#reviews"}).get_text()
        return re.findall("\d+",total_review)[0]  

    def review_score(self):
        review_score = self.soup.find('a',{'href': "#comments"}).get_text()
        return re.findall("\d+",review_score)[0]     
