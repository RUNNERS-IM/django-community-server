from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from community.apps.emojis.models import PostEmoji
from community.modules.producers.post_emojis import PostEmojiProducer


# Main Section
@receiver(pre_save, sender=PostEmoji)
def post_emoji_pre_save(sender, instance, *args, **kwargs):
    print("========== PostEmoji pre_save ==========")

    if not instance.id:
        # PostEmoji 생성시 User의 Activity Point 생성
        # create_activity_point(user_id=instance.post.user.id, type="CLUB_GET_LIKE")
        instance._is_changed = False
    else:
        _instance = PostEmoji.objects.filter(id=instance.id).first()
        instance._is_changed = _instance.emoji_code != instance.emoji_code


@receiver(post_save, sender=PostEmoji)
def sync_post_emoji_post_save(sender, instance, created, **kwargs):
    print("========== PostEmoji post_save : Sync ==========")
    # 1. post 서버 PostEmoji sync
    # 2. alarm, activityLog, activity 생성 (기획 필요)
    # 3. friend point history 추가

    post = instance.post
    post_user = post.user
    club = post.club
    user = instance.user

    is_friend = user.check_friend(post_user)
    is_changed = instance._is_changed

    if created or is_changed:
        PostEmojiProducer().sync_post_emoji(instance)

    # Emoji 추가한 경우
    if created or is_changed:
        # Send Alarm
        # if post_user != user:
        #     send_alarm(
        #         user_id=instance.post.user.id,
        #         type="POST/POST_LIKE",
        #         club_id=club.id,
        #         post_id=post.id,
        #         user_other_id=instance.user_id,
        #     )

        # Send ActivityLog
        # send_activity_log(
        #     user_id=user.id,
        #     type="CLUB/POST_LIKE",
        #     image_url=club.profile_image_url,
        #     club_id=club.id,
        #     post_id=post.id,
        #     contents=post.title,
        # )

        if is_friend:
            # Create Friend Point History Task
            print("Post Emoji 추가 친구 포인트")
            # FriendPointHistoriesProducer().create_friend_point_history(
            #     me_id=user.id,
            #     user_id=post_user.id,
            #     friend_point_type=HISTORY_LIKE_POST,
            # )

            # Send Activity
            # send_activity(
            #     user_id=user.id,
            #     type="POST_LIKE",
            #     image_url=post.thumbnail_media_url,
            #     club_id=club.id,
            #     post_id=post.id,
            # )


@receiver(post_save, sender=PostEmoji)
def count_post_emoji_post_save(sender, instance, created, **kwargs):
    print("========== PostEmoji post_save : Count ==========")

    post = instance.post
    profile = instance.profile
    club = post.club
    is_changed = instance._is_changed

    if created or is_changed:
        # Post PostEmoji Count
        post.update_post_emoji_count()

        # Profile PostEmoji Count
        profile.update_profile_posts_emoji_count()

        # Club PostEmoji Count
        club.update_club_posts_emoji_count()

        # Club Daily PostEmoji Count
        club.update_daily_count(type="posts_like", is_positive=True)


@receiver(post_delete, sender=PostEmoji)
def post_emoji_post_delete(sender, instance, *args, **kwargs):
    print("========== PostEmoji post_delete ==========")
    # 1. 카운트 감소.
    # 2. post 서버 PostEmoji 삭제 sync
    # 3. friend point history 추가

    post = instance.post
    user = instance.user
    post_user = post.user
    club = post.club

    is_friend = user.check_friend(post_user)

    # Post PostEmoji Count
    post.update_post_emoji_count()

    # Profile PostEmoji Count
    instance.profile.update_profile_posts_emoji_count()

    # Club PostEmoji Count
    post.club.update_club_posts_emoji_count()

    # Club Daily PostEmoji Count
    club.update_daily_count(type="posts_like", is_positive=False)

    if is_friend:
        print("Post Emoji 삭제 친구 포인트")
        # FriendPointHistoriesProducer().create_friend_point_history(
        #     me_id=user.id,
        #     user_id=post_user.id,
        #     friend_point_type=HISTORY_UNLIKE_POST,
        # )

    PostEmojiProducer().delete_post_emoji(instance)
