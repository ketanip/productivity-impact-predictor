import streamlit as st

# Loading Data
import pickle
import pandas as pd

unique_values_file = open("output\model_unique_values.pkl", "rb")
model_unique_values = pickle.load(unique_values_file)
unique_values_file.close()

model_pipeline_file = open("output\model_pipeline.pkl", "rb")
model_pipeline = pickle.load(model_pipeline_file)
model_pipeline_file.close()


st.header("Productivity Loss Predictor")
st.text(
    "This is a tool which predicts loss of your productivity due to social media based."
)


# Personal Details
# ----------------

st.markdown(
    """
----
#### Personal Details
Let us start by filling out some of your personal details. These are some broad details which help us determine a basic idea about you.
"""
)

pd1_col1, pd1_col2, pd1_col3 = st.columns(3)

with pd1_col1:
    age = st.number_input("**Age (in Years)**", min_value=16, max_value=80, step=1)

with pd1_col2:
    gender = st.selectbox("**Gender**", model_unique_values["gender"])

with pd1_col3:
    profession = st.selectbox("**Profession**", model_unique_values["profession"])


pd2_col1, pd2_col2 = st.columns(2)

with pd2_col1:
    location = st.selectbox("**Country**", model_unique_values["location"])

with pd2_col2:
    demographics = st.selectbox(
        "**Place of residence**", model_unique_values["demographics"]
    )


# ------------------
# Social Media Details
st.markdown(
"""
---
#### Social Media Usage
Now let us see how reflect on you social media usage. We suggest you use **Digital Wellbeing** to fill out the data below more accurately. As there can sometimes be a bias in out mind regarding our usage of social media.
"""
)


total_time_spent = st.number_input("**Time spent on social media each day (in minutes)**", min_value=1, step=1)

smd1, smd2 = st.columns(2)

with smd1:
    platform = st.selectbox("**Most used social media**", model_unique_values["platform"])
    
with smd2:
    watch_reason = st.selectbox(
        "**Why do you watch content ?**", model_unique_values["watch_reason"]
    )


# ------------------
# Device Details
st.markdown(
"""
---
#### Device Details
Now let us see focus on your device. It is a less realized fact that it has a lot to do with your social media usage.
"""
)

dd_col1, dd_col2 = st.columns(2)

with dd_col1:
    device_type = st.selectbox("**Device**", model_unique_values["device_type"])

with dd_col2:
    os = st.selectbox("**Operating System**", model_unique_values["os"])
connection_type = st.selectbox(
    "**Internet connection type**", model_unique_values["connection_type"]
)

# ------------------
# Other Details
st.markdown(
"""
---
#### Other Details
These are some of the other less know details that may heavily impact your social media usage and thus your productivity by it. One of phenomenon that can be used with the following data is *doom spending*.
"""
)

otd_col1, otd_col2 = st.columns(2)

with otd_col1:
    debt = st.toggle("Have active debt.")
    
with otd_col2:
    owns_property = st.toggle("Own property.")


# ------------------
# Self Awareness
st.markdown(
"""
---
#### Self Awareness
These questions require you to be very self aware and self critical while answering it. So please focus and be critical on your self while answering the following,
"""
)

addiction_level = st.number_input(
    "**How much would you rate your social media addiction ? (1-10)**", min_value=1, max_value=10, step=1
)
self_control = st.number_input(
    "***How much would you rate your self control ? (1-10)**", min_value=1, max_value=10, step=1
)


def get_prediction():
    data = {
        "age": age,
        "gender": gender,
        "profession": profession,
        "demographics": demographics,
        "location": location,
        "debt": debt,
        "owns_property": owns_property,
        "platform": platform,
        "total_time_spent": total_time_spent,
        "watch_reason": watch_reason,
        "device_type": device_type,
        "os": os,
        "connection_type": connection_type,
        "self_control": self_control,
        "addiction_level": addiction_level,
    }
    res = model_pipeline.predict(pd.DataFrame([data]))
    st.toast(
        """
        You are losing upto **{}%** of your productivity due to social media.
        """.format(float(res)*10), icon="🙄"
    )
    

st.button("Find my Loss", type="primary", on_click=get_prediction)