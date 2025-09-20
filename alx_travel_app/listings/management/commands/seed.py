import uuid
from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        # Create or get a sample host
        host, _ = User.objects.get_or_create(email='host@example.com', defaults={
            'first_name': 'Host',
            'last_name': 'Example',
            'password': 'password123'
        })

        # Create sample listings
        for i in range(5):
            Listing.objects.create(
                title=f"Sample Listing {i+1}",
                description="This is a sample description.",
                host=host,
                price_per_night=50 + i * 10
            )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
