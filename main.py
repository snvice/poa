import streamlit as st
import streamlit.components.v1 as components
import pickle

# Load the cost prediction model
with open('cost_model.pkl', 'rb') as f:
    cost_model = pickle.load(f)

def predict_cost(age_group, total_people, night_mainland, country, main_activity, total_female):
    # Prepare the input data for the model
    X = [[age_group, total_people, night_mainland, country, main_activity, total_female]]

    # Use the model to predict the cost
    predicted_cost = cost_model.predict(X)[0]

    # Ensure total cost is within the desired range
    predicted_cost = max(50000, min(130000, predicted_cost))

    return int(predicted_cost)

def main():
    st.set_page_config(page_title="Travel Cost Calculator", page_icon=":money_with_wings:", layout="wide")

    # Add background image
    page_bg_img = """
    <style>
    body {
    background-image: url("https://example.com/background.jpg");
    background-size: cover;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Create sidebar menu
    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                # st.image("https://example.com/logo.png", width=150)
                st.image("https://github.com/snvice/poa/blob/main/tourist.jpg", width=150)
            with col2:
                st.title("Travel Cost Calculator")
                st.write("Welcome! Let's estimate the cost of your upcoming adventure.")

        with st.container():
            st.header("Trip Details")
            col1, col2 = st.columns(2)

            with col1:
                countries = ['Kenya', 'USA', 'UK', 'Italy', 'South Africa']
                country = st.radio("Which country are you visiting?", options=countries, key="country", horizontal=True)

                age_options = ['Youth (Below 18)', 'Adult (18-64)', 'Senior (65+)']
                age_group = st.radio("Select your age group", options=age_options, key="age_group", horizontal=True)

                activities = ['Beach', 'Safari', 'City Tour', 'Hiking', 'Cultural Experience']
                main_activity = st.radio("What's your primary activity?", options=activities, key="activity", horizontal=True)

            with col2:
                total_male = st.number_input("How many men in your travel group?", min_value=0, value=1, step=1, key="male")
                total_female = st.number_input("How many women in your travel group?", min_value=0, value=1, step=1, key="female")
                night_mainland = st.number_input("How many nights will you stay?", min_value=1, value=3, step=1, key="nights")

        with st.container():
            st.header("Additional Information")
            first_trip = st.radio("Is this your first trip to the country?", options=['Yes', 'No'], key="first_trip")
            guided_tour = st.radio("Will you be taking a guided tour?", options=['Yes', 'No'], key="guided_tour")

        with st.container():
            submitted = st.button("Calculate Cost")

            if submitted:
                total_people = total_male + total_female
                age_group_key = age_options.index(age_group)
                age_group_value = ['youth', 'adult', 'senior'].index(age_group_key)
                country_value = countries.index(country)
                activity_value = activities.index(main_activity)
                predicted_cost = predict_cost(age_group_value, total_people, night_mainland, country_value, activity_value, total_female)
                st.success(f"The estimated cost for your trip is: Ksh {predicted_cost:,.0f}")

    elif choice == "About":
        st.header("About")
        st.write("This is a travel cost calculator app built with Streamlit. It uses a machine learning model to estimate the cost of your upcoming trip based on various factors such as age group, number of people, and duration of stay.")
        st.write("To use the calculator, simply navigate to the 'Home' page and provide the required information. The app will then use the trained model to predict and display the estimated cost of your trip.")

if __name__ == "__main__":
    main()