from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day)

    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # EDIT let only registred users to make comment
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # new_comment = comment_form.save(commit=False)
            # new_comment.post = post
            # new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request, 
        'blog/post/detail.html', 
        {
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        }
    )

def post_share(request, post_id):
    # EDIT let only registred users to share post 
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            # EDIT move email to global settings
            send_mail(subject, message, 'no-reply@myblog.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(
        request, 'blog/post/share.html',
        {   
            'post': post,
            'form': form,
            'sent': sent
        }
    )