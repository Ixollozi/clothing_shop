from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from store.platform.registry import iter_sites


class Command(BaseCommand):
    help = 'Apply migrations to every site database in platform mode.'

    def handle(self, *args, **options):
        from django.conf import settings

        if not getattr(settings, 'PLATFORM_MODE', False):
            raise CommandError('Set PLATFORM_MODE=1 before running platform_migrate.')

        for site in iter_sites():
            site.root.mkdir(parents=True, exist_ok=True)
            site.media_dir.mkdir(parents=True, exist_ok=True)
            self.stdout.write(f'Migrating {site.slug} ({site.database_alias})...')
            call_command(
                'migrate',
                database=site.database_alias,
                interactive=False,
                verbosity=options.get('verbosity', 1),
            )
        self.stdout.write(self.style.SUCCESS('All site databases migrated.'))
