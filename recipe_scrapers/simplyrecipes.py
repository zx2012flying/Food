import re
from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string


class SimplyRecipes(AbstractScraper):

    @classmethod
    def host(self):
        return 'simplyrecipes.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def total_time(self):
        return sum([
            get_minutes(self.soup.find(
                'span',
                {'class': 'preptime'})
            ),

            get_minutes(self.soup.find(
                'span',
                {'class': 'cooktime'})
            )
        ])

    def ingredients(self):
        ingredients = self.soup.find(
            'div',
            {'class': 'recipe-ingredients'}
        ).findAll('li')

        return '\n'.join([
            normalize_string(ingredient.get_text())
            for ingredient in ingredients
        ])

    def instructions(self):
        instructions_html = self.soup.find(
            'div',
            {'itemprop': 'recipeInstructions'}
        ).findAll('p')

        return '\n'.join([
            normalize_string(instruction.get_text())
            for instruction in instructions_html
        ])
    
    def total_review(self):
        return self.soup.find(
                'span',
                {'class': "total-count ratings"}
                ).get_text()

    def review_score(self):
        review_score = self.soup.find('span', {'class': "rating-value"}).get('style')
        return re.findall("\d+",review_score)[0] 
