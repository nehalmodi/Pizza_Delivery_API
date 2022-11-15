import streamlit as st
import requests 

from order import run

st.set_page_config("Pizza Delivery", "https://static.toiimg.com/thumb/53110049.cms?width=1200&height=900", "wide")
st.write("# Pizza Delivery App")

def signup():
    username = st.text_input("Username")
    email = st.text_input("email")
    password = st.text_input("Password")
    is_staff = st.checkbox("Are you a staff",False)
    is_active = True
    if st.button("Submit") : 
        signup_response = requests.post("http://13.233.194.53:8000/auth/signup",json={"username": username,
                    "email": email,
                    "password": password,
                    "is_staff": is_staff,
                    "is_active": is_active}).json()
        if "status_code" in signup_response:
            st.error(signup_response["detail"])
        else:
            st.success("Created Successfully")

def login():
    username = st.text_input("Username", key="Login_username")
    password = st.text_input("Password",key="Login_password")
    if st.button("Login") : 
        login_response  = requests.post("http://13.233.194.53:8000/auth/login",json={
            "username" : username,
            "password" : password
        }).json()
        if "detail" in login_response:
            st.error(login_response["detail"])
        else:
            refresh_token = login_response["refresh"]
            access_token = login_response["access"]
            st.success("Logedin Successfully")
            st.session_state["access_token"] = access_token
            st.session_state["refresh_token"] = refresh_token
            st.session_state["username"] = username
            st._rerun()


is_login = False

if "access_token" in st.session_state:
    is_login = True

if not is_login:
    with st.sidebar.expander("Signup") : 
        signup()
    with st.sidebar.expander("Login") : 
        login()
else :
    if st.sidebar.button("Logout") :
        del st.session_state["access_token"]
        del st.session_state["refresh_token"]
        st._rerun()
    run()
