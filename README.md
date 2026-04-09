# VipraTech Store Assignment

## Assumptions Made
* **Database:** I used the default SQLite database. As an entry-level developer, I wanted to focus my time entirely on mastering the Stripe integration and core logic rather than setting up a full PostgreSQL instance.
* **Authentication:** I used Django sessions to track user carts/orders instead of building a full user login system to keep the scope focused strictly on the assignment requirements.
* **Frontend:** I used a simple Bootstrap CDN to make the user interface clean and presentable quickly.

## Flow Chosen & Why
**Stripe Checkout Session**
I decided to implement the Stripe Checkout Session flow instead of Payment Intents. 
* **Why:** It delegates the payment UI, error handling, and security entirely to Stripe. For my current experience level, this felt like the safest and most reliable way to handle payments without risking any sensitive card data handling on my end.

## Avoiding Double Charges & Inconsistent State
* **Frontend:** I added a simple JavaScript function to disable the "Buy" button and change its text to "Redirecting..." as soon as it is clicked. This prevents impatient users from double-clicking and creating two orders.
* **Backend:** Orders are initially saved to the database with a `pending` status. When Stripe redirects the user back to the success page, I verify the `session_id` directly with Stripe's API to confirm the actual payment status before marking the order as `paid` in the database.

## Notes on Code Quality & Logic
* I used Django Class-Based Views (CBVs) and ensured `self` was used properly to maintain a clean, object-oriented structure.
* I kept the architecture separated: database tables are strictly defined in `models.py`, while the business and payment logic lives in `views.py`.

## Setup and Run Steps
1. **Clone the repository.**
2. **Create and activate a virtual environment:**
   `python -m venv venv`
   `venv\Scripts\activate` (Windows)
3. **Install required packages:**
   `pip install django stripe`
4. **Configure Stripe:**
   * Rename `.env.example` to `.env`.
   * Add your Stripe Test Secret Key. (Note: For ease of evaluation, I have temporarily left my test key hardcoded in `settings.py`).
5. **Set up the database:**
   `python manage.py makemigrations store`
   `python manage.py migrate`
6. **Populate test products:**
   `python manage.py shell -c "from store.models import Product; Product.objects.create(name='Premium Widget', price=150.00); Product.objects.create(name='Standard Widget', price=50.00)"`
7. **Start the local server:**
   `python manage.py runserver`

## Time Spent
[I spent around 4 hour here to make this assignment , where i used AI only few places like in model.py and test.py ...]