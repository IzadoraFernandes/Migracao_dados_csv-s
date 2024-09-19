import csv
from datetime import datetime
from django.utils import timezone
from .models import Rating, Tag, Movie, Link, GenomeScore, GenomeTag, FileUpload

def import_ratings(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Rating.objects.create(
                userId=row['userId'],
                movieId=row['movieId'],
                rating=row['rating'],
                timestamp=row['timestamp']
            )

def import_tags(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Tag.objects.create(
                userId=row['userId'],
                movieId=row['movieId'],
                tag=row['tag'],
                timestamp=row['timestamp']
            )

def import_movies(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Movie.objects.create(
                movieId=row['movieId'],
                title=row['title'],
                genres=row['genres']
            )

def import_links(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Link.objects.create(
                movieId=Movie.objects.get(movieId=row['movieId']),
                imdbId=row['imdbId'],
                tmdbId=row['tmdbId']
            )

def import_genome_scores(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            GenomeScore.objects.create(
                movieId=row['movieId'],
                tagId=row['tagId'],
                relevance=row['relevance']
            )

def import_genome_tags(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            GenomeTag.objects.create(
                tagId=row['tagId'],
                tag=row['tag']
            )

def record_file_upload(file_name, records_inserted, records_failed, start_time):
    upload = FileUpload(
        file_name=file_name,
        upload_date=timezone.now(),
        processing_time=timezone.now() - start_time,
        records_inserted=records_inserted,
        records_failed=records_failed,
    )
    upload.save()

def main():
    start_time = timezone.now()
    
    try:
        import_ratings('path_to_ratings.csv')
        import_tags('path_to_tags.csv')
        import_movies('path_to_movies.csv')
        import_links('path_to_links.csv')
        import_genome_scores('path_to_genome-scores.csv')
        import_genome_tags('path_to_genome-tags.csv')

        records_inserted = Rating.objects.count() + Tag.objects.count() + Movie.objects.count() + Link.objects.count() + GenomeScore.objects.count() + GenomeTag.objects.count()
        records_failed = 0

        record_file_upload('MovieLens 20M Dataset', records_inserted, records_failed, start_time)
        print("Data import completed successfully.")
    except Exception as e:
        records_failed = 1
        print(f"An error occurred: {e}")
        record_file_upload('MovieLens 20M Dataset', 0, records_failed, start_time)

if __name__ == '__main__':
    main()
