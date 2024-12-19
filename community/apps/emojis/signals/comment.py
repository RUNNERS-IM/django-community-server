from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from community.apps.emojis.models import CommentEmoji


# Main Section
@receiver(pre_save, sender=CommentEmoji)
def comment_emoji_pre_save(sender, instance, *args, **kwargs):
    print("========== CommentEmoji pre_save ==========")

    if not instance.id:
        instance._is_changed = False
    else:
        _instance = CommentEmoji.objects.filter(id=instance.id).first()
        instance._is_changed = _instance.emoji_code != instance.emoji_code


@receiver(post_save, sender=CommentEmoji)
def sync_post_emoji_post_save(sender, instance, created, **kwargs):
    print("========== CommentEmoji post_save : Sync ==========")
    # 1. alarm, activityLog 생성 (기획 필요)
    # 2. friend point history 추가

    comment = instance.comment
    comment_user = instance.user
    user = instance.user

    post = comment.post
    club = post.club

    is_friend = user.check_friend(comment_user)
    is_changed = instance._is_changed

    # Emoji 추가한 경우
    if created or is_changed:
        # Send Alarm
        # if comment_user != user:
        #     send_alarm(
        #         user_id=comment_user.id,
        #         type="POST/COMMENT_LIKE",
        #         club_id=club.id,
        #         post_id=post.id,
        #         comment_id=comment.id,
        #         user_other_id=user.id,
        #     )

        # Send ActivityLog
        # send_activity_log(
        #     user_id=user.id,
        #     type="CLUB/COMMENT_LIKE",
        #     image_url=club.profile_image_url,
        #     club_id=club.id,
        #     post_id=post.id,
        #     contents=comment.content_summary,
        # )

        if is_friend:
            # Create Friend Point History Task
            print("Comment Emoji 추가 친구 포인트")
            # is_child_comment = True if comment.parent_comment else False
            # friend_point_type = HISTORY_LIKE_CHILD_COMMENT if is_child_comment else HISTORY_LIKE_COMMENT
            #
            # FriendPointHistoriesProducer().create_friend_point_history(
            #     me_id=user.id,
            #     user_id=comment_user.id,
            #     friend_point_type=friend_point_type,
            # )


@receiver(post_save, sender=CommentEmoji)
def count_comment_emoji_post_save(sender, instance, created, **kwargs):
    print("========== CommentEmoji post_save : Count ==========")

    comment = instance.comment
    post = comment.post
    club = post.club
    is_changed = instance._is_changed

    if created or is_changed:
        comment.update_emoji_count()

        # Post PostEmoji Count
        post.update_comments_emoji_count()

        # Profile PostEmoji Count
        instance.profile.update_profile_comments_emoji_count()

        # Club PostEmoji Count
        club.update_club_comments_emoji_count()


@receiver(post_delete, sender=CommentEmoji)
def post_emoji_post_delete(sender, instance, *args, **kwargs):
    print("========== CommentEmoji post_delete ==========")
    # 1. 카운트 감소
    # 2. friend point history 추가

    comment = instance.comment
    comment_user = comment.user
    user = instance.user
    post = comment.post
    club = post.club

    is_friend = user.check_friend(comment_user)

    #
    comment.update_emoji_count()
    # Post CommentEmoji Count
    post.update_comments_emoji_count()

    # Profile CommentEmoji Count
    instance.profile.update_profile_comments_emoji_count()

    # Club CommentEmoji Count
    club.update_club_comments_emoji_count()

    if is_friend:
        print("Comment Emoji 삭제 친구 포인트")
        # is_child_comment = True if comment.parent_comment else False
        # friend_point_type = HISTORY_UNLIKE_CHILD_COMMENT if is_child_comment else HISTORY_UNLIKE_COMMENT
        #
        # FriendPointHistoriesProducer().create_friend_point_history(
        #     me_id=user.id,
        #     user_id=comment_user.id,
        #     friend_point_type=friend_point_type,
        # )
