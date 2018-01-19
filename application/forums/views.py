from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import View, UpdateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django.utils import timezone

from .forms import CategoriesListForm

# Create your views here.
from .models import Forum, Topic, Post, Category, User, Like
from .forms import NewTopicForm, PostReplyForm


class ForumListView(ListView):
    model = Forum
    context_object_name = 'forums'
    template_name = 'home.html'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        kwargs['forum'] = self.forum
        return super(TopicListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.forum = get_object_or_404(Forum, pk=self.kwargs.get('pk'))
        queryset = self.forum.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super(PostListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, forum__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def new_topic(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum = forum
            topic.starter = user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('topic_posts', pk=pk, topic_pk=forum.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'forum': forum, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, pk=topic_pk)
    if request.method == 'POST':
        form = PostReplyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostReplyForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


class CategoryDetail(DetailView):

    template_name = 'category_detail.html'
    context_object_name = 'category'
    model = Category


class CategoryList(ListView):

    template_name = 'category_list.html'
    context_object_name = 'categories'
    model = Category

    def get_queryset(self):

        q = super(CategoryList, self).get_queryset()

        form = CategoriesListForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['order_by']:
                q = q.order_by(form.cleaned_data['order_by'])
            if form.cleaned_data['search']:
                q = q.filter(title=self.request.GET['search'])
        return q


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super(PostUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.forum.pk, topic_pk=post.topic.pk)


class PostLikeView(View):

    post_object = None

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.post_object = get_object_or_404(Post, id=pk)
        return super(PostLikeView, self).dispatch(request, *args, **kwargs)

    def post(self):
        like = self.post_object.likes.filter(author=self.request.user).first()
        if like is None:
            like = Like()
            like.author = self.request.user
            like.post = self.post_object
            like.save()
        else:
            like.delete()
        return HttpResponse(Like.objects.filter(post=self.post_object).count())
