import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from blog.models import Author, Tags, Article, SubTitle
from developer.models import Developer

@pytest.fixture
def author(db):
    return Author.objects.create(
        first_name="Aarsh",
        last_name="Paghe",
        email="Aarsh@example.com",
        phone="09123456789",
    )


@pytest.fixture
def tag(db):
    return Tags.objects.create(
        title="Django",
        slug="django",
    )


@pytest.fixture
def article(db, author):
    return Article.objects.create(
        title="Django Testing",
        author=author,
        description="Learn how to test Django applications.",
        slug="django-testing",
        published=True,
    )


@pytest.fixture
def unpublished_article(db, author):
    return Article.objects.create(
        title="Secret Article",
        author=author,
        description="This article is not published.",
        slug="secret-article",
        published=False,
    )


@pytest.fixture
def superuser(db):
    User = get_user_model()

    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="password123",
    )


@pytest.fixture
def normal_user(db):
    User = get_user_model()

    return User.objects.create_user(
        username="normaluser",
        email="user@example.com",
        password="password123",
    )


@pytest.fixture
def image():
    return SimpleUploadedFile(
        name="test.jpg",
        content=b"fake image content",
        content_type="image/jpeg",
    )

@pytest.fixture
def developer(db):
    return Developer.objects.create(
        username="arashPQ",
    )


@pytest.mark.django_db
class TestBlogView:

    def test_blog_redirects_to_article_list(self, client):
        response = client.get(reverse("blog:blog"))

        assert response.status_code == 302
        assert response.url == reverse("blog:article_list")


@pytest.mark.django_db
class TestArticleListView:

    def test_article_list_returns_200(self, client, article):
        response = client.get(reverse("blog:article_list"))

        assert response.status_code == 200

    def test_article_list_contains_published_articles(
        self,
        client,
        article,
        unpublished_article,
    ):
        response = client.get(reverse("blog:article_list"))

        assert article in response.context["articles"]
        assert unpublished_article not in response.context["articles"]

    def test_article_list_pagination(self, client, author):
        for i in range(12):
            Article.objects.create(
                title=f"Article {i}",
                author=author,
                description=f"Description {i}",
                slug=f"article-{i}",
                published=True,
            )

        response = client.get(
            reverse("blog:article_list"),
            {"page": 1},
        )

        assert response.status_code == 200
        assert len(response.context["page_objects"]) == 5

    def test_article_list_page_two(self, client, author):
        for i in range(12):
            Article.objects.create(
                title=f"Article {i}",
                author=author,
                description=f"Description {i}",
                slug=f"article-{i}",
                published=True,
            )

        response = client.get(
            reverse("blog:article_list"),
            {"page": 2},
        )

        assert response.status_code == 200
        assert len(response.context["page_objects"]) == 5


@pytest.mark.django_db
class TestArticleDetailView:

    def test_article_detail_returns_200(self, client, article):
        response = client.get(
            reverse(
                "blog:article_detail",
                kwargs={"pk": article.pk},
            )
        )

        assert response.status_code == 200

    def test_article_detail_contains_article(
        self,
        client,
        article,
    ):
        response = client.get(
            reverse(
                "blog:article_detail",
                kwargs={"pk": article.pk},
            )
        )

        assert response.context["article"] == article

    def test_article_detail_contains_subtitles(
        self,
        client,
        article,
    ):
        subtitle = SubTitle.objects.create(
            article=article,
            title="Introduction",
            body="Introduction body",
        )

        response = client.get(
            reverse(
                "blog:article_detail",
                kwargs={"pk": article.pk},
            )
        )

        assert subtitle in response.context["subtitles"]


@pytest.mark.django_db
class TestSearchByTagView:

    def test_search_by_tag_returns_matching_articles(
        self,
        client,
        article,
        tag,
    ):
        article.tag.add(tag)

        response = client.get(
            reverse(
                "blog:search_by_tag",
                kwargs={"tt": "django"},
            )
        )

        assert response.status_code == 200
        assert article in response.context["articles"]

    def test_search_by_tag_finds_tag_with_dash(
        self,
        client,
        article,
        tag,
    ):
        article.tag.add(tag)

        response = client.get(
            reverse(
                "blog:search_by_tag",
                kwargs={"tt": "django"},
            )
        )

        assert response.status_code == 200
        assert article in response.context["articles"]

    def test_search_by_tag_excludes_unpublished_article(
        self,
        client,
        unpublished_article,
        tag,
    ):
        unpublished_article.tag.add(tag)

        response = client.get(
            reverse(
                "blog:search_by_tag",
                kwargs={"tt": "django"},
            )
        )

        assert response.status_code == 302
        assert response.url == reverse("blog:article_list")


@pytest.mark.django_db
class TestCreateArticleView:

    def test_normal_user_cannot_create_article(
        self,
        client,
        normal_user,
    ):
        client.force_login(normal_user)

        response = client.get(
            reverse("blog:create_article")
        )

        assert response.status_code == 302

    def test_anonymous_user_cannot_create_article(self, client):
        response = client.get(
            reverse("blog:create_article")
        )

        assert response.status_code == 302

    def test_superuser_can_access_create_article(
        self,
        client,
        superuser,
    ):
        client.force_login(superuser)

        response = client.get(
            reverse("blog:create_article")
        )

        assert response.status_code == 200
