from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from forums.views import ForumListView, TopicListView, PostListView, new_topic, reply_topic, PostUpdateView, \
    CategoryList, CategoryDetail, PostLikeView

urlpatterns = [
    url(r'^$', ForumListView.as_view(), name='home'),
    url(r'^forums/(?P<pk>\d+)/$', TopicListView.as_view(), name='forum_topics'),
    url(r'^forums/(?P<pk>\d+)/new/$', new_topic, name='new_topic'),
    url(r'^forums/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', PostListView.as_view(), name='topic_posts'),
    url(r'^forums/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', reply_topic, name='reply_topic'),
    url(r'^forums/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/like/$', login_required(PostLikeView.as_view()), name="onepostlike"),
    url(r'^forums/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        PostUpdateView.as_view(), name='edit_post'),
    url(r'^categories/$', CategoryList.as_view(), name='category_list'),
    url(r'^categories/(?P<pk>\d+)/$', CategoryDetail.as_view(), name='category_detail'),

]
