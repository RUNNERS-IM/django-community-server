# Third Party
import asyncio

# Django
from django.core.management.base import BaseCommand

from community.apps.friends.services.consumer import (
    FriendConsumerService,
    FriendRequestConsumerService,
)


# Main Section
class Command(BaseCommand):
    help = "Consume messages"

    consumers = [
        FriendRequestConsumerService,
        FriendConsumerService,
    ]

    def handle(self, *args, **options):
        asyncio.run(self.handle_async(*args, **options))

    async def handle_async(self, *args, **kwargs):
        await asyncio.gather(*[consumer().consume_messages() for consumer in self.consumers])
