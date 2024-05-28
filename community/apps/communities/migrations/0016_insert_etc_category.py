from django.db import migrations

from community.apps.communities.constants import categories


def update_category_titles(apps, schema_editor):
    # Community = apps.get_model('communities', 'Community')
    # for category in categories:
    #     if category["depth"] == 2 and category["2depth"] == "기타":
    #         category_1depth = Community.objects.filter(title_ko=category["1depth"], depth=1).first()
    #         category_2depth = Community.objects.filter(title_ko=category["2depth"], depth=2,
    #                                                    parent_community=category_1depth).first()
    #         if category_1depth and not category_2depth:
    #             category_2depth = Community.objects.create(
    #                 id=Community.objects.order_by("-id").first().id + 1,
    #                 parent_community=category_1depth,
    #                 title=category["title"],
    #                 depth=category["depth"],
    #                 title_en=category["title_en"],
    #                 title_ko=category["title_ko"],
    #                 title_ja=category["title_ja"],
    #                 title_zh_hans=category["title_zh_hans"],
    #                 title_zh_hant=category["title_zh_hant"],
    #                 title_es=category["title_es"],
    #                 title_ru=category["title_ru"],
    #                 title_ar=category["title_ar"]
    #             )
    #             print(f"==== {category_1depth.title} - {category_2depth.title} category 생성 완료====")
    pass


def reverse_update_category_titles(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('communities', '0015_insert_logo_image_url'),
    ]

    operations = [
        migrations.RunPython(
            code=update_category_titles,
            reverse_code=reverse_update_category_titles,
        ),
    ]
