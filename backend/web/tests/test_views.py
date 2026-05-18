from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from api.models import User, Article, Category, Comment, Program, Product, Favorite, Cart, CartItem, Exercise

class WebTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user.is_onboarded = True
        self.user.save()
        self.category = Category.objects.create(name='Test Category', slug='test-cat')
        self.article = Article.objects.create(
            title='Test Article', 
            content='Test Content', 
            author=self.user, 
            category=self.category,
            is_published=True
        )

    def test_planner_view_requires_login(self):
        """
        Verify that the planner page redirects to login if not authenticated.
        """
        response = self.client.get(reverse('planner'))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    def test_planner_view_authenticated(self):
        """
        Verify that the planner page loads for an authenticated user.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('planner'))
        self.assertEqual(response.status_code, 200)
        # Language-agnostic: checks for the translated "Strategy" heading
        self.assertContains(response, _("Stratégie"))

    def test_blog_comment_submission(self):
        """
        Verify that an authenticated user can post a comment.
        """
        self.client.force_login(self.user)
        url = reverse('article_detail', args=[self.article.slug])
        data = {'content': 'This is a test comment.'}
        response = self.client.post(url, data)
        
        # Should redirect back to article page
        self.assertEqual(response.status_code, 302)
        
        # Verify comment was created
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, 'This is a test comment.')

    def test_article_like(self):
        """
        Verify that a user can like an article.
        """
        self.client.force_login(self.user)
        url = reverse('like_article', args=[self.article.slug])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.article.likes.filter(id=self.user.id).exists())

    def test_edit_profile(self):
        """
        Verify that a user can update their profile.
        """
        self.client.force_login(self.user)
        url = reverse('edit_profile')
        data = {
            'email': 'newemail@test.com',
            'bio': 'New Bio',
            'avatar': 'http://image.url'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Redirect to profile
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@test.com')
        self.assertEqual(self.user.bio, 'New Bio')

    def test_change_password(self):
        """
        Verify that a user can change their password.
        """
        self.client.force_login(self.user)
        url = reverse('change_password')
        data = {
            'old_password': 'password',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Redirect to profile
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_blog_search_and_filter(self):
        """
        Verify that blog search and category filtering work.
        """
        # Create another article in a different category
        cat2 = Category.objects.create(name='Nutrition', slug='nutrition')
        Article.objects.create(
            title='Nutrition Basics',
            content='Eat healthy.',
            author=self.user,
            category=cat2,
            is_published=True
        )

        # 1. Test Search
        response = self.client.get(reverse('blog_list') + '?q=Nutrition')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nutrition Basics')
        self.assertNotContains(response, 'Test Article') # Should be filtered out

        response = self.client.get(reverse('blog_list') + '?category=nutrition')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nutrition Basics')
        self.assertNotContains(response, 'Test Article') # Should be filtered out

    def test_delete_comment(self):
        """
        Verify that a user can delete their own comment.
        """
        self.client.force_login(self.user)
        
        # Create a comment
        comment = Comment.objects.create(
            article=self.article,
            author=self.user,
            content="To be deleted"
        )
        
        # Delete it
        url = reverse('delete_comment', args=[comment.id])
        response = self.client.post(url)
        
        # Check redirection
        self.assertEqual(response.status_code, 302)
        
        # Check it's gone
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())
        
    def test_delete_other_user_comment(self):
        """
        Verify that a user cannot delete another user's comment.
        """
        other_user = User.objects.create_user(username='other', password='password')
        comment = Comment.objects.create(
            article=self.article,
            author=other_user,
            content="Other user comment"
        )
        
        self.client.force_login(self.user)
        url = reverse('delete_comment', args=[comment.id])
        response = self.client.post(url)
        
        # Should redirect but NOT delete
        self.assertTrue(Comment.objects.filter(id=comment.id).exists())

    def test_dashboard_view(self):
        """
        Verify that the dashboard requires login and loads correctly with context data.
        """
        url = reverse('dashboard')
        
        # 1. Unauthenticated -> Redirect
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        # 2. Authenticated -> 200 OK
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/dashboard.html')
        self.assertIn('avg_sleep', response.context)
        self.assertIn('today_events', response.context)

    def test_program_list_view(self):
        """
        Verify that the program list page loads correctly.
        """
        response = self.client.get(reverse('program_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/programs_list.html')

    def test_program_detail_view(self):
        """
        Verify that the program detail page loads correctly.
        """
        # Create a test program
        program = Program.objects.create(
            name='Test Program',
            slug='test-program',
            goal='weight_loss',
            level='beginner',
            duration='4_weeks',
            description_short='Test description',
            description_long='Test long description',
            total_sessions=12,
            duration_weeks=4,
            nutrition_tips='Test tips',
            equipment_needed='None',
            image='https://example.com/image.jpg'
        )
        
        response = self.client.get(reverse('program_detail', args=[program.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/program_detail.html')
        self.assertContains(response, 'Test Program')

    def test_shop_list_view(self):
        """
        Verify that the shop list page loads correctly.
        """
        response = self.client.get(reverse('shop_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/shop_list.html')

    def test_shop_detail_view(self):
        """
        Verify that the shop detail page loads correctly.
        """
        # Create a test product
        product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category='strength',
            description_short='Test description',
            description_long='Test long description',
            price=99.99,
            rating=4.5,
            stock=10
        )
        
        response = self.client.get(reverse('shop_detail', args=[product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/shop_detail.html')
        self.assertContains(response, 'Test Product')

    def test_cart_view_requires_login(self):
        """
        Verify that the cart page requires authentication.
        """
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 302)

    def test_cart_view_authenticated(self):
        """
        Verify that the cart page loads for authenticated users.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/cart.html')

    def test_favorites_view_requires_login(self):
        """
        Verify that the favorites page requires authentication.
        """
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 302)

    def test_favorites_view_authenticated(self):
        """
        Verify that the favorites page loads for authenticated users.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/favorites.html')

    def test_cart_item_creation(self):
        """
        Verify that cart items can be created via the cart view logic.
        """
        product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category='strength',
            description_short='Test',
            description_long='Test long',
            price=99.99,
            rating=4.5,
            stock=10
        )
        
        self.client.force_login(self.user)
        # Create cart and add item directly (simulating view logic)
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        
        # Verify cart item was created
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 1)

    def test_cart_item_deletion(self):
        """
        Verify that cart items can be deleted.
        """
        product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category='strength',
            description_short='Test',
            description_long='Test long',
            price=99.99,
            rating=4.5,
            stock=10
        )
        
        self.client.force_login(self.user)
        # Add item to cart
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=product, quantity=1)
        
        # Delete item
        item.delete()
        
        # Verify item was removed
        self.assertEqual(cart.items.count(), 0)

    def test_favorite_creation(self):
        """
        Verify that favorites can be created.
        """
        exercise = Exercise.objects.create(
            name='Test Exercise',
            slug='test-exercise',
            muscle_group='chest',
            difficulty='beginner',
            description='Test description'
        )
        
        self.client.force_login(self.user)
        # Create favorite directly (simulating view logic)
        Favorite.objects.create(user=self.user, exercise=exercise, content_type='exercise')
        
        # Verify favorite was created
        self.assertTrue(Favorite.objects.filter(user=self.user, exercise=exercise).exists())

    def test_favorite_deletion(self):
        """
        Verify that favorites can be deleted.
        """
        exercise = Exercise.objects.create(
            name='Test Exercise',
            slug='test-exercise',
            muscle_group='chest',
            difficulty='beginner',
            description='Test description'
        )
        
        self.client.force_login(self.user)
        # Create favorite
        favorite = Favorite.objects.create(user=self.user, exercise=exercise, content_type='exercise')
        
        # Delete favorite
        favorite.delete()
        
        # Verify favorite was removed
        self.assertFalse(Favorite.objects.filter(user=self.user, exercise=exercise).exists())

    def test_exercise_detail_view(self):
        """
        Verify that the exercise detail page loads correctly.
        """
        exercise = Exercise.objects.create(
            name='Test Exercise',
            slug='test-exercise',
            muscle_group='chest',
            difficulty='beginner',
            description='Test description'
        )
        
        response = self.client.get(reverse('exercise_detail', args=[exercise.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/exercise_detail.html')
        self.assertContains(response, 'Test Exercise')

