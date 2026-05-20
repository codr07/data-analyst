import csv
import random

def main():
    print("[*] Generating email fraud detection dataset...")
    
    # Text templates for Spam/Fraud (Label 1)
    fraud_templates = [
        ("URGENT: Verify your bank account immediately", "Dear Customer, We detected suspicious activity on your online bank account. Please click the link to verify your identity and prevent account suspension: http://secure-verify-login.net/auth. This is urgent."),
        ("Congratulations! You won $1,000,000 lottery!", "Dear lucky winner, your email address was selected as the grand prize winner of $1,000,000 in our international lottery promotion. To claim your cash prize, reply with your full name, phone number, and bank details."),
        ("Invoice payment overdue - Action required", "Hello, please find attached the invoice for your recent purchase. The payment of $4,520 is overdue. Please click the link below to settle the outstanding balance immediately: http://invoice-payment-portal.com/pay."),
        ("Work from home and earn $500/hour", "Hello! We are looking for remote data entry assistants. Work only 2 hours a day and earn $500 per hour. No experience required. If you are interested, please visit http://easy-money-jobs-now.com to apply today."),
        ("Security Alert: Google Account Compromised", "Dear User, someone just logged into your Gmail account from a new device in Russia. If this was not you, click here immediately to change your password and protect your credentials: http://google-safety-alert.com/reset."),
        ("Exclusive Offer: Cheap online prescriptions", "Get up to 80% off on all medications! Best prices online. Fast shipping, discrete packaging. Click here to browse our catalog: http://cheap-meds-discount.com/rx."),
        ("Your package delivery is pending validation", "Dear customer, your parcel from DHL could not be delivered due to an incorrect address. A redelivery fee of $1.50 is required. Please update your address and pay the fee at http://dhl-tracking-delivery.com."),
        ("Investment Opportunity: 500% returns guaranteed", "Hello, we represent a major cryptocurrency investment firm. Get 500% returns on your investment in 7 days. Guaranteed payouts. Reply to this email with 'START' to join our group.")
    ]
    
    # Text templates for Legitimate/Ham (Label 0)
    ham_templates = [
        ("Project Status Update - Weekly Meeting", "Hi team, please find the weekly project status report attached. Let's meet tomorrow at 10 AM in Conference Room B to discuss the database migration and backend container orchestration details. Thanks, Project Manager."),
        ("Dinner plans for Friday night?", "Hey, are you free this Friday for dinner? Some of us are planning to try the new Italian place downtown. Let me know by Wednesday so I can make a reservation. Hope you can make it!"),
        ("Data Analyst Interview Schedule", "Dear Sankha, thank you for applying for the Data Analyst position at CODR. We would like to schedule a 30-minute technical interview via Google Meet this Thursday at 2 PM. Please let us know if this time works for you."),
        ("Reviewed pull request: Fix memory leak", "Hi, I have reviewed your pull request for fixing the cache eviction leak in the Redis interface. The code looks clean and matches our design system. I have approved it and merged it into main."),
        ("Monthly newsletter: Tech trends", "Hello subscriber, here is our monthly digest of software development trends, covering concurrent React rendering, SEO strategies, and Edge caching performance metrics. Read the full article on our blog."),
        ("Your monthly utility bill is ready", "Dear resident, your digital utility bill for April 2026 is now available. The total amount due is $145.20, which will be auto-debited from your registered card on May 5th. Thank you."),
        ("Feedback request: Team performance", "Hi all, please take 5 minutes to fill out the quarterly team feedback survey. Your responses are anonymous and help us improve our developer tooling and workspace guidelines. Thanks, HR Team."),
        ("Notes from today's brainstorming session", "Hi everyone, here are the main notes and action items from our meeting: 1. Optimize CSS styles, 2. Add sanitization layer to input fields, 3. Review playtests. Let me know if I missed anything.")
    ]
    
    records = []
    
    # Generate 500 emails
    # ~25% fraud (1), ~75% ham (0)
    for i in range(1, 501):
        email_id = f"EM{i:04d}"
        label = random.choices([0, 1], weights=[0.75, 0.25])[0]
        
        if label == 1:
            subject, body = random.choice(fraud_templates)
            # Add small random changes
            body += f" Reference ID: {random.randint(10000, 99999)}."
        else:
            subject, body = random.choice(ham_templates)
            body += f" Sincerely, {random.choice(['Sankha', 'CODR', 'Team', 'HR'])}."
            
        full_text = f"Subject: {subject}\n\n{body}"
        records.append([email_id, full_text, label])
        
    random.shuffle(records)
    
    with open("email_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Email_ID", "Text", "Label"])
        writer.writerows(records)
        
    print(f"[+] Successfully generated {len(records)} emails in email_dataset.csv.")

if __name__ == "__main__":
    main()
