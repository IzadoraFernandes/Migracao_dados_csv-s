import csv
import time
from django.utils import timezone
from .models import Movie, Rating, Tag, Link, GenomeScore, GenomeTag, FileUpload
from celery import shared_task

@shared_task
def process_csv_file(file_path, file_name):
    start_time = time.time()
    records_inserted = 0
    records_failed = 0
    
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            if 'ratings' in file_name:
                for row in reader:
                    try:
                        Rating.objects.create(
                            userId=row['userId'],
                            movieId=row['movieId'],
                            rating=row['rating'],
                            timestamp=row['timestamp']
                        )
                        records_inserted += 1
                    except Exception as e:
                        records_failed += 1
            elif 'tags' in file_name:
                for row in reader:
                    try:
                        Tag.objects.create(
                            userId=row['userId'],
                            movieId=row['movieId'],
                            tag=row['tag'],
                            timestamp=row['timestamp']
                        )
                        records_inserted += 1
                    except Exception as e:
                        records_failed += 1
            elif 'movies' in file_name:
                for row in reader:
                    try:
                        Movie.objects.create(
                            movieId=row['movieId'],
                            title=row['title'],
                            genres=row['genres']
                        )
                        records_inserted += 1
                    except Exception as e:
                        records_failed += 1
            elif 'links' in file_name:
                for row in reader:
                    try:
                        movie = Movie.objects.get(movieId=row['movieId'])
                        Link.objects.create(
                            movieId=movie,
                            imdbId=row['imdbId'],
                            tmdbId=row['tmdbId']
                        )
                        records_inserted += 1
                    except Exception as e:
                        records_failed += 1
            elif 'genome-scores' in file_name:
                for row in reader:
                    try:
                        GenomeScore.objects.create(
                            movieId=row['movieId'],
                            tagId=row['tagId'],
                            relevance=row['relevance']
                        )
                        records_inserted += 1
                    except Exception as e:
                        records_failed += 1
            elif 'genome-tags' in file_name:
                for row in reader:
                    try:
                        GenomeTag.objects.create(
                            tagId=row['tagId'],
                            tag=row['tag']
                        )
                        records_inserted += 1
                    except Exception as e:
                        records_failed += 1

        processing_time = timezone.timedelta(seconds=(time.time() - start_time))
        file_upload = FileUpload.objects.get(file_name=file_name)
        file_upload.processing_time = processing_time
        file_upload.records_inserted = records_inserted
        file_upload.records_failed = records_failed
        file_upload.save()
    except Exception as e:
        print(f"Error processing file {file_name}: {e}")
