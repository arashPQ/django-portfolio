import pytest

from blog.models import Author, Tags, Article, SubTitle


@pytest.mark.django_db
class TestAuthor:

    def test_author_str(self):
        author = Author.objects.create(
            first_name="Arash",
            last_name="Paghe",
            email="Aarsh@example.com",
            phone="09123456789",
        )

        assert str(author) == "Arash Paghe"

    def test_author_name_property(self):
        author = Author.objects.create(
            first_name="Aarsh",
            last_name="Paghe",
            email="Aarsh@example.com",
            phone="09123456789",
        )

        assert author.name == "Arash Paghe"


@pytest.mark.django_db
class TestTags:

    def test_tag_str(self):
        tag = Tags.objects.create(
            title="Django",
            slug="django",
        )

        assert str(tag) == "Django"

    def test_tag_slug_is_generated_when_empty(self):
        tag = Tags(
            title="Python Programming",
            slug="",
        )

        tag.save()

        assert tag.slug == "python-programming"

    def test_tag_slug_is_unique(self):
        Tags.objects.create(
            title="Django",
            slug="django",
        )

        with pytest.raises(Exception):
            Tags.objects.create(
                title="Another Django",
                slug="django",
            )


@pytest.mark.django_db
class TestArticle:

    def test_article_str(self):
        author = Author.objects.create(
            first_name="Aarsh",
            last_name="Paghe",
            email="Aarsh@example.com",
            phone="09123456789",
        )

        article = Article.objects.create(
            title="My First Article",
            author=author,
            description="This is a test article",
            slug="my-first-article",
        )

        assert str(article) == "My First Article"

    def test_article_default_published_is_false(self):
        author = Author.objects.create(
            first_name="Aarsh",
            last_name="Paghe",
            email="Aarsh@example.com",
            phone="09123456789",
        )

        article = Article.objects.create(
            title="Test Article",
            author=author,
            description="Test description",
            slug="test-article",
        )

        assert article.published is False

    def test_article_can_have_tags(self):
        author = Author.objects.create(
            first_name="Aarsh",
            last_name="Paghe",
            email="Aarsh@example.com",
            phone="09123456789",
        )

        tag = Tags.objects.create(
            title="Django",
            slug="django",
        )

        article = Article.objects.create(
            title="Django Article",
            author=author,
            description="Django description",
            slug="django-article",
        )

        article.tag.add(tag)

        assert article.tag.count() == 1
        assert article.tag.first() == tag


@pytest.mark.django_db
class TestSubTitle:

    def test_subtitle_str(self):
        author = Author.objects.create(
            first_name="Aarsh",
            last_name="Paghe",
            email="Aarsh@example.com",
            phone="09123456789",
        )

        article = Article.objects.create(
            title="Django Article",
            author=author,
            description="Description",
            slug="django-article",
        )

        subtitle = SubTitle.objects.create(
            article=article,
            title="Introduction",
            body="This is the introduction.",
        )

        assert str(subtitle) == "Introduction from Django Article"
