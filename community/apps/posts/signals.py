# Django
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from community.apps.badges.models import Badge

# Models
from community.apps.posts.models import Post

# Tasks
from community.apps.posts.tasks import sync_post_task
from community.apps.profiles.api.serializers import ProfileSerializer
from community.apps.profiles.models import Profile

# Serializers
from community.apps.users.api.serializers import UserProfileSerializer

# Base
from config.settings.base import SUPERCLUB_WEB_HOST


# Main Section
@receiver(pre_save, sender=Post)
def post_pre_save_sync_post(sender, instance, *args, **kwargs):
    print("========== Post pre_save: Sync Post ==========")
    if instance.id is None:
        if instance.user:
            instance.user_data = UserProfileSerializer(instance=instance.user).data

        if instance.profile:
            instance.profile_data = ProfileSerializer(instance.profile).data

    else:
        _instance = Post.objects.filter(id=instance.id).first()
        if _instance:
            for field in [
                # Main
                "content_summary",
                "public_type",
                "password",
                "reserved_at",
                "boomed_at",
                "point",
                # Count
                "comment_count",
                "total_like_count",
                "dislike_count",
                "like_count",
                "fun_count",
                "healing_count",
                "legend_count",
                "useful_count",
                "empathy_count",
                "devil_count",
                # Boolean
                "password",
                "is_notice",
                "is_event",
                "is_temporary",
                "is_secret",
                "is_search",
                "is_share",
                "is_comment",
                "is_reserved",
                "is_boomed",
                "is_active",
                "is_deleted",
                # Date
                "achieved_20_points_at",
            ]:
                _value = getattr(_instance, field)
                value = getattr(instance, field)

                if _value != value:
                    print("========================= sync_post_task =========================")
                    try:
                        sync_post_task.apply_async((instance.id,), countdown=2)
                    except BaseException:
                        pass


@receiver(post_save, sender=Post)
def post_post_save_create_new_post_badge(sender, instance, created, **kwargs):
    print("========== Post post_save : Create New Post Badge ==========")
    if created:
        if not instance.is_temporary and not instance.is_agenda:
            new_post_badge = Badge.objects.get(title_en="New Post", model_type="POST")
            instance.badges.add(new_post_badge.id)


@receiver(post_save, sender=Post)
def post_post_save_set_web_url(sender, instance, created, **kwargs):
    print("========== Post post_save: Set Web Url Field ==========")
    if created:
        if not instance.is_temporary:
            instance.web_url = SUPERCLUB_WEB_HOST + f"/community/{instance.community.id}/post/{instance.id}"


@receiver(post_save, sender=Post)
def post_post_save_create_profile(sender, instance, created, **kwargs):
    print("========== Post post_save: Create Profile ==========")
    if created:
        profile = Profile.objects.filter(user=instance.user, community=instance.community).first()
        if profile is None:
            profile = Profile.objects.create(user=instance.user, community=instance.community)
            instance.profile_data = ProfileSerializer(instance=profile).data


@receiver(post_save, sender=Post)
def post_post_save(sender, instance, created, **kwargs):
    print("========================= Post post_save: Sync Post =========================")
    if (
        created
        and not instance.is_default
        and not instance.is_temporary
        and not instance.is_reserved
        and instance.public_type != "ONLY_ME"
    ):
        sync_post_task.apply_async((instance.id,), countdown=2)
