from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm,
)
from django.contrib import messages
import json
from .models import Vision, Reply, Share, User, Category, Tweet
from .views import VisionViewSet


class ShareInline (admin.TabularInline):
    model = Share
    extra = 1


class ReplyInline (admin.TabularInline):
    model = Reply
    extra = 3


class TweetAssignmentFilter(admin.SimpleListFilter):
    title = 'Assignment'
    parameter_name = 'assignment'

    def lookups(self, request, model_admin):
        return (
            ('visions', 'Visions'),
            ('replies', 'Replies'),
            ('null', 'Unassigned'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'visions':
            return queryset.filter(vision__isnull=False)
        if val == 'replies':
            return queryset.filter(reply__isnull=False)
        if val == 'null':
            return queryset.filter(vision__isnull=True, reply__isnull=True)


class TweetAdmin (admin.ModelAdmin):
    model = Tweet
    list_display = ('__unicode__', 'tweeter', 'text', 'assignment', 'is_a_reply')
    readonly_fields = ('tweeter', 'text', 'assignment')
    actions = ('make_visions', 'make_replies',)
    list_filter = (TweetAssignmentFilter,)
    search_fields = ('tweet_data',)
    raw_id_fields = ('in_reply_to',)

    def queryset(self, request):
        queryset = super(TweetAdmin, self).queryset(request)
        return queryset.select_related('vision', 'reply')

    def make_visions(self, request, tweet_qs):
        tweet_qs.make_visions()
        self.message_user(request, 'Successfully converted %s tweets to visions.' % (tweet_qs.count(),))
    make_visions.short_description = "Make visions from the selected tweets"

    def make_replies(self, request, tweet_qs):
        try:
            tweet_qs.make_replies()
            self.message_user(request, 'Successfully converted %s tweets to replies.' % (tweet_qs.count(),))
        except ValueError:

            # If we fail to make them all replies (which is fastest), go one
            # by one and count the failures.
            successes = 0
            failures = 0

            for tweet in tweet_qs.all():
                try:
                    tweet.make_reply()
                    successes += 1
                except ValueError:
                    failures += 1

            self.message_user(request, 'Successfully converted %s tweet(s) to replies. %s tweet(s) are not yet replies to visions. Assign tweets to be replies before proceeding.' % (successes, failures), level=messages.WARNING)
    make_replies.short_description = "Make replies from the selected tweets"

    def tweeter(self, tweet):
        user_data = tweet.tweet_data.get('user', {})
        return '%s (%s)' % (user_data.get('screen_name'), user_data.get('name'))

    def text(self, tweet):
        return tweet.tweet_data.get('text')

    def assignment(self, tweet):
        try:
            tweet.vision
            return ('<a href="%s">Vision %s</a>' % (reverse('admin:visionlouisville_vision_change', args=[tweet.vision.id]), tweet.vision.id))
        except Vision.DoesNotExist:
            pass

        try:
            tweet.reply
            return ('<a href="%s">Reply %s</a>' % (reverse('admin:visionlouisville_reply_change', args=[tweet.reply.id]), tweet.reply.id))
        except Reply.DoesNotExist:
            pass
    assignment.allow_tags = True  # Do not HTML-escape the value

    def is_a_reply(self, tweet):
        return tweet.in_reply_to_id is not None
    is_a_reply.boolean = True  # Display a "pretty" on/off icon


class VisionAdmin (admin.ModelAdmin):
    inlines = [ReplyInline, ShareInline]
    # date_hierarchy = 'created_at'
    filter_horizontal = ('supporters',)
    list_display = ('__unicode__', 'author', 'text', 'category', 'featured')
    list_editable = ('category', 'featured',)
    list_filter = ('category', 'created_at', 'updated_at')
    readonly_fields = ('tweet_text',)
    search_fields = ('text', 'category')

    def change_view(self, request, *args, **kwargs):
        # Save the request so that we can use it when
        # constructing the tweet text.
        self.request = request
        return super(VisionAdmin, self).change_view(request, *args, **kwargs)

    def tweet_text(self, vision):
        return VisionViewSet.get_app_tweet_text(self.request, vision)


class UserCreationForm (BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

    # NOTE: We must override clean_username because of this bug:
    #       https://code.djangoproject.com/ticket/19353
    # TODO: Get rid of this whenever that patch gets merged in.
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            self._meta.model._default_manager.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        from django import forms
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class UserChangeForm (BaseUserChangeForm):
    class Meta:
        model = User


class UserAdmin (BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = BaseUserAdmin.list_display + ('date_joined', 'last_login', 'visible_on_home',)
    list_editable = BaseUserAdmin.list_editable + ('visible_on_home',)


admin.site.register(Vision, VisionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Reply)
admin.site.register(Category)
admin.site.register(Tweet, TweetAdmin)
