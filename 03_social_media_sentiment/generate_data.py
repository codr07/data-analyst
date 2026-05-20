import csv
import random
from datetime import datetime, timedelta

def main():
    print("[*] Generating social media sentiment dataset...")
    
    # Templates for synthetic posts
    positive_templates = [
        "Absolutely love the new CODR Analytics tool! It has saved us hours of work. #dataanalytics #business",
        "The antigravity framework is incredibly fast. Perceived latency is virtually zero!",
        "Stunning dashboard design by CODR. Simple, clean, and highly interactive.",
        "Great customer support! Resolved my query in under 5 minutes. highly recommend.",
        "Best tool in the market for data analysts. The visualization capabilities are second to none.",
        "This software is a game changer for our business intelligence pipeline. Great job, team!",
        "Incredibly impressed with the performance scaling. Handles millions of rows without a sweat.",
        "So easy to use, even our marketing team can run queries now. Fantastic UX design.",
        "Excellent product! Clean code, solid documentation, and flawless execution.",
        "Smooth transitions, high speed, and elegant aesthetics. Truly premium feel."
    ]
    
    negative_templates = [
        "Extremely disappointed with the latest update. The interface keeps freezing on load.",
        "This app is so slow, it takes minutes to load a simple CSV. Unacceptable performance.",
        "The pricing model is a complete rip-off. Too expensive for such basic features.",
        "Encountered a major bug in the SQL query parser. It threw a database connection timeout again.",
        "The documentation is extremely outdated. Half of the API endpoints don't work as documented.",
        "Terrible experience. The dashboard crashed twice in the middle of our presentation.",
        "The interface feels very clunky and outdated. Needs a major visual redesign.",
        "Customer support is completely unresponsive. Opened a ticket 3 days ago, still no response.",
        "Full of bugs and random crashes. Do not waste your money on this.",
        "High latency and constant lag. This is definitely not the standard we expected."
    ]
    
    neutral_templates = [
        "Just downloaded the new analytics tool. Let's see how it compares to others.",
        "Is there a way to export the reports to PDF directly? Checking the documentation now.",
        "CODR Analytics has released its quarterly update today. #tech #software",
        "Looking for recommendations for a reliable forecasting tool. Any thoughts?",
        "Reading a comparison article between various Python NLP libraries today.",
        "Standard data analytics platform. Has all the basic features you'd expect.",
        "The app underwent scheduled server maintenance last night. No major changes noticed.",
        "We are currently evaluating multiple BI tools for our team's workflow.",
        "New version released. Testing the query speeds on our staging server.",
        "Just finished configuring the database connection. Ready to start analysis."
    ]
    
    usernames = ["@data_dan", "@tech_guru", "@biz_leader", "@code_ninja", "@data_queen", 
                 "@startup_founder", "@analyst_sam", "@dev_alice", "@cloud_expert", "@it_manager"]
    
    start_date = datetime(2026, 1, 1)
    
    records = []
    
    # Generate 400 posts with varying sentiments
    # 55% positive, 25% neutral, 20% negative
    for i in range(1, 401):
        post_id = f"POST{i:04d}"
        days_ago = random.randint(0, 120)
        post_date = (start_date + timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
        username = random.choice(usernames)
        
        sentiment_choice = random.choices(["Positive", "Neutral", "Negative"], weights=[0.55, 0.25, 0.20])[0]
        
        if sentiment_choice == "Positive":
            text = random.choice(positive_templates)
            # Add some variations
            if random.random() > 0.5:
                text += f" Thanks to the developers!"
        elif sentiment_choice == "Negative":
            text = random.choice(negative_templates)
            if random.random() > 0.5:
                text += f" Please fix this ASAP."
        else:
            text = random.choice(neutral_templates)
            
        records.append([post_id, post_date, username, text, sentiment_choice])
        
    records.sort(key=lambda x: x[1])
    
    with open("social_media_posts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Post_ID", "Date", "Username", "Text", "True_Sentiment"])
        writer.writerows(records)
        
    print(f"[+] Successfully generated {len(records)} social media posts in social_media_posts.csv.")

if __name__ == "__main__":
    main()
