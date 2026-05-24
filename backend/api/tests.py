from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Article, Category, Comment, Tag

class AccountTests(APITestCase):
    def test_registration(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('api:register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

class ArticleTests(APITestCase):
    """Tests compliant with Django Final Project specification."""

    def setUp(self):
        # Specification: authenticated user (not necessarily admin) can create.
        self.user = User.objects.create_user(username='alice', email='alice@test.com', password='alicepass')
        self.other = User.objects.create_user(username='bob', email='bob@test.com', password='bobpass')
        self.category = Category.objects.create(name='Health')

    def test_create_article_authenticated(self):
        """An authenticated user (non-admin) can create an article."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:article-list')
        data = {'title': 'Test Article', 'content': 'Content here', 'category': self.category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.get().author, self.user)

    def test_create_article_anonymous_forbidden(self):
        """An anonymous user CANNOT create an article."""
        url = reverse('api:article-list')
        data = {'title': 'Should Fail', 'content': 'No auth'}
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_anonymous_can_list_articles(self):
        """Anonymous can read the list of articles."""
        Article.objects.create(title='Public Article', content='c', author=self.user, category=self.category)
        response = self.client.get(reverse('api:article-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_only_author_can_update(self):
        """Only the author can modify their own article."""
        article = Article.objects.create(title='Mine', content='c', author=self.user, category=self.category)
        self.client.force_authenticate(user=self.other)
        response = self.client.patch(
            reverse('api:article-detail', args=[article.id]),
            {'title': 'Hijacked'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_author_can_delete(self):
        """Only the author can delete their own article."""
        article = Article.objects.create(title='Mine', content='c', author=self.user, category=self.category)
        self.client.force_authenticate(user=self.other)
        response = self.client.delete(reverse('api:article-detail', args=[article.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Article.objects.filter(id=article.id).exists())

    def test_search_articles(self):
        """GET /api/articles/?search=<query> filters by title/content."""
        Article.objects.create(title='Django REST', content='cool', author=self.user, category=self.category)
        Article.objects.create(title='Other Topic', content='nope', author=self.user, category=self.category)
        response = self.client.get(reverse('api:article-list') + '?search=Django')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Django REST')

    def test_create_article_with_tags(self):
        """Article creation with tag list (automatically created)."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('api:article-list'),
            {
                'title': 'Tagged',
                'content': 'Content',
                'category': self.category.id,
                'tags': ['python', 'api'],
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        article = Article.objects.get(title='Tagged')
        self.assertEqual(set(article.tags.values_list('name', flat=True)), {'python', 'api'})
        self.assertEqual(Tag.objects.count(), 2)

    def test_filter_articles_by_tag(self):
        """GET /api/articles/?tags__name=python filters by tag."""
        a1 = Article.objects.create(title='A', content='c', author=self.user, category=self.category)
        a2 = Article.objects.create(title='B', content='c', author=self.user, category=self.category)
        tag = Tag.objects.create(name='python')
        a1.tags.add(tag)
        response = self.client.get(reverse('api:article-list') + '?tags__name=python')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], a1.id)


class CommentTests(APITestCase):
    """Tests for the nested route /api/articles/<id>/comments/."""

    def setUp(self):
        self.user = User.objects.create_user(username='alice', email='a@x.com', password='pw')
        self.cat = Category.objects.create(name='C')
        self.article = Article.objects.create(title='T', content='c', author=self.user, category=self.cat)

    def test_anonymous_cannot_post_comment(self):
        """An anonymous user cannot post a comment."""
        url = reverse('api:article-comments', args=[self.article.id])
        response = self.client.post(url, {'content': 'hi'}, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_authenticated_can_post_comment(self):
        """An authenticated user can post a comment via the nested route."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:article-comments', args=[self.article.id])
        response = self.client.post(url, {'content': 'great post'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_anonymous_can_list_comments(self):
        """Anonymous can read comments."""
        Comment.objects.create(article=self.article, author=self.user, content='c')
        url = reverse('api:article-comments', args=[self.article.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

from .services import generate_wellness_plan

class ServiceTests(APITestCase):
    def test_generate_wellness_plan_math(self):
        """
        Verify that the generated plan's calories and macros are mathematically consistent.
        """
        # Inputs
        age = 25
        gender = 'male'
        height = 180
        weight = 80
        goal = 'maintenance'
        activity_level = 'moderate'

        workout, nutrition, score = generate_wellness_plan(age, gender, height, weight, goal, activity_level)

        # 1. Verify Structure
        self.assertIn('calories', nutrition)
        self.assertIn('macros', nutrition)
        
        # 2. Verify Calorie/Macro consistency
        # Parse "160g" -> 160
        p_grams = int(nutrition['macros']['protein'][:-1])
        c_grams = int(nutrition['macros']['carbs'][:-1])
        f_grams = int(nutrition['macros']['fats'][:-1])
        
        total_cals_from_macros = (p_grams * 4) + (c_grams * 4) + (f_grams * 9)
        target_cals = nutrition['calories']
        
        # Allow small rounding difference (e.g. +/- 5 kcals)
        diff = abs(target_cals - total_cals_from_macros)
        self.assertTrue(diff <= 10, f"Calorie mismatch: Target {target_cals} vs Calc {total_cals_from_macros} (Diff: {diff})")
        
        # 3. Verify Protein Rule (2g per kg)
        expected_protein = weight * 2
        self.assertEqual(p_grams, expected_protein)

class WebViewsTests(APITestCase):
    def test_public_urls(self):
        """
        Test that public pages are accessible.
        """
        urls = [
            reverse('home'),
            reverse('login'),
            reverse('register'),
            reverse('blog_list'),
            reverse('legal'),
            reverse('password_reset'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed on {url}")

    def test_redirect_if_not_logged_in(self):
        """
        Test that protected pages redirect to login.
        """
        urls = [
            reverse('profile'),
            reverse('edit_profile'),
            reverse('change_password'),
            reverse('planner'),
            reverse('tools'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.assertIn('/login/', response.url)
