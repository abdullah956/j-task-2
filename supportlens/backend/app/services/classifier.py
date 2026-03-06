from app.services.llm import GroqClient


CLASSIFIER_SYSTEM_PROMPT = """You are a support ticket classifier for a SaaS billing platform.
Classify the conversation into exactly one category.

Categories:
- Billing: invoices, charges, payment methods, pricing, subscription fees
- Refund: return product, get money back, dispute a charge, process a credit
- Account Access: login issues, password reset, locked account, MFA problems
- Cancellation: cancel subscription, downgrade plan, close account
- General Inquiry: feature questions, product info, how-to, anything else

Rules:
1. Return ONLY the category name. Nothing else. No punctuation.
2. If multiple categories apply, pick the PRIMARY intent.
   'I want to cancel and get a refund' → Refund
   'I was charged twice, should I cancel?' → Billing
3. Never return anything outside the five category names."""


VALID_CATEGORIES = {
    "Billing",
    "Refund",
    "Account Access",
    "Cancellation",
    "General Inquiry"
}


async def classify_trace(user_message: str, bot_response: str) -> str:
    """
    Classify a support conversation into a category.

    Args:
        user_message: The customer's message
        bot_response: The support agent's response

    Returns:
        str: The classified category name
    """
    groq_client = GroqClient()

    classifier_prompt = f"Customer: {user_message}\nSupport: {bot_response}\nClassify:"

    category, _ = await groq_client.chat_complete(
        system_prompt=CLASSIFIER_SYSTEM_PROMPT,
        user_message=classifier_prompt
    )

    # Validate the response
    if category not in VALID_CATEGORIES:
        print(f"Warning: Invalid category '{category}' returned by classifier. Defaulting to 'General Inquiry'.")
        return "General Inquiry"

    return category
