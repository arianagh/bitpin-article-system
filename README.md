# 🌟 Article Rating Django Project 🌟

This project is a Django application that allows users to view articles and rate them. The application utilizes Django
REST Framework (DRF) to provide a robust API for interaction.

## Features

1. **Article Listing**:
    - Users can view a list of articles, each containing a title and content.
    - Articles display the average score and the number of ratings.

2. **Rating System**:
    - Users can submit ratings for articles on a scale from 0 to 5.
    - Users have the ability to update their previously submitted ratings.

3. **Performance Optimization**:
    - The system is designed to handle high volumes of ratings without performance degradation.
    - We implemented an **eventual consistency** model, allowing the application to handle large loads efficiently by
      ensuring that data is consistently updated across all instances while still maintaining responsiveness.

4. **Fraud Detection**:
    - The application includes multiple layers of fraud detection and an algorithm designed to identify and flag
      suspicious rating patterns. for detailed explanation you can read these sections:
      **[Fake Ratings Detailed Explanation](#fake-ratings-detailed-explanation)** ,
      **[Suggestions](#suggestions)** ,
      **[Potential Issues](#potential-issues)**.
        - **Weighted Scores**: Scores are weighted based on factors such as the user's rating history and the
          variability of their scores. This approach helps mitigate the influence of potentially fraudulent users by
          reducing the weight of their scores if they exhibit suspicious patterns.
        - **Algorithmic Analysis**: The system constantly analyzes recent scores in a time window and spike threshold
          defined by FraudDetectionConfig model with the use of numpy and pandas to detect anomalies, such as high
          concentrations of identical scores and sudden spikes in ratings to prevent manipulation, low standard
          deviations, scores significantly lower than the 24-hour mean, and outliers. If any suspicious activity is
          detected, the relevant scores are flagged for further review.
        - **Throttling and Rate Limiting**: To enhance security and prevent abuse, the application implements throttling
          and rate limiting. Users are restricted to a specific number of requests within a defined timeframe, ensuring
          that no single user can overwhelm the system with excessive ratings and we have per article throttling per
          minute too to avoid very unusual ratings.

5. **Best Practices**:
    - The project follows best practices in Django development, such as clear separation of concerns, using class-based
      views for scalability, and minimizing business logic in serializers.
    - Code is organized for readability and maintainability, ensuring that the project adheres to the principles of
      clean code.

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
    - Due to the network problems of Iran i myself couldn't build the image and i strongly suggest use the local
      approach to run the app.
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
   This task flags articles with suspicious ratings, based on the fraud detection algorithm and flag them for manual
   reviews by admins.

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

## Code Quality and Pre-commit Hooks

To maintain clean and consistent code quality, we have integrated pre-commit hooks into the project. The following tools
are used:

1. flake8: For linting Python code to ensure it follows PEP 8 standards.
2. yapf: For automatically formatting code to keep it consistent.
3. isort: For sorting imports in a standard way.
4. Missing Migrations Check: Ensures that all model changes have corresponding migrations committed.

These checks are automatically run before each commit to prevent bad code from being committed to the repository
for enabling them use this command:

1. ```pre-commit install```

## Fake Ratings Detailed Explanation

**Problem Statement:**
   - In any system that relies on user-generated ratings, there's always a risk of manipulation or fraudulent activity. Users
   or bots may attempt to skew the ratings of certain articles to either artificially inflate or deflate their perceived
   quality. This kind of manipulation undermines the integrity of the rating system and can lead to misleading information
   for other users. In this project, we needed to ensure that the ratings provided by users are as genuine as possible and
   not the result of fraudulent activity.
   Objectives

**The primary objectives of the fraud detection mechanism:**

   - Identify and flag suspicious ratings: Detect patterns in user ratings that suggest manipulation or abuse.
   Ensure data integrity: Maintain the credibility of the rating system by preventing skewed or biased data.
   Minimize false positives: Avoid incorrectly flagging legitimate user ratings as suspicious, ensuring that genuine feedback is accurately represented.

**Approach and Implementation:**

   - To achieve these objectives, we implemented a multi-layered fraud detection system mostly within the ArticleRatingsAnalyzer
   class. The system uses a combination of statistical analysis, historical data comparison, and custom rules to identify
   and flag suspicious ratings.

1. High Concentration of Identical Scores:

   - One of the simplest indicators of fraud is a high concentration of identical scores within a short period. For example,
   if an article suddenly receives a large number of identical ratings (e.g., a flood of 5-star ratings), it could indicate
   that someone is trying to manipulate the average score.

   Implementation:

   - We define a threshold for the concentration of identical scores. If more than 70% of the ratings for an article are identical, the system flags this as suspicious.
   The algorithm groups ratings by their value and checks the concentration against the threshold. If the threshold is exceeded, the ratings are marked as potentially fraudulent.

2. Weighted Scores:

   - To further refine our fraud detection, we assign weights to user scores when they are being created based on certain factors, such as the user's
   rating history. The idea is to reduce the impact of ratings from users who consistently give extreme or identical
   scores, which could indicate manipulation.

   Implementation:

    - We calculate the standard deviation of the scores a user has given across all articles. If a user consistently gives similar scores (e.g., always 5-stars), their scores are given less weight.
    The weight is dynamically adjusted based on the user's behavior, with more varied scoring patterns resulting in higher weights.

3. Spike Detection:

   - A sudden spike in the number of ratings for an article can also be indicative of fraudulent activity, especially if the
   ratings are clustered around a particular value. This spike could be the result of a coordinated effort to influence the
   article's average rating.

   Implementation:

   - The system monitors the number of ratings an article receives within a predefined time window (e.g., 5 minutes). If the number of ratings exceeds a certain threshold, the article's ratings are flagged for further analysis.
   The algorithm also considers the standard deviation of the scores during this spike. If the deviation is low, it indicates that the ratings are not diverse and are likely manipulated.

4. Comparison with Historical Data:

   - Comparing current ratings with historical data can reveal anomalies that indicate fraud. For instance, if an article's
   current mean rating is significantly lower than its mean rating from the previous 24 hours, it could suggest that
   the recent ratings are not genuine.

   Implementation:

   - The algorithm calculates the average rating of an article over the past 24 hours and compares it with the current average rating.
   If the current average is significantly lower, and this coincides with other suspicious patterns (e.g., low standard deviation, high concentration of identical scores), the ratings are flagged.

5. Comprehensive Analysis and Final Decision

   - The fraud detection system does not rely on a single metric but rather uses a combination of the above techniques to
   make a final decision. Each potential indicator of fraud (high concentration, spike detection, historical comparison)
   contributes to the overall analysis.

   Implementation:

   - The ArticleRatingsAnalyzer class collects all the identified suspicious ratings and updates their status in the database, marking them as suspicious and recording the reason for suspicion.
   The system is designed to minimize false positives by only flagging ratings when multiple indicators suggest fraud. this task is done by a cron job for example every 20 minutes.
   - We also have another cron job that runs for example every hour and flag the articles that have suspicious ratings for further review by admins of the system.

## Suggestions

While the current fraud detection mechanism is robust, there are several potential improvements and alternative approaches that could be explored:

Machine Learning-Based Detection:
  - Implementing a machine learning model that learns from past suspicious activities could improve the accuracy of fraud detection. This model could be trained to recognize complex patterns that may not be evident through simple statistical analysis and this
    is what most famous companies do like instagram and youtube and etc do.

User Behavior Analysis:
  - Analyzing user behavior across different articles and time periods could provide more insights into potential fraud. For example, users who frequently rate articles in a similar manner or who exhibit sudden changes in their rating behavior might be flagged for further investigation.

Real-Time Monitoring:
  - Integrating real-time monitoring with alerting could allow administrators to respond to potential fraud immediately. This could involve setting up dashboards that visualize rating activity and flag suspicious trends as they happen.

Adaptive Thresholds:
  - Instead of using fixed thresholds for flagging suspicious activities (e.g., a set number of identical scores), the system could use adaptive thresholds that change based on the article’s typical rating behavior. This would make the detection mechanism more flexible and context-sensitive.

Community Feedback:
  - Allowing users to report suspicious rating activities could complement the automated detection system. User reports could be used to train the fraud detection algorithms or trigger manual reviews.

## Potential Issues

While the current fraud detection mechanism is designed to be robust, it’s important to recognize some potential limitations and challenges:

False Positives:
  - The system may incorrectly flag legitimate scores as suspicious. For example, if a popular article receives a large number of identical scores due to genuine user sentiment, these scores might be mistakenly flagged as fraudulent.

Performance Overhead:
  - The fraud detection process involves complex calculations and data processing, which could impact performance, especially as the number of ratings and articles scales up. Ensuring that this process does not slow down the overall system is a key concern.

Dependence on Historical Data:
  - The effectiveness of the detection mechanism relies heavily on historical data, such as average scores over the last 24 hours. If there is insufficient historical data (e.g., for a newly published article), the accuracy of fraud detection may be compromised.

Fixed Thresholds:
  - The use of fixed thresholds for identifying suspicious activity (e.g., a certain percentage of identical scores) may not be suitable for all articles. Articles with a small number of ratings might be unfairly flagged, while those with a large number of ratings might require more sensitive thresholds.

User-Specific Patterns:
  - The current mechanism may not fully account for individual user behavior patterns. For instance, some users might naturally give similar scores across multiple articles, which could be misinterpreted as fraudulent activity.

Evasion Tactics:
  - As users and bots become more sophisticated, they may find ways to evade detection, such as by slightly varying scores or timing their submissions to avoid triggering the fraud detection algorithms.

Scalability:
  - As the application grows and more articles and ratings are added, the system may struggle to process and analyze all the data in a timely manner. This could lead to delays in detecting and responding to fraudulent activity. and the fact that we need a big operation team to sometimes manually review some articles and scores is not a scalable approach.