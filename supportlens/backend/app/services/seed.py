from datetime import datetime, timedelta
from sqlalchemy import select, func

from app.database import AsyncSessionLocal
from app.models import Trace, CategoryEnum


async def seed_database():
    """Seed the database with initial trace data if empty."""
    async with AsyncSessionLocal() as session:
        # Check if traces already exist
        result = await session.execute(select(func.count(Trace.id)))
        count = result.scalar()

        if count > 0:
            print(f"Database already seeded with {count} traces. Skipping seed.")
            return

        print("Seeding database with initial traces...")

        # Define 20 realistic traces
        traces = [
            # Billing (5)
            {
                "user_message": "I was charged twice this month for my Pro subscription. Can you check my account?",
                "bot_response": "I apologize for the duplicate charge. I've reviewed your account and confirmed you were charged twice on March 1st. I've initiated a refund for the duplicate payment of $49. It should appear in your account within 3-5 business days. Your subscription is active and correct.",
                "category": CategoryEnum.BILLING,
                "response_time_ms": 1250,
                "timestamp": datetime.utcnow() - timedelta(days=6, hours=14)
            },
            {
                "user_message": "What payment methods do you accept? I want to switch from credit card to PayPal.",
                "bot_response": "We accept credit cards (Visa, Mastercard, Amex), PayPal, and ACH bank transfers. To switch to PayPal, go to Settings > Billing > Payment Method and select 'Add PayPal'. Once added, you can set it as your default payment method. Let me know if you need help with this!",
                "category": CategoryEnum.BILLING,
                "response_time_ms": 980,
                "timestamp": datetime.utcnow() - timedelta(days=5, hours=8)
            },
            {
                "user_message": "My invoice shows $99 but I thought the Business plan was $79/month?",
                "bot_response": "The Business plan is $79/month for annual billing. The $99/month rate is for monthly billing. Your account is currently on monthly billing. If you'd like to switch to annual billing and save $240/year, I can help you make that change. Would you like to proceed?",
                "category": CategoryEnum.BILLING,
                "response_time_ms": 1420,
                "timestamp": datetime.utcnow() - timedelta(days=4, hours=11)
            },
            {
                "user_message": "I need a receipt for last month's payment for my expense report.",
                "bot_response": "I've just emailed your February invoice/receipt to the email address on file. It includes the full payment breakdown and transaction ID. If you need receipts for other months, you can also download them anytime from Settings > Billing > Invoice History.",
                "category": CategoryEnum.BILLING,
                "response_time_ms": 890,
                "timestamp": datetime.utcnow() - timedelta(days=3, hours=16)
            },
            {
                "user_message": "Why did my subscription price increase from $29 to $39?",
                "bot_response": "Your account was on our legacy Starter plan at $29/month. We sent an email 60 days ago about plan updates. The new Starter plan is $39/month but includes additional features like API access and priority support. Your grandfathered rate expired on March 1st. I can provide more details if needed.",
                "category": CategoryEnum.BILLING,
                "response_time_ms": 1650,
                "timestamp": datetime.utcnow() - timedelta(days=2, hours=9)
            },

            # Refund (4)
            {
                "user_message": "I accidentally upgraded to the wrong plan. Can I get a refund and switch back?",
                "bot_response": "Absolutely! Since the upgrade happened less than 24 hours ago, I can process a full refund and revert you to your previous plan. I've initiated the refund of $70 and downgraded your account back to the Pro plan. The refund will process within 5-7 business days.",
                "category": CategoryEnum.REFUND,
                "response_time_ms": 1340,
                "timestamp": datetime.utcnow() - timedelta(days=6, hours=10)
            },
            {
                "user_message": "I was charged $149 but I canceled my account last week. This shouldn't have happened.",
                "bot_response": "I sincerely apologize for this error. I've verified that you canceled on Feb 28th, but our billing system processed the March charge before the cancellation took effect. I've issued a full refund of $149 and confirmed your cancellation. You'll see the refund in 3-5 business days.",
                "category": CategoryEnum.REFUND,
                "response_time_ms": 1580,
                "timestamp": datetime.utcnow() - timedelta(days=5, hours=15)
            },
            {
                "user_message": "The service has been down for 3 days. I want a partial refund for this month.",
                "bot_response": "I'm very sorry for the service disruption you experienced. I've reviewed the outage logs and confirmed the 3-day downtime. I've applied a prorated credit of $15 to your account, representing the downtime period. This will automatically apply to your next invoice. Thank you for your patience.",
                "category": CategoryEnum.REFUND,
                "response_time_ms": 1720,
                "timestamp": datetime.utcnow() - timedelta(days=4, hours=7)
            },
            {
                "user_message": "I paid for the annual plan but only used it for 2 months. Can I get a refund for the unused time?",
                "bot_response": "I understand your situation. While our annual plans are typically non-refundable, I can make an exception here. I've calculated the prorated refund for 10 unused months ($658) and submitted it for processing. You should receive this within 7-10 business days. Your access will continue until the end of your current billing period.",
                "category": CategoryEnum.REFUND,
                "response_time_ms": 2100,
                "timestamp": datetime.utcnow() - timedelta(days=1, hours=18)
            },

            # Account Access (4)
            {
                "user_message": "I can't log in. It says my password is incorrect but I'm using the right one.",
                "bot_response": "Let me help you regain access. It looks like there were 5 failed login attempts from your account, which triggered our security lock. I've just unlocked your account. Please try logging in again. If you still have issues, use the 'Forgot Password' link to reset your password. For security, I recommend enabling 2FA.",
                "category": CategoryEnum.ACCOUNT_ACCESS,
                "response_time_ms": 1180,
                "timestamp": datetime.utcnow() - timedelta(days=6, hours=12)
            },
            {
                "user_message": "I'm not receiving the 2FA codes to my email. I'm completely locked out.",
                "bot_response": "I can help with this. I see the verification emails are being sent to j***@gmail.com. Please check your spam folder. If they're not there, I can temporarily disable 2FA so you can log in and update your email address. Reply with 'disable 2FA' and I'll process this immediately for you.",
                "category": CategoryEnum.ACCOUNT_ACCESS,
                "response_time_ms": 1450,
                "timestamp": datetime.utcnow() - timedelta(days=5, hours=20)
            },
            {
                "user_message": "My account shows as suspended but I paid my invoice last week.",
                "bot_response": "I apologize for the confusion. I've checked your payment records and confirmed your payment of $79 was received on Feb 28th. There was a delay in our payment processing system updating your account status. I've manually reactivated your account and it's now fully active. You should have immediate access.",
                "category": CategoryEnum.ACCOUNT_ACCESS,
                "response_time_ms": 1290,
                "timestamp": datetime.utcnow() - timedelta(days=3, hours=14)
            },
            {
                "user_message": "I forgot my password and the reset email isn't coming through.",
                "bot_response": "I can assist with that. Password reset emails are sent from noreply@billflow.com. Please check your spam folder and add this address to your contacts. I've just triggered a new password reset email. If you don't see it in 5 minutes, reply here and I'll help you through an alternative verification process.",
                "category": CategoryEnum.ACCOUNT_ACCESS,
                "response_time_ms": 1020,
                "timestamp": datetime.utcnow() - timedelta(days=2, hours=11)
            },

            # Cancellation (3)
            {
                "user_message": "I need to cancel my subscription. How do I do that?",
                "bot_response": "I can help you with that. To cancel, go to Settings > Subscription > Cancel Plan. You'll retain access until the end of your current billing period (March 31st). Before you go, is there anything I can help with? We also offer a pause option if you need a temporary break.",
                "category": CategoryEnum.CANCELLATION,
                "response_time_ms": 1150,
                "timestamp": datetime.utcnow() - timedelta(days=6, hours=9)
            },
            {
                "user_message": "Can I downgrade from Business to Pro instead of canceling completely?",
                "bot_response": "Absolutely! Downgrading is a great option. Go to Settings > Subscription > Change Plan and select the Pro plan ($49/month). The change takes effect at your next billing cycle on March 15th. You'll keep all Business features until then. Your data and settings will transfer seamlessly.",
                "category": CategoryEnum.CANCELLATION,
                "response_time_ms": 1380,
                "timestamp": datetime.utcnow() - timedelta(days=4, hours=13)
            },
            {
                "user_message": "I canceled yesterday but I'm still being charged. Please stop all billing immediately.",
                "bot_response": "I've reviewed your account and confirmed your cancellation request from March 4th. Your subscription is set to end on March 31st (end of current billing period), and no future charges are scheduled. You won't be billed again. The current charge is for the active period you're using through March 31st.",
                "category": CategoryEnum.CANCELLATION,
                "response_time_ms": 1520,
                "timestamp": datetime.utcnow() - timedelta(days=1, hours=10)
            },

            # General Inquiry (4)
            {
                "user_message": "Do you have an API for integrating with our accounting software?",
                "bot_response": "Yes! We offer a comprehensive REST API available on Business and Enterprise plans. It includes endpoints for invoices, subscriptions, customers, and webhooks. You can find complete documentation at docs.billflow.com/api. If you're on a Pro plan, you can upgrade to access the API. Need help getting started?",
                "category": CategoryEnum.GENERAL_INQUIRY,
                "response_time_ms": 1240,
                "timestamp": datetime.utcnow() - timedelta(days=6, hours=17)
            },
            {
                "user_message": "What's the difference between the Pro and Business plans?",
                "bot_response": "Great question! Pro ($49/month) includes up to 1,000 transactions, basic reporting, and email support. Business ($79/month) adds unlimited transactions, API access, advanced analytics, priority support, and custom branding. Most growing companies find Business better for scaling. Would you like a detailed feature comparison?",
                "category": CategoryEnum.GENERAL_INQUIRY,
                "response_time_ms": 1100,
                "timestamp": datetime.utcnow() - timedelta(days=5, hours=12)
            },
            {
                "user_message": "Can I export all my customer data to CSV?",
                "bot_response": "Yes, you can export customer data, invoices, and transaction history to CSV. Go to Reports > Export Data, select the data type and date range, then click Export. The CSV file will be emailed to you within a few minutes. Enterprise plans also support automated scheduled exports. Let me know if you need help with this!",
                "category": CategoryEnum.GENERAL_INQUIRY,
                "response_time_ms": 980,
                "timestamp": datetime.utcnow() - timedelta(days=3, hours=8)
            },
            {
                "user_message": "How do I add more team members to my account?",
                "bot_response": "To add team members, go to Settings > Team > Invite Members. Enter their email addresses and select their role (Admin, Member, or Billing Only). They'll receive an invitation email to create their account. Pro plans include 3 team members, Business includes 10, and Enterprise is unlimited. You currently have 2/3 seats used.",
                "category": CategoryEnum.GENERAL_INQUIRY,
                "response_time_ms": 1320,
                "timestamp": datetime.utcnow() - timedelta(days=1, hours=15)
            },
        ]

        # Insert all traces
        for trace_data in traces:
            trace = Trace(**trace_data)
            session.add(trace)

        await session.commit()
        print(f"Successfully seeded {len(traces)} traces into the database.")

