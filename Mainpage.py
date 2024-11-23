import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

# Function for Fraud Detection page
def fraud_detection_page():
    # Set the title of the app
    st.write("# Credit Card Fraud Detection")

    # Sidebar for user input
    st.sidebar.header('Input Credit Card Details')

    # CSV file upload
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=['csv'])
    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
        # Ensure input matches expected features
        input_df = input_df.drop(['Time', 'Class'], axis=1, errors='ignore')
    else:
        def user_input():
            # Create sliders for features
            V_features = {f'V{i}': st.sidebar.slider(f'V{i}', -5.0, 1.5, 5.0) for i in range(1, 29)}
            Amount = st.sidebar.number_input('Amount')

            data = {**V_features, 'Amount': Amount}
            features = pd.DataFrame(data, index=[0])
            return features

        input_df = user_input()

    # Display input data
    st.subheader('Credit Card Data')
    st.write(input_df)

    # Standardize the input data
    scaler = StandardScaler()
    input_df_scaled = scaler.fit_transform(input_df)

    # Load saved machine learning model
    try:
        load_clf = joblib.load('model.joblib')

        # Apply the model to make predictions
        prediction = load_clf.predict(input_df_scaled)
        prediction_probability = load_clf.predict_proba(input_df_scaled)

        # Display prediction
        st.subheader('Prediction')
        if prediction[0] == 0:
            st.write("Genuine Transaction")
        else:
            st.write("Fraudulent Transaction")

        # Display prediction probability
        st.subheader('Prediction Probability')
        st.write(prediction_probability)

    except FileNotFoundError as e:
        st.error("Model file not found. Please ensure the model is saved at 'model.joblib'.")
    except ValueError as e:
        st.error(f"An error occurred: {e}")


# Function for Login page with some decorations
def login_page():
    # Set the title for the login page with some decoration
    st.markdown("""
    <style>
        .title {
            font-size: 36px;
            color: #4CAF50;
            text-align: center;
        }
        .input-box {
            width: 80%;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .login-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .login-button:hover {
            background-color: #45a049;
        }
        .signup-button {
            background-color: #2196F3;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .signup-button:hover {
            background-color: #1976D2;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="title">Login Page</p>', unsafe_allow_html=True)

    # User input for login credentials
    username = st.text_input("Enter your username", key="username", placeholder="Username", label_visibility="collapsed", help="Please enter your username.")
    password = st.text_input("Enter your password", type="password", key="password", placeholder="Password", label_visibility="collapsed", help="Please enter your password.")

    # Styling the input fields with CSS
    st.markdown('<div class="input-box"></div>', unsafe_allow_html=True)

    # Button to submit login details
    login_button = st.button("Login", key="login", help="Click to login")

    # Button to navigate to the signup page
    signup_button = st.button("Sign Up", key="signup", help="Click to sign up")

    # Button logic
    if login_button:
        # For this example, we don't check credentials, just redirect to the fraud detection page
        st.session_state.page = "fraud_detection"  # Navigate to fraud detection page

    if signup_button:
        # Redirect to signup page
        st.session_state.page = "signup"  # Navigate to signup page


# Function for Signup page (No Functionality - Just a Static Form)
def signup_page():
    # Set the title for the signup page
    st.title("Sign Up Page")

    # Static text to let the user know how to sign up
    st.markdown("""
    <style>
        .sign-up-text {
            font-size: 20px;
            text-align: center;
            color: #4CAF50;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sign-up-text">Enter your details to Sign Up.</p>', unsafe_allow_html=True)
    
    # User input for new account (No button, just a form)
    new_username = st.text_input("Choose a username", placeholder="Enter your username")
    new_password = st.text_input("Choose a password", type="password", placeholder="Enter your password")
    new_password1 = st.text_input("Confirm your password", type="password", placeholder="Enter your password")
    # You can add more fields like Email, etc. if required.
    if new_password !=new_password1:
        st.success("please enter correct detainls.")
    # Instructions for users
    st.info("This page is just for creating a new account")
    Createaccount_button = st.button("Create Account", key="createaccount", help="Click to create account")
    if Createaccount_button:
        st.success("Account created Successfully.")


# Function for logout
def logout():
    # Logout the user by clearing session state
    if st.button('Logout'):
        st.session_state.clear()  # Clear session state
        st.session_state.page = "login"  # Redirect to login page
        st.success("You have been logged out.")


# Main function to control the page flow
def app():
    # Initialize session state variables
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    
    # If on login page, show login page
    if st.session_state.page == "login":
        login_page()

    # If on signup page, show signup page
    elif st.session_state.page == "signup":
        signup_page()

    # If logged in, go to fraud detection page
    elif st.session_state.page == "fraud_detection":
        fraud_detection_page()
        logout()  # Show logout button after fraud detection


# Run the app
if __name__ == "__main__":
    app()
