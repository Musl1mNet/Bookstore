import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    def clean(self):
        rating_stars = self.cleaned_data["rating_stars"]
        rating_count = self.cleaned_data["rating_count"]
        if rating_stars > 0 and rating_stars / rating_count > 5:
            raise ValidationError({
                "rating_stars": f"Ustun qiymati {rating_stars} dan/ga teng/kichik bo'lishi lozim!"
            })
        return self.cleaned_data

    def clean_publish_year(self):
        py = self.cleaned_data["publish_year"]
        now = datetime.datetime.now().year
        if py:
            if py > now:
                raise ValidationError(f"Siz kiritgan yil {now} dan katta bo'lmasligi lozim!")
        return py
    class Meta:
        model = Book
        fields = "__all__"

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=50, min_length=6, widget=forms.PasswordInput())
    confirm = forms.CharField(max_length=50, min_length=6, widget=forms.PasswordInput())

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            raise ValidationError({
                'confirm': "Password ustuni bilan bir xil emas!"
            })
        return self.cleaned_data
    class Meta:
         model = User
         fields = ['first_name', 'last_name', 'username', 'password', 'confirm']
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

# class UserForm(forms.Form):
#     first_name = forms.CharField(max_length=50)
#     last_name = forms.CharField(max_length=50)
#     email = forms.EmailField(widget=forms.EmailInput)
#     password = forms.CharField(widget=forms.PasswordInput)
#     img = forms.ImageField()
#
#
# class BooksForm(forms.Form):
#     name = forms.CharField(max_length=50)
#     content = forms.CharField(
#         widget=forms.Textarea(attrs={'rows': 10, 'cols': 30}))
#     photo = forms.ImageField()
#     price = forms.DecimalField()
