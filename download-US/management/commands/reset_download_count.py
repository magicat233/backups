from django.core.management.base import NoArgsCommand, CommandError
from django.db.models import F
from ubntcom.download.models import Download



class Command(NoArgsCommand):

    """
    Copy the `download_count_tracked` values to
    `download_count` and zero out `download_count_tracked`. 

    This is to allow the download "popularity rankings" to be
    aggregated over a shorter segment of time, such as
    a single month.
    """

    def handle_noargs(self, *args, **kwargs):

        Download.objects.all().update(download_count=F('download_count_tracked'))
        Download.objects.all().update(download_count_tracked=0)