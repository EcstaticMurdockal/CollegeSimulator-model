"""
Reddit r/collegeresults Scraper
Collects self-reported college admissions data from Reddit
"""

import praw
import pandas as pd
import re
import json
from datetime import datetime
from typing import Dict, List, Optional
import time

class CollegeResultsScraper:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """
        Initialize Reddit API client

        To get credentials:
        1. Go to https://www.reddit.com/prefs/apps
        2. Click "create app" or "create another app"
        3. Select "script"
        4. Get client_id and client_secret
        """
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.subreddit = self.reddit.subreddit('collegeresults')

    def extract_stats_from_text(self, text: str) -> Dict:
        """Extract admissions statistics from post text"""
        data = {
            'gpa_unweighted': None,
            'gpa_weighted': None,
            'sat_total': None,
            'sat_math': None,
            'sat_ebrw': None,
            'act_composite': None,
            'ap_courses': [],
            'extracurriculars': [],
            'awards': [],
            'essays_quality': None,
            'lor_quality': None,
            'intended_major': None,
            'ethnicity': None,
            'gender': None,
            'state': None,
            'country': None,
            'first_gen': None,
            'legacy': None,
            'income_bracket': None,
            'decisions': []
        }

        text_lower = text.lower()

        # Extract GPA
        gpa_patterns = [
            r'gpa[:\s]+(\d\.\d+)\s*(?:uw|unweighted)',
            r'unweighted gpa[:\s]+(\d\.\d+)',
            r'uw gpa[:\s]+(\d\.\d+)',
            r'gpa[:\s]+(\d\.\d+)/4\.0'
        ]
        for pattern in gpa_patterns:
            match = re.search(pattern, text_lower)
            if match:
                data['gpa_unweighted'] = float(match.group(1))
                break

        weighted_patterns = [
            r'gpa[:\s]+(\d\.\d+)\s*(?:w|weighted)',
            r'weighted gpa[:\s]+(\d\.\d+)',
            r'w gpa[:\s]+(\d\.\d+)'
        ]
        for pattern in weighted_patterns:
            match = re.search(pattern, text_lower)
            if match:
                data['gpa_weighted'] = float(match.group(1))
                break

        # Extract SAT
        sat_patterns = [
            r'sat[:\s]+(\d{3,4})',
            r'sat score[:\s]+(\d{3,4})'
        ]
        for pattern in sat_patterns:
            match = re.search(pattern, text_lower)
            if match:
                score = int(match.group(1))
                if 400 <= score <= 1600:
                    data['sat_total'] = score
                break

        # Extract SAT subscores
        math_match = re.search(r'sat math[:\s]+(\d{3})', text_lower)
        if math_match:
            data['sat_math'] = int(math_match.group(1))

        ebrw_match = re.search(r'sat (?:ebrw|reading)[:\s]+(\d{3})', text_lower)
        if ebrw_match:
            data['sat_ebrw'] = int(ebrw_match.group(1))

        # Extract ACT
        act_match = re.search(r'act[:\s]+(\d{1,2})', text_lower)
        if act_match:
            score = int(act_match.group(1))
            if 1 <= score <= 36:
                data['act_composite'] = score

        # Extract AP courses
        ap_pattern = r'ap ([a-z\s]+?)(?:\s*-\s*|\s+)(\d)'
        ap_matches = re.findall(ap_pattern, text_lower)
        for subject, score in ap_matches:
            data['ap_courses'].append({
                'subject': subject.strip().title(),
                'score': int(score)
            })

        # Extract demographics
        if 'asian' in text_lower:
            data['ethnicity'] = 'Asian'
        elif 'white' in text_lower or 'caucasian' in text_lower:
            data['ethnicity'] = 'White'
        elif 'hispanic' in text_lower or 'latino' in text_lower:
            data['ethnicity'] = 'Hispanic/Latino'
        elif 'black' in text_lower or 'african american' in text_lower:
            data['ethnicity'] = 'Black/African American'

        if 'male' in text_lower and 'female' not in text_lower:
            data['gender'] = 'Male'
        elif 'female' in text_lower:
            data['gender'] = 'Female'

        # Extract first-gen status
        if 'first gen' in text_lower or 'first-gen' in text_lower:
            data['first_gen'] = True

        # Extract legacy
        if 'legacy' in text_lower:
            data['legacy'] = True

        # Extract intended major
        major_keywords = ['computer science', 'cs', 'engineering', 'biology', 'chemistry',
                         'physics', 'mathematics', 'economics', 'business', 'psychology',
                         'english', 'history', 'political science']
        for keyword in major_keywords:
            if keyword in text_lower:
                data['intended_major'] = keyword.title()
                break

        # Extract decisions
        decision_patterns = [
            (r'accepted[:\s]+([a-z\s,]+)', 'accepted'),
            (r'admitted[:\s]+([a-z\s,]+)', 'accepted'),
            (r'rejected[:\s]+([a-z\s,]+)', 'rejected'),
            (r'waitlisted[:\s]+([a-z\s,]+)', 'waitlisted'),
            (r'deferred[:\s]+([a-z\s,]+)', 'deferred')
        ]

        for pattern, decision_type in decision_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                schools = [s.strip().title() for s in match.split(',')]
                for school in schools:
                    if len(school) > 3:  # Filter out noise
                        data['decisions'].append({
                            'school': school,
                            'decision': decision_type
                        })

        return data

    def scrape_posts(self, limit: int = 1000, time_filter: str = 'all') -> List[Dict]:
        """
        Scrape posts from r/collegeresults

        Args:
            limit: Number of posts to scrape
            time_filter: 'all', 'year', 'month', 'week', 'day'
        """
        posts_data = []

        print(f"Scraping {limit} posts from r/collegeresults...")

        for post in self.subreddit.top(time_filter=time_filter, limit=limit):
            try:
                # Extract data from post
                post_data = self.extract_stats_from_text(post.selftext + " " + post.title)

                # Add metadata
                post_data['post_id'] = post.id
                post_data['post_title'] = post.title
                post_data['post_date'] = datetime.fromtimestamp(post.created_utc).isoformat()
                post_data['post_score'] = post.score
                post_data['num_comments'] = post.num_comments

                # Only keep posts with at least some data
                if post_data['gpa_unweighted'] or post_data['sat_total'] or post_data['act_composite']:
                    posts_data.append(post_data)
                    print(f"Scraped post {len(posts_data)}: {post.title[:50]}...")

                # Rate limiting
                time.sleep(0.5)

            except Exception as e:
                print(f"Error scraping post {post.id}: {e}")
                continue

        print(f"Successfully scraped {len(posts_data)} posts with data")
        return posts_data

    def save_to_csv(self, data: List[Dict], filename: str):
        """Save scraped data to CSV"""
        # Flatten nested structures for CSV
        flattened_data = []
        for post in data:
            for decision in post.get('decisions', []):
                row = {
                    'post_id': post['post_id'],
                    'post_date': post['post_date'],
                    'gpa_unweighted': post['gpa_unweighted'],
                    'gpa_weighted': post['gpa_weighted'],
                    'sat_total': post['sat_total'],
                    'sat_math': post['sat_math'],
                    'sat_ebrw': post['sat_ebrw'],
                    'act_composite': post['act_composite'],
                    'num_ap_courses': len(post['ap_courses']),
                    'intended_major': post['intended_major'],
                    'ethnicity': post['ethnicity'],
                    'gender': post['gender'],
                    'first_gen': post['first_gen'],
                    'legacy': post['legacy'],
                    'school': decision['school'],
                    'decision': decision['decision']
                }
                flattened_data.append(row)

        df = pd.DataFrame(flattened_data)
        df.to_csv(filename, index=False)
        print(f"Saved {len(flattened_data)} records to {filename}")
        return df

    def save_to_json(self, data: List[Dict], filename: str):
        """Save scraped data to JSON (preserves nested structure)"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} posts to {filename}")


def main():
    """
    Main function to run the scraper

    IMPORTANT: You need to create a Reddit app to get credentials:
    1. Go to https://www.reddit.com/prefs/apps
    2. Click "create app"
    3. Select "script"
    4. Fill in name and redirect uri (http://localhost:8080)
    5. Copy client_id and client_secret
    """

    # TODO: Replace with your Reddit API credentials
    CLIENT_ID = "YOUR_CLIENT_ID_HERE"
    CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
    USER_AGENT = "CollegeAdmissionsResearch/1.0"

    if CLIENT_ID == "YOUR_CLIENT_ID_HERE":
        print("ERROR: Please set your Reddit API credentials in the script")
        print("Visit https://www.reddit.com/prefs/apps to create an app")
        return

    # Initialize scraper
    scraper = CollegeResultsScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)

    # Scrape posts
    posts = scraper.scrape_posts(limit=2000, time_filter='all')

    # Save data
    scraper.save_to_csv(posts, 'reddit_admissions_data.csv')
    scraper.save_to_json(posts, 'reddit_admissions_data.json')

    print("\nData collection complete!")
    print(f"Total posts scraped: {len(posts)}")


if __name__ == "__main__":
    main()
