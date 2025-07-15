# Import python packages
import streamlit as st
import pandas as pd
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

# Convert the Snowpark dataframe to Pandas dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
st.stop

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients?",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    st.write("You selected:", ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write("ingredients_string:", ingredients_string)

    #🥋 Build a SQL Insert Statement & Test It 
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order.replace("'","''") + """')"""

    # st.write(my_insert_stmt)
    # st.stop

    time_to_insert = st.button('Submit Order')

    # 🥋 Insert the Order into Snowflake
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    import requests

    if ingredients_list:
        ingredients_string = ''
        
        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '
            st.subheader(fruit_chosen + ' Nutritional Information')
            smoothiefroot_response = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_chosen)
            sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
