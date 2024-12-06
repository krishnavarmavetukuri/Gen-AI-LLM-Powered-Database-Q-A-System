import streamlit as st
from langchain_helper import get_few_shot_db_chain
from few_shots import few_shots
import time

keywords = [
    "tshirts",
    "t shirts",
    "T-shirts",
    "t-shirts",
    "shirts",
    "shirt",
    "tshirt id" ,"brand", 'Van Huesen', 'Levi', 'Nike', 'Adidas' ,
    "color", 'Red', 'Blue', 'Black', 'White',
    "size",
    "sizes",
    "colors",
    "colours",
    "colour",
    "price" ,
    "prices" ,
    "stock", "quantity" ,
    "brand", "color", "size",
    "discounts",
    "discount",
    "discount id",
    "tshirt",
    "pct", "discount" ,
    "Populate TShirts"
]

def is_valid_question(question):
    question_lower = question.lower() # Convert question to lowercase for case-insensitive check
    for keyword in keywords:
        if keyword.lower() in question_lower:
            return True
    return False

def main():
    st.title("Krishna T Shirts: Database Q&A")

    option = st.radio("Select an option:", ("Type a Question", "Select from Existing Questions"))

    if option == "Type a Question":
        question = st.text_input("Enter your question:")
        if st.button("Ask"):
            if question:
                st.header("Question")
                st.write(question)
                if is_valid_question(question):
                    valid_message = 0 #st.info("")
                else:
                    st.warning("""Invalid question. Please include one of the keywords:""")
                    st.warning("""
                                "tshirts",
                                "tshirt id" ,"brand", 'Van Huesen', 'Levi', 'Nike', 'Adidas', 
                                "color", 'Red', 'Blue', 'Black', 'White', 
                                "size", 
                                "price", 
                                "stock quantity", 
                                "brand color size", "brand", "color", "size", 
                                "discounts", 
                                "discount id",     
                                "tshirt id", 
                                "pct discount",     
                                "PopulateTShirts"
                            """)
                    return
                # Placeholder for "Answering..."
                answer_placeholder = st.empty()
                answer_placeholder.text("Answering")
                
                for i in range(1, 8):  # Change 3 to the number of seconds or half-seconds you want
                    time.sleep(0.5)  # Adjust sleep time as needed (0.5 seconds in this case)
                    answer_placeholder.text("Answering"+"."*(i%4))

                try:
                    chain, chain2 = get_few_shot_db_chain()
                    response = chain.run(question)
                    #response, sql_query = chain.run(question)
                    #response = chain(question)
                    sqlresponse = chain2.invoke({"question":question})
                    
                    #response = chain.invoke({"question":question})
                    valid_message = st.info("Valid question.")
                    # Display answer
                    st.header("Answer")
                    answer_placeholder.empty()  # Clear "Answering..." message
                    st.write(response)
                    
                    # Display SQL Query
                    st.header("SQL Query")
                    st.write(sqlresponse)
                except Exception as e:
                    #valid_message.empty()  # Clear the valid message
                    # st.warning("An error occurred: {}".format(str(e)))
                    st.warning("""Invalid question. You haven't asked the question related to the existing Tables""")
                    st.warning("""Please include one of the keywords:""")
                    st.warning("""
                                "tshirts",
                                "tshirt id", "brand", 'Van Huesen', 'Levi', 'Nike', 'Adidas', 
                                "color", 'Red', 'Blue', 'Black', 'White', 
                                "size", 
                                "price", 
                                "stock quantity", 
                                "brand color size", "brand", "color", "size", 
                                "discounts", 
                                "discount id",     
                                "tshirt id", 
                                "pct discount",     
                                "PopulateTShirts"
                            """)
                    return
    
    elif option == "Select from Existing Questions":
        selected_question = st.selectbox("Select a question:", ["Select a question"] + [shot['Question'] for shot in few_shots])
        
        if selected_question != "Select a question":  # Check if a question is selected
            if st.button("Ask"):
                # Find the selected question and get its details
                selected_shot = next((shot for shot in few_shots if shot['Question'] == selected_question), None)
                if selected_shot:
                    st.header("Question")
                    st.write(selected_shot['Question'])
                    
                    # Placeholder for "Answering..."
                    answer_placeholder = st.empty()
                    answer_placeholder.text("Answering.")

                    for i in range(3):  # Change 3 to the number of seconds or half-seconds you want
                        time.sleep(0.5)  # Adjust sleep time as needed (0.5 seconds in this case)
                        answer_placeholder.text("Answering..")

                    # Display answer
                    st.header("Answer")
                    answer_placeholder.empty()  # Clear "Answering..." message
                    st.write(selected_shot['Answer'])

                    # Display SQL Query
                    st.header("SQL Query")                
                    st.write(selected_shot['SQLQuery'])

if __name__ == "__main__":
    main()
