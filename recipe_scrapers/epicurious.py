import re
from ._abstract import AbstractScraper
from ._utils import normalize_string


class Epicurious(AbstractScraper):

    @classmethod
    def host(self):
        return 'epicurious.com'

    def title(self):
        return self.soup.find(
            'h1',
            {'itemprop': 'name'}
        ).get_text()

    def total_time(self):
        return 0

    def ingredients(self):
        ingredients = self.soup.findAll(
            'li',
            {'itemprop': "ingredients"}
        )

        return [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients
        ]

    def instructions(self):
        instructions = self.soup.findAll(
            'li',
            {'class': 'preparation-step'}
        )

        return '\n'.join([
            normalize_string(instruction.get_text())
            for instruction in instructions
        ])
 
    def total_review(self):
        return self.soup.find(
                'span',
                {'itemprop': "reviewCount"}
                ).get_text()
        
    def review_score(self): 
        review = self.soup.find(
                        'div',
                        {'class', 'prepare-again-rating'}
                        ).get_text()
        review = re.findall('\d+',review)
        for i in review:
            return int(i)
    
