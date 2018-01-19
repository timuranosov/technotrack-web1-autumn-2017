from django import forms
from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = Topic
        fields = ['subject', 'message', 'categories']


class PostReplyForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]


class CategoriesListForm(forms.Form):

    order_by = forms.ChoiceField(choices=(
        ('title', 'title'),
        ('-title', '-title'),
        ('id', 'id')
    ), required=False)
    search = forms.CharField(required=False)

