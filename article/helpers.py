from collections import Counter
from datetime import timedelta

import numpy as np
import pandas as pd
from django.utils import timezone

from .models import FraudDetectionConfig, Score


class ArticleRatingsAnalyzer:
    HIGH_CONCENTRATION_THRESHOLD = 0.8

    def __init__(self):
        self.config = FraudDetectionConfig.objects.first()
        self.now = timezone.now()
        self.start_time = self.now - timedelta(minutes=self.config.time_window_minutes)
        self.day_ago = self.now - timedelta(hours=24)
        self.score_updates = []

    def analyze(self):
        last_24_hours_mean_per_article = self._get_last_24_hours_mean_per_article()
        grouped = self._get_grouped_recent_scores()

        for article_id, group in grouped:
            self._process_article_group(article_id, group, last_24_hours_mean_per_article)

        self._update_suspicious_scores()

    def _get_recent_scores(self):
        return Score.objects.filter(created_at__gte=self.start_time,
                                    updated_at__gte=self.start_time)

    def _get_grouped_recent_scores(self):
        recent_scores = self._get_recent_scores()
        data = pd.DataFrame(
            list(recent_scores.values('id', 'article_id', 'value', 'weight', 'created_at')))
        if not data.empty:
            return data.groupby('article_id')

    def _get_last_24_hours_mean_per_article(self):
        last_24_hours_scores = Score.objects.filter(created_at__gte=self.day_ago,
                                                    created_at__lte=self.start_time)
        if last_24_hours_scores.exists():
            last_24_hours_data = pd.DataFrame(
                list(last_24_hours_scores.values('article_id', 'value')))
            last_24_hours_mean_per_article = last_24_hours_data.groupby(
                'article_id')['value'].mean().to_dict()
            return last_24_hours_mean_per_article
        return {}

    def _process_article_group(self, article_id, group, last_24_hours_mean_per_article):
        scores = group['value'].to_numpy()
        count_scores = len(scores)
        weighted_std_dev = np.std(scores)
        mean_scores = np.mean(scores)
        mode_score, mode_count = Counter(scores).most_common(1)[0]
        is_suspicious = False
        reason_of_suspicion = ""

        last_24_hours_mean = last_24_hours_mean_per_article.get(article_id, 0)

        if mode_count >= len(scores) * self.HIGH_CONCENTRATION_THRESHOLD:
            is_suspicious = True
            reason_of_suspicion = (f"High concentration of identical scores: {mode_count} out of"
                                   f" {len(scores)} scores are {mode_score}. --- ")
            suspicious_score_ids = group[group['value'] == mode_score]['id']

        elif count_scores > self.config.spike_threshold:
            if weighted_std_dev < self.config.min_score_deviation:
                is_suspicious = True
                reason_of_suspicion += f"Low standard deviation detected: {weighted_std_dev}. --- "

            if mean_scores < last_24_hours_mean:
                is_suspicious = True
                reason_of_suspicion += (f"Mean score lower than 24-hour average: "
                                        f"{mean_scores} < {last_24_hours_mean}. --- ")

            outlier_scores = group[~group['value'].isin([
                score for score in scores
                if np.abs(score - mode_score) >= self.config.min_score_deviation
            ])]['id']

            suspicious_score_ids = outlier_scores if len(outlier_scores) > 0 else group['id']
        else:
            suspicious_score_ids = pd.Series()

        if is_suspicious and not suspicious_score_ids.empty:
            self._collect_score_updates(suspicious_score_ids, reason_of_suspicion)

    def _collect_score_updates(self, suspicious_score_ids, reason_of_suspicion):
        self.score_updates.extend([{
            'id': score_id,
            'is_suspicious': True,
            'reason_of_suspicion': reason_of_suspicion
        } for score_id in suspicious_score_ids])

    def _update_suspicious_scores(self):
        if self.score_updates:
            scores_to_update = Score.objects.filter(
                id__in=[score['id'] for score in self.score_updates])
            updates_dict = {update['id']: update for update in self.score_updates}
            for score in scores_to_update:
                update = updates_dict[score.id]
                score.is_suspicious = update['is_suspicious']
                score.reason_of_suspicion = update['reason_of_suspicion']
            Score.objects.bulk_update(scores_to_update, ['is_suspicious', 'reason_of_suspicion'],
                                      batch_size=750)
