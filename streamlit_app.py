import streamlit
import pandas
import requests
from urllib.error import URLError
import snowflake.connector

def get_fruityvice_data(fruit):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
def get_fruit_load_list(my_cnx):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
    
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
        return "Thanks for adding " + new_fruit
    

streamlit.title("My parents new healthy Diner")

streamlit.header("🥣 Breakfast Menu")
streamlit.text("🥗 Omega 3 and Blueberry Oatmeal")
streamlit.text("🐔 Kale, Spinach and Rocket Smoothie")
streamlit.text("🥑🍞 Hard-Boiled Fre-Range Eggs")
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

streamlit.header("View our fruit list - Add your favorites !")
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list(my_cnx)
    my_cnx.close()
    streamlit.dataframe(my_data_rows)


add_my_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    response = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(response)
