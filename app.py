import streamlit as st
import pandas as pd
import os
from datetime import datetime


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Smart Wallet Tracker",
    page_icon="💰",
    layout="wide"
)


FILE_NAME="wallet_history.xlsx"



# ==========================
# CSS THEME
# ==========================

st.markdown("""
<style>


/* BACKGROUND */

.stApp{

background:

linear-gradient(
135deg,
#020617,
#111827,
#1e1b4b
);

color:white;

}



/* LOGIN BOX */

.login-box{


background:#0f172a;


padding:50px;


border-radius:25px;


border:2px solid #6366f1;


box-shadow:

0 0 40px #4f46e5;


}



/* HEADINGS */

h1,h2,h3{

color:white !important;

}



/* INPUT LABEL TEXT */

label{


color:white !important;


font-size:18px !important;


font-weight:600;


}



/* INPUT AREA */


.stTextInput input{


background:white !important;


color:black !important;


font-size:18px;


border-radius:12px;


border:2px solid #8b5cf6;


}



.stTextInput input:focus{


border:2px solid #06b6d4;


}



/* PLACE HOLDER */


.stTextInput input::placeholder{


color:#64748b !important;


}




/* BUTTON */


.stButton button{


background:

linear-gradient(

90deg,

#7c3aed,

#06b6d4

);



color:white !important;


font-size:18px;


font-weight:bold;


border-radius:15px;


height:45px;


}



/* TAB TEXT */


button[data-baseweb="tab"]{


color:white !important;


font-size:18px;


}



</style>

""",
unsafe_allow_html=True)






# ==========================
# LOGIN SYSTEM
# ==========================


if "logged_in" not in st.session_state:

    st.session_state.logged_in=False




if not st.session_state.logged_in:



    st.markdown(
    "<h1 style='text-align:center'>💰 Smart Wallet Tracker Pro</h1>",
    unsafe_allow_html=True
    )



    st.markdown(
    "<h3 style='text-align:center;color:#38bdf8'>Manage Expenses • Save Money • Track Future</h3>",
    unsafe_allow_html=True
    )



    a,b,c=st.columns([1,2,1])



    with b:


        st.markdown(
        "<div class='login-box'>",
        unsafe_allow_html=True
        )



        tab1,tab2=st.tabs(
        [
        "🔑 SIGN IN",
        "📝 CREATE ACCOUNT"
        ]
        )



        # LOGIN

        with tab1:


            st.header("Welcome Back")



            email=st.text_input(
            "Email Address",
            key="email_login",
            placeholder="Enter your email"
            )



            password=st.text_input(
            "Password",
            type="password",
            key="pass_login",
            placeholder="Enter password"
            )



            if st.button(
            "SIGN IN",
            key="login_btn"
            ):


                if email and password:


                    st.session_state.logged_in=True


                    st.success(
                    "Login Successful"
                    )


                    st.rerun()


                else:


                    st.error(
                    "Enter email and password"
                    )





        # CREATE ACCOUNT


        with tab2:


            st.header("Create Account")



            name=st.text_input(
            "Full Name",
            key="name_signup",
            placeholder="Enter your name"
            )



            new_email=st.text_input(
            "Email Address",
            key="email_signup",
            placeholder="Enter email"
            )



            new_password=st.text_input(
            "Password",
            type="password",
            key="password_signup",
            placeholder="Create password"
            )



            if st.button(
            "CREATE ACCOUNT",
            key="create_btn"
            ):



                if name and new_email and new_password:


                    st.success(
                    "Account Created Successfully"
                    )


                else:


                    st.error(
                    "Fill all details"
                    )



        st.markdown(
        "</div>",
        unsafe_allow_html=True
        )


    st.stop()






# ==========================
# DASHBOARD
# ==========================


with st.sidebar:


    st.title("⚙ Control Panel")



    if st.button("Logout"):


        st.session_state.logged_in=False

        st.rerun()



    income=st.number_input(
    "Monthly Income",
    value=50000
    )


    food_limit=st.number_input(
    "Food Limit",
    value=8000
    )




# READ DATA


food_total=0
travel_total=0
saving=0



if os.path.exists(FILE_NAME):


    df=pd.read_excel(FILE_NAME)



    food_total=df["Food"].sum()


    travel_total=df["Travel"].sum()



    expense=df[df["Type"]=="Debit"]["Total"].sum()


    saving=income-expense






st.title(
"💰 Expense Tracker Dashboard"
)



left,right=st.columns(2)




with left:


    st.subheader(
    "➕ Add Expense"
    )



    typ=st.selectbox(
    "Transaction Type",
    [
    "Debit",
    "Credit"
    ]
    )



    date=st.date_input(
    "Date",
    datetime.now()
    )


    mode=st.selectbox(
    "Payment Mode",
    [
    "Cash",
    "UPI",
    "Bank",
    "Card"
    ]
    )



    food=st.number_input(
    "Food"
    )


    travel=st.number_input(
    "Travel"
    )


    rent=st.number_input(
    "Rent"
    )


    fun=st.number_input(
    "Fun"
    )


    total=food+travel+rent+fun



    if st.button(
    "SAVE TRANSACTION"
    ):


        data=pd.DataFrame({

        "Date":[date],

        "Type":[typ],

        "Payment":[mode],

        "Food":[food],

        "Travel":[travel],

        "Rent":[rent],

        "Fun":[fun],

        "Total":[total]

        })



        if os.path.exists(FILE_NAME):

            old=pd.read_excel(FILE_NAME)

            data=pd.concat(
            [old,data],
            ignore_index=True
            )



        data.to_excel(
        FILE_NAME,
        index=False
        )


        st.success(
        "Saved"
        )

        st.rerun()





with right:


    st.subheader(
    "📊 Analysis"
    )


    st.metric(
    "Food Expense",
    f"₹{food_total}"
    )


    st.metric(
    "Travel Expense",
    f"₹{travel_total}"
    )


    st.metric(
    "Savings",
    f"₹{saving}"
    )



    if food_total>food_limit:

        st.error(
        "Food limit exceeded"
        )






st.divider()


st.header(
"📁 History"
)



if os.path.exists(FILE_NAME):


    st.dataframe(
    pd.read_excel(FILE_NAME),
    use_container_width=True
    )


else:


    st.info(
    "No transactions yet"
    )





# AI

st.divider()

st.subheader(
"🤖 AI Expense Assistant"
)


question=st.text_input(
"Ask question",
key="ai"
)


if question:


    if "food" in question.lower():

        st.info(
        f"Food expense ₹{food_total}"
        )


    elif "saving" in question.lower():

        st.info(
        f"Savings ₹{saving}"
        )


    else:

        st.warning(
        "Ask about food or saving"
        )