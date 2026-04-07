import stripe
import streamlit as st

stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

def create_checkout_session(email):

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": st.secrets["STRIPE_PRICE_ID"],
                "quantity": 1,
            }],
            mode="subscription",  # 🔥 IMPORTANT

            customer_email=email,

            success_url=f"{st.secrets['APP_URL']}?success=true&email={email}",
            cancel_url=st.secrets["APP_URL"] + "?canceled=true",
        )

        return session.url

    except Exception as e:
        st.error("Stripe Error ❌")
        st.write(e)
        return None
