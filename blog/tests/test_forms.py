import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from blog.forms import ArticleForm


@pytest.mark.django_db
class TestArticleForm:

    def test_form_with_valid_image_is_valid(self):
        image = SimpleUploadedFile(
            name="test.jpg",
            content=(
                b"\xff\xd8\xff\xe0"
                b"\x00\x10JFIF"
                b"\x00\x01\x02"
                b"\x00\x00\x01\x00\x01"
                b"\x00\x00"
                b"\xff\xd9"
            ),
            content_type="image/jpeg",
        )

        form = ArticleForm(
            files={
                "image": image,
            }
        )

        assert form.is_valid()

    def test_form_without_image_is_invalid(self):
        form = ArticleForm(files={})

        assert not form.is_valid()
        assert "image" in form.errors

    @pytest.mark.parametrize(
        "filename",
        [
            "test.txt",
            "test.pdf",
            "test.exe",
            "test.py",
        ],
    )
    def test_invalid_file_extension(self, filename):
        file = SimpleUploadedFile(
            name=filename,
            content=b"test content",
            content_type="application/octet-stream",
        )

        form = ArticleForm(
            files={
                "image": file,
            }
        )

        assert not form.is_valid()
        assert "image" in form.errors

    def test_form_contains_only_image_field(self):
        form = ArticleForm()

        assert list(form.fields.keys()) == ["image"]