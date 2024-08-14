# 🌟 Article Rating Django Project 🌟

This project is a Django application that allows users to view articles and rate them. The application utilizes Django REST Framework (DRF) to provide a robust API for interaction. 

## Features

1. **Article Listing**: 
   - Users can view a list of articles, each containing a title and content.
   - Articles display the average score and the number of ratings.

2. **Rating System**: 
   - Users can submit ratings for articles on a scale from 0 to 5.
   - Users have the ability to update their previously submitted ratings.

3. **Performance Optimization**: 
   - The system is designed to handle high volumes of ratings without performance degradation. 
   - We implemented an **eventual consistency** model, allowing the application to handle large loads efficiently by ensuring that data is consistently updated across all instances while still maintaining responsiveness.

4. **Fraud Detection**: 
   - The application includes fraud detection layers and algorithm to identify and flag suspicious rating patterns.
   - High concentrations of identical scores or sudden spikes in ratings are monitored to prevent manipulation.
   - To enhance security and prevent abuse, the application implements throttling and rate limiting. Users are restricted to a specific number of requests within a defined timeframe, ensuring that no single user can overwhelm the system with excessive ratings.

5. **Best Practices**: 
   - The project follows best practices in Django development, such as clear separation of concerns, using class-based views for scalability, and minimizing business logic in serializers.
   - Code is organized for readability and maintainability, ensuring that the project adheres to the principles of clean code.

## Technologies Used

- Django
- Django REST Framework (DRF)
- JWT (JSON Web Tokens)
- Celery
- Cron jobs
- Docker Compose
- PostgreSQL
- Redis
- Swagger (DRF Spectacular)
- Makefile (You can use it for easier running the commands)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd article-rating-project
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Makemigrations:**:
   ```bash
   python manage.py makemigrations
   ```

5. **Run Migrations:**:
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver --settings=core.settings.development
   ```

7. **Create Super User**:
   ```bash
   python manage.py createsuperuser
   ```
## Setup Instructions Using Docker Compose

1. **Run With Docker Compose**:
   ```bash
   docker compose up --build
   docker compose exec app python manage.py makemigrations
   docker compose exec app python manage.py migrate
   ```

## Testing

The project includes a suite of tests to ensure reliability.
To run the tests, execute:
   ```bash
   python manage.py test
   ```

## Celery Tasks and Scheduled Jobs

The project includes several scheduled tasks managed by Celery and cron jobs:

1. Batch Update Article Ratings:
  Task: article.tasks.batch_update_article_ratings
  Schedule: Every 1 minute
  This task updates the ratings for articles in batches based on recent submissions.

2. Update Stale Articles:
  Task: article.tasks.update_stale_articles
  Schedule: Every day at 23:59
  This task updates articles that have not been updated recently, ensuring the data remains fresh.

3. Flag Suspicious Articles:
  Task: article.tasks.flag_suspicious_articles
  Schedule: Every 60 minutes
  This task flags articles with suspicious ratings, based on the fraud detection algorithm and flag them for manual reviews by admins.
   
4. Find And Flag Suspicious Ratings:
  Task: article.tasks.find_suspicious_ratings
  Schedule: Every 20 minutes
  This task analyzes recent ratings and identifies those that are potentially suspicious.

**These tasks are essential for maintaining the integrity and performance of the system, ensuring that data is accurate, 
up-to-date, and free from manipulation. to run the task use these commands:**
1. ```celery -A core.celery worker -l info```
2. ```celery -A core.celery beat -l info```

## API Endpoints

The API will be available at http://127.0.0.1:8000/api/. for
better convenience you can use the auto generated api doc from swagger at:
http://127.0.0.1:8000/api/docs/.

1. **Register A User**:
    ```bash
    POST /api/account/registration/
   ```
   
2. **Get Access Token**:
    ```bash
    POST /api/account/login/
   ```
   
3. **Create Some Articles**:
    ```bash
    POST /api/article/create/
   ```
   
4. **Create Some Scores For The Articles**:
    ```bash
    POST /api/article/score/{article_id}/create/
   ```
   
5. **Get The List Of Articles**:
    ```bash
    POST /api/article/list/
   ```



