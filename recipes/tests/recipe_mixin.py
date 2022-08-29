from django.contrib.auth.models import User
from recipes.models import Recipe, Category


class RecipeMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(self, username='Tester', email='tester@test.com', password='Tester.123'):
        return User.objects.create_user(username=username, email=email, password=password)

    def make_recipe(
            self,
            title='The Best Meat Recipe',
            description='Nothing',
            slug='the-best-meat-recipe',
            preparation_time_unit='minutes',
            preparation_time=120,
            servings=5,
            servings_unit='portions',
            preparation_steps='test',
            category=None,
            author=None,
            is_published=False
        ):

        if category is None:
            category = self.make_category(name='django')
        if author is None:
            author = self.make_author(username='django_admin', email='django.admin@hotmail.com', password='dj.admin')

        return Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time_unit=preparation_time_unit,
            preparation_time=preparation_time,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            category=category,
            author=author,
            is_published=is_published
        )

    def make_recipe_default(self):
        return self.make_recipe(author=self.make_author(username='new_user_'), slug='new-user-', is_published=False)

    def make_recipes(self, amount=3) -> list:
        all_recipes = []

        for i in range(amount):
            all_recipes.append(
                self.make_recipe(
                    title=f'recipe{i}',
                    description='...',
                    slug=f'recipe-{i}',
                    preparation_time_unit='minutes',
                    preparation_time=30,
                    servings_unit='portions',
                    servings=5,
                    preparation_steps='...',
                    is_published=True,
                    category=self.make_category(
                        name=f'category{i}'
                    ),
                    author=self.make_author(
                        username=f'user{i}',
                        email=f'user{i}.mail.com',
                        password=f'Us3r.{i}'
                    )
                )
            )
        else:
            return all_recipes
