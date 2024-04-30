import streamlit as st
import streamlit.components.v1 as components

def predict_cost(age_group, total_people, night_mainland, country, main_activity, total_female):
    # Define age group costs
    age_costs = {'youth': 0.8, 'adult': 1, 'senior': 1.3}

    # Define base cost per person per night
    base_cost = 10000

    # Country cost factor
    country_costs = {'Kenya': 1, 'USA': 1.2, 'UK': 1.5, 'Italy': 1.3, 'South Africa': 1.1}
    country_cost_factor = country_costs[country]

    # Activity cost factor
    activity_costs = {'Beach': 1, 'Safari': 1.3, 'City Tour': 1.1, 'Hiking': 1.3, 'Cultural Experience': 1.2}
    activity_cost_factor = activity_costs[main_activity]

    # Female cost factor
    female_cost_factor = 1 + (total_female * 0.05)  # 5% increase for each female traveler

    # Calculate age cost factor
    age_cost_factor = age_costs[age_group]

    # Calculate total cost
    total_cost = (base_cost * total_people * night_mainland) * age_cost_factor * country_cost_factor * activity_cost_factor * female_cost_factor

    # Ensure total cost is within the desired range
    total_cost = max(50000, min(130000, total_cost))

    return int(total_cost)

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
                age_group_value = ['youth', 'adult', 'senior'][age_group_key]
                predicted_cost = predict_cost(age_group_value, total_people, night_mainland, country, main_activity, total_female)
                st.success(f"The estimated cost for your trip is: Ksh {predicted_cost:,.0f}")

    elif choice == "About":
        st.header("About")
        st.write("This is a travel cost calculator app built with Streamlit. It helps you estimate the cost of your upcoming trip based on various factors such as age group, number of people, and duration of stay.")
        st.write("To use the calculator, simply navigate to the 'Home' page and provide the required information. The app will then calculate and display the estimated cost of your trip.")

if __name__ == "__main__":
    main()
