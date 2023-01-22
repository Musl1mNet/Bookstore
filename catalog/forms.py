from django import forms
from .models import Book, Category


def build_book_category_tree(choice=False):
    parents = {}
    for row in Category.objects.order_by("id").all():
        if row.parent_id not in parents:
            parents[row.parent_id] = []

        parents[row.parent_id].append(row)

    result = []

    def build_tree(parent_id=None, depth=0):
        if parent_id not in parents:
            return

        margin = ">> " * depth

        for row in parents[parent_id]:
            txt = f"{margin} {row.name}"
            if choice:
                result.append((row.id, txt))
            else:
                result.append({"value": row.id, "text": txt})
            build_tree(row.id, depth + 1)
    build_tree()

    return result


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].choices = build_book_category_tree(True)

    class Meta:
        model = Book
        fields = "__all__"


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    img = forms.ImageField()


class BooksForm(forms.Form):
    name = forms.CharField(max_length=50)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 30}))
    photo = forms.ImageField()
    price = forms.DecimalField()
