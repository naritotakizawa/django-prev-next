from django.views import generic
from .forms import SearchForm
from .models import Post


class PostList(generic.ListView):
    model = Post
    ordering = '-created_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context

    def get_queryset(self):
        # ここで表示した記事の一覧を詳細ビューで再現できるように
        # セッション post_list_typeに、検索か通常か、検索ならキーワードも保存しておく
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET or None)
        if form.is_valid():
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                queryset = queryset.filter(title__icontains=key_word)
                self.request.session['post_list_type'] = 'search'
                self.request.session['word'] = key_word
        else:
            self.request.session['post_list_type'] = 'normal'
        return queryset


class PostDetail(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        post_list_type = self.request.session.get('post_list_type', 'normal')
        # 記事一覧が通常の一覧だった
        if post_list_type == 'normal':
            post_list_queryset = Post.objects.all()

        # 記事一覧は、検索結果の一覧だった
        elif post_list_type == 'search':
            post_list_queryset = Post.objects.filter(title__icontains=self.request.session['word'])

        # 上で作ったQuerysetをもとに、今の記事の前、次を取得する
        prev = post_list_queryset.filter(created_at__lt=post.created_at).order_by('created_at').last()
        next = post_list_queryset.filter(created_at__gt=post.created_at).order_by('created_at').first()
        context['prev'] = prev
        context['next'] = next
        return context
