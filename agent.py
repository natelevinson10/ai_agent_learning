from dotenv import load_dotenv
from openai import OpenAI
import json, logging, os, sys
from scrape_menu import get_menu_categories, get_menu_category_items
from scrape_restaurants import search_restaurants
import numpy as np
import time

load_dotenv()
api_key = os.getenv('api_key')

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of the moon?"}
    ]
)

class FoodRecommendationAgent:
    def __init__(self):
        self.client = OpenAI(api_key=api_key)
        self.setup_logging()

    def setup_logging(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.log_file = os.path.join('logs', 'agent.log')
        self.file_handler = logging.FileHandler(self.log_file)
        self.file_handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def extract_search_terms(self, user_input):
        """
        Use OpenAI GPT-4o-mini to extract key context from user's food request.
        
        :param user_prompt: User's natural language food request
        :return: Dictionary with extracted search parameters cuisine_type, dish_type, and reasoning
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful shopping assistant. Your job is to read in a user's preference for what the want to order from a food delivery service. You will then extract the following information about the user's preference and return it to JSON format with quotes around strings, and so on. It should be the case that json.loads() works on your output. Follow this format: cuisine_type: [cuisine_type], dish_type: [dish_type], reasoning: [reasoning]. You will also include a reasoning key with your reasoning in the format 'I used the following logic to extract the cuisine_type, dish_type: [reasoning]'. Dishes with flavor preference adjective describing the dish should be added to the dish_type, so something like spicy chicken tikka masala should be one item ['spicy chicken tikka masala'] just as creamy quesadilla should be one item ['creamy quesadilla'] and hot wings should be one item ['hot wings']. The cuisine_type should be the most general type of food the user wants to order, and the dish_type should be the specific type of food the user wants to order. If there is no specific cuisine_type, then it should be inferred from the dish_type (i.e. if the user says they want curry, the cuisine_type should be Indian). If there is no specific dish_type, leave the field as an empty list. An example input and output is: input: 'I want to eat some Chinese food. Maybe some dim sum and a plate of sweet general tso's chicken.' output: {'cuisine_type': 'Chinese', 'dish_type': ['dim sum', ('sweet', 'general tso's chicken')], 'reasoning': '...'}"},
                    {"role": "user", "content": f"Extract the main and secondary search terms from the following user input: {user_input}"}
                ]
            )
            #log the output, user input, and the reasoning given by the AI
            self.logger.info(f"User input: {user_input}")
            self.logger.info(f"AI output: {response.choices[0].message.content.strip()}")
            #parse the output into a dictionary
            output = response.choices[0].message.content.strip()
            output_dict = json.loads(output)
            return output_dict
        except Exception as e:
            self.logger.error(f"Error extracting search terms: {e}")
            return None
    
    def get_restaurants(self, cuisine_type):
        """
        Get the restaurants for a given cuisine_type AKA search query.
        
        :param cuisine_type: The cuisine_type of the restaurant
        :return: A list of restaurants with their title, action URL, and rating
        """

        #search for restaurants on ubereats
        restaurants = search_restaurants(cuisine_type)
        return restaurants

    def get_menu_items(self, store_uuid, store_url):
        """
        Get the menu items for a given store.
        
        :param store_uuid: The UUID of the store
        :param store_url: The URL of the store
        """
        menu_categories = get_menu_categories(store_uuid, store_url)
        menu_items = get_menu_category_items(store_uuid, menu_categories[1], store_url, menu_categories[0])
        return menu_items


    def check_menu_similarity(self, menu_items, context):
        """
        Check the similarity between the menu items and the context using gpt-4o-mini.
        
        :param menu_items: A list of strings, each representing a menu item and its description
        :param context: A string representing the user's dish_type request
        :return: A list of menu items and their similarity scores
        """
        #create a list of menu items and their descriptions
        menu_items_list = [f"{item}: {menu_items[item]}" for item in menu_items]

        context_list = [context]
       
        #check the similarity between the menu items and the context
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful shopping assistant. Your job is to check if a given menu contains items that are given to you labeled as context. The menu is in the form of a list of 'item: description' and the context a list of strings. Closely examine the menu items and return a list of lists [context, menu_item] items that are most similar. For an input like 'burger', anything that mentions any form of burger should be included in the output. This includes things like 'Kid's Cheeseburger' or 'Double Double Burger'. For something like 'Soda', anything that mentions soda should be included in the output. The general rule you must follow is the words do not have to be an exact match, but you must use critical thinking to determine if the item is similar to the context. Buffalo wings are similar to normal wings, a hoagie is similar to a sandwich, etc. This includes things like 'Coke' or 'Diet Coke' for soda. You can be lenient and cross into grey areas to match context to menu items, and include any and all items on the menu that fit this criteria. However, don't be careless - a chicken sandwich is not similar to a cheese burger even though they are both sandwiches - take note of relations like this as well when making decisions. If there are no items that are similar to the context, return an empty list. The output should be in the form of a list of strings, each representing a menu item. An example input and output is: input: 'Menu items: ['cheeseburger: a burger with a bun, cheese, and a patty'] Context: ['burger']' output: ('cheeseburger: a burger with a bun, cheese, and a patty', 'burger'). Please ensure that if there is a description of the menu item, it should be included in the output. you MUST ensure the output contains the menu item and the initial user's context item. Like if the user only wants 2 items and only 1 is found, this should not satisy the user. But if they want 5 and only 4 are found, this will be good. Please include all instances of your findings in JSON format under a ['results'] key. Then under a ['reasoning'] key explain your reasoning for your decisions. the JSON format with quotes around strings, and so on. It should be the case that json.loads() works on your output."},                                          {"role": "user", "content": f"Menu items: {menu_items_list} Context: {context_list}"}
                ]
            )
            #log the output, user input, and the reasoning given by the AI
            self.logger.info(f"AI output: {response.choices[0].message.content.strip()}")
            #parse the output into a dictionary
            output = response.choices[0].message.content.strip().replace('```json', '').replace('```', '').strip()
            output_dict = json.loads(output)
            return output_dict

        except Exception as e:
            self.logger.error(f"Error extracting search terms: {e}")
            return None
    
    def summarize_menu_findings(self, similarities):
        """
        Summarize the menu findings.
        
        :param similarities: A list of tuples (context, menu_item)
        :return: A string summarizing the menu findings
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful shopping analyst, working on a project finding how good a menu is for a given context. Your job is to take in a list with two entries on each index. The first entry will be a menu and sometimes a description of the menu item in form item: description. The second entry will be a context item, which is a user's input that was matched to appear on the menu. Your job is to summarize the findings, and provide an overall sentiment about how close the menu items are to the user's context. For example, if the user's context is 'chicken sandwich', and the menu item is 'BBQ chicken sandwich: a chicken breast with a bun, cheese, and a patty, and BBQ sauce' and you should take note that the user did not specift BBQ, but it is still on the menu item, and add this to the output.  Another example is if the user's context item is 'steak fajita' and the actual menu item is 'chicken fajita: cheese and chicken in a fajita' take note that the user wanted steak but the menu has chicken, this counts too. I would like you to do this for each pair in the list you are given and create an overall sentiment. Something like, 'This menu has both items you are looking for! However, you may have to settle for chicken fajitas instead of steak. And if you like BBQ on your chicken sandwiches, then there is no problem!'. This sentiment should be output in a [sentiment] = (sentiment here). You must remember that it is okay if the menu does not have everything exactly right - it just has to have a similar enough selection to what the user wants. It is okay if they have chicken chow mein but not beef, as long as the other items are close matches as well meaning the user can find almost exactly what they want. Use judgement here to come to a reasonable conclusion whether or not the user would be able to work around it - still you must ensure the user's needs can be met given the menu. Then please include the reasoning for your output in the format 'I used the following logic to extract the menu items: [reasoning]'. If the overall sentiment is negative, or good but not good enough to satisfy all or most of the user's context, then the word 'OMIT' must be at the end of the sentiment. If the sentiment is positive and will satisfy the user, you must include the word 'CONFIRMED' at the end of your sentiment. Your output should be in JSON format with quotes around strings, and so on. It should be the case that json.loads() works on your output."},                     
                    {"role": "user", "content": f"Similarities: {similarities}"}
                ]
            )
            #log the output, user input, and the reasoning given by the AI
            self.logger.info(f"AI output: {response.choices[0].message.content.strip()}")
            #parse the output into a dictionary
            output = response.choices[0].message.content.strip().replace('```json', '').replace('```', '').strip()
            output_dict = json.loads(output)
            return output_dict

        except Exception as e:
            self.logger.error(f"Error extracting search terms: {e}")
            return None

    def chat_bot(self, user_input):
        """
        Chat with the user.
        
        :param user_input: The user's input
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful shopping assistant."},
                {"role": "user", "content": user_input}
            ]
        )   
        return response.choices[0].message.content.strip()
    


    def generate_conversational_response(self, context):
        """
        Generate a conversational response based on the context.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a friendly, helpful food delivery chatbot. Respond to the user's request in a warm, engaging manner. Add some personality and humor, but keep the response concise and focused on helping the user find their perfect meal."},
                    {"role": "user", "content": f"Help me find a great {context} to eat"}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Error generating conversational response: {e}")
            return "I'm having trouble understanding your request. Could you tell me more about what you'd like to eat?"

    def run_chatbot(self):
        """
        Run the interactive chatbot.
        """
        print("🍽️ Welcome to the Food Recommendation Chatbot! 🍔")
        print("What are you in the mood for today?")

        while True:
            # Get user input
            user_input = input("\n> ").strip()
            
            # Check for exit
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Thanks for chatting! Enjoy your meal!")
                break

            # Generate a friendly conversational response
            print("\n🤖 Let me help you find something delicious!")
            time.sleep(1)

            # Extract search terms
            user_specs = self.extract_search_terms(user_input)
            
            if user_specs is None:
                print("🤔 I'm having trouble understanding your request. Could you be more specific?")
                continue

            cuisine_type = user_specs['cuisine_type']
            dish_type = user_specs['dish_type']

            # Find restaurants
            print(f"\n🔍 Searching for {cuisine_type} restaurants...")
            print("key words: ", dish_type, "\n")
            time.sleep(1)
            restaurants = self.get_restaurants(cuisine_type)

            # Track found matches
            matches_found = False

            # Search through restaurants
            print(f"\n🍽️ Checking stores near you...")
            for i in range(0, min(50, len(restaurants))):  # Limit to first 50 restaurants
                try:
                    store = list(restaurants.keys())[i]
                    time.sleep(0.5)

                    # Get menu items
                    menu_items = self.get_menu_items(restaurants[store][1], restaurants[store][0])
                    
                    # Check menu similarity
                    output_dict = self.check_menu_similarity(menu_items, dish_type)
                    
                    if output_dict is None:
                        continue

                    # Summarize findings
                    final_output = self.summarize_menu_findings(output_dict)
                    
                    if final_output is None:
                        continue

                    # Check if restaurant is a good match
                    if 'CONFIRMED' in final_output['sentiment']:
                        matches_found = True
                        print(f"\n🎉 Great news! We found a match at {store}!")
                        print(f"🍽️ {final_output['sentiment'].replace('OMIT', '').replace('CONFIRMED', '')}")
                        
                        print("\nMatching Menu Items:")
                        for item in output_dict['results']:
                            print("👉 ", item.split(':')[0])
                        time.sleep(2.5)
                        break  # Exit the loop after the first confirmed match
                        
                except Exception as e:
                    self.logger.error(f"Error checking restaurant {i}: {e}")
            
            if not matches_found:
                print("😕 Sorry, no matching items were found. Would you like to try again?")
                continue_search = input("Do you want to continue searching for a restaurant?").lower()
                if continue_search not in ['yes', 'y']:
                    print("Thanks for chatting! Enjoy your meal!")
                    break


def main():
    agent = FoodRecommendationAgent()
    agent.run_chatbot()
    # user_specs = agent.extract_search_terms("For lunch, I want to eat some Indian food. Maybe some chicken tikka masala and a plate of naan.")
    # cuisine_type = user_specs['cuisine_type']
    # dish_type = user_specs['dish_type']


    # restaurants = agent.get_restaurants(cuisine_type)
    # for i in range(3, 7):
    #     store = list(restaurants.keys())[i]
    #     menu_items = agent.get_menu_items(restaurants[store][1], restaurants[store][0])
    #     output_dict = agent.check_menu_similarity(menu_items, dish_type)
    #     final_output = agent.summarize_menu_findings(output_dict)
    #     if 'CONFIRMED' in final_output['sentiment']:
    #         #exlucde omit and confirmed from the output
    #         print(f"{store} - {final_output['sentiment'].replace('OMIT', '').replace('CONFIRMED', '')}")
    #         items = [item[0].split(':')[0] for item in output_dict['results']]
    #         print("Some items on the menu you may like:")
    #         for item in items:
    #             print(item)
        
        


if __name__ == "__main__":
    main()
