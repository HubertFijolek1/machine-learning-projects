import os
import random
import string
import json
from faker import Faker

# Initialize Faker for realistic data generation
fake = Faker()

# Define the folder structure
BASE_PATH = "../data"
TEMPLATES_PATH = os.path.join(BASE_PATH, "templates_json")
HAM_PATH = os.path.join(BASE_PATH, "ham")
SPAM_PATH = os.path.join(BASE_PATH, "spam")

spam_template_file = os.path.join(TEMPLATES_PATH, "spam_templates.json")
ham_template_file = os.path.join(TEMPLATES_PATH, "ham_templates.json")

print(f"HAM_PATH: {HAM_PATH}")
print(f"SPAM_PATH: {SPAM_PATH}")

# Create directories if they don't exist
os.makedirs(HAM_PATH, exist_ok=True)
os.makedirs(SPAM_PATH, exist_ok=True)


# -----------------------------
# FUNCTIONS FOR EMAIL GENERATION
# -----------------------------

def generate_code(length=10):
    """Generates a random alphanumeric code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def introduce_typos(text, typo_prob=0.03):
    """
    Introduces minor typos into the text with a given probability.
    Default typo probability is 3%.
    """
    new_text = []
    for char in text:
        if random.random() < typo_prob and char.isalpha():
            # Replace the character with a random letter
            new_char = random.choice(string.ascii_letters)
            new_text.append(new_char)
        else:
            new_text.append(char)
    return ''.join(new_text)


def load_templates(file_path):
    """
    Loads email templates from a JSON file.

    Args:
        file_path (str): Path to the JSON template file.

    Returns:
        list: List of template dictionaries with 'subject' and 'body'.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            templates = json.load(f)
        return templates
    except FileNotFoundError:
        print(f"Template file not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the template file: {file_path}")
        return []


def generate_messages(templates, num_messages, is_spam=True):
    """
    Generates a list of email messages based on provided templates.

    Args:
        templates (list): List of template dictionaries with 'subject' and 'body'.
        num_messages (int): Number of messages to generate.
        is_spam (bool): Indicates if the messages are spam (True) or ham (False).

    Returns:
        list: List of generated email messages as strings.
    """
    messages = []
    for _ in range(num_messages):
        template = random.choice(templates)

        # Generate subject
        subject = template["subject"].format(
            name=fake.first_name(),
            item=random.choice(["iPhone 14", "100 USD Gift Card", "Laptop", "Gift Card", "SmartWatch"]),
            discount=random.randint(5, 80),
            code=generate_code(),
            url=fake.url(),
            expiry_date=fake.date_between(start_date='today', end_date='+30d'),
            company=random.choice(["TechCorp", "ShopEasy", "SafeBank", "PromoMax", "BizSolutions"]),
            time=fake.time(pattern="%H:%M"),
            deadline=fake.date_between(start_date='today', end_date='+10d'),
            sender_name=fake.name()
        )

        # Generate body
        body_lines = []
        for line in template["body"]:
            filled_line = line.format(
                name=fake.first_name(),
                item=random.choice(["iPhone 14", "100 USD Gift Card", "Laptop", "Gift Card", "SmartWatch"]),
                discount=random.randint(5, 80),
                code=generate_code(),
                url=fake.url(),
                expiry_date=fake.date_between(start_date='today', end_date='+30d'),
                company=random.choice(["TechCorp", "ShopEasy", "SafeBank", "PromoMax", "BizSolutions"]),
                time=fake.time(pattern="%H:%M"),
                deadline=fake.date_between(start_date='today', end_date='+10d'),
                sender_name=fake.name()
            )
            body_lines.append(filled_line)

        # Construct the full email
        email_content = (
                f"From: {fake.email()}\n"
                f"To: {fake.email()}\n"
                f"Subject: {subject}\n"
                f"Date: {fake.date_time_this_year()}\n\n"
                + "\n".join(body_lines)
        )

        # Introduce typos if the email is ham
        if not is_spam:
            email_content = introduce_typos(email_content, typo_prob=0.02)

        messages.append(email_content)

    return messages


# -----------------------------
# MAIN FUNCTION TO GENERATE AND SAVE EMAILS
# -----------------------------

def main():
    # Paths to template files
    spam_template_file = os.path.join(TEMPLATES_PATH, "spam_templates.json")
    ham_template_file = os.path.join(TEMPLATES_PATH, "ham_templates.json")

    # Load templates
    spam_templates = load_templates(spam_template_file)
    ham_templates = load_templates(ham_template_file)

    if not spam_templates:
        print("No spam templates loaded. Exiting.")
        return
    if not ham_templates:
        print("No ham templates loaded. Exiting.")
        return

    # Define the number of emails to generate
    num_spam = 100
    num_ham = 100

    # Generate spam and ham emails
    print("Generating spam emails...")
    spam_emails = generate_messages(spam_templates, num_spam, is_spam=True)
    print("Generating ham emails...")
    ham_emails = generate_messages(ham_templates, num_ham, is_spam=False)

    # Save ham emails as individual files
    print(f"Saving ham emails to '{HAM_PATH}' directory...")
    for i, email in enumerate(ham_emails, 1):
        file_path = os.path.join(HAM_PATH, f"ham{i}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(email)

    # Save spam emails as individual files
    print(f"Saving spam emails to '{SPAM_PATH}' directory...")
    for i, email in enumerate(spam_emails, 1):
        file_path = os.path.join(SPAM_PATH, f"spam{i}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(email)

    print(
        "Advanced data generation completed successfully. Ham and spam emails have been saved in their respective folders.")


if __name__ == "__main__":
    main()
