# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import json
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionListCourses(Action):

    def name(self) -> Text:
        return "action_list_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Load the data from the JSON file
        with open('courses.json') as f:
            data = json.load(f)

        # Get the user intent
        user_intent = tracker.latest_message['intent'].get('name')

        # Initialize a response message
        response = ""

        # Handle the request for Master's programs
        if user_intent == "request_master_programs":
            response = "Woah! I've got a Smart One today. Please specify an area of interest (e.g., Engineering / Information Technology)."
            return [SlotSet("awaiting_area_of_interest", True)]  # Set a slot to track this state

        # Check if the user specified an area of interest
        area_of_interest = tracker.get_slot("area_of_interest")
        print(area_of_interest)

        if area_of_interest:       
         filtered_programs = [
            f"{program['Program Name']} - {program['University']}"
            for program in data
            if program['Main Category'].strip() == "Masters Degree" and program['Interest Area'].lower() == area_of_interest.lower()
            ]
         print(filtered_programs)
        # Create response
        if filtered_programs:
            program_list = "\n".join(f"{i + 1}. {prog}" for i, prog in enumerate(filtered_programs))
            response = f"Here are the programs available:\n{program_list}"
        else:
            response = "Sorry, there are no programs available for that area of interest."

        dispatcher.utter_message(text=response)
        return []

class ActionShowEnrollmentInfo(Action):

    def name(self) -> str:
        return "action_show_enrollment_info"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        info_list = []
        info_url = ""

        with open('useful_info.json') as f:
            data = json.load(f)

        for entry in data:
            if entry['Sub Information'] == "Before Enrolling":
                info_list.append(entry['Data'])
                info_url = entry['Information URL']

         # Format the list to be numbered and each on a new line
        formatted_info = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(info_list)])
        
        dispatcher.utter_message(
            text=f"Congratulations on Your New Semester. Before enrolling, please make sure you have the following information:\n{formatted_info}\n\nFor more details, ({info_url})."
        )
        return []
        

class ActionShowEnrollSteps(Action):

    def name(self) -> str:
        return "action_show_enroll_steps"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        enroll_steps = []
        info_url = ""

        with open('useful_info.json') as f:
            data = json.load(f)

        for entry in data:
            if entry['Sub Information'] == "Steps To Enrol":
                enroll_steps.append(entry['Data'])
                info_url = entry['Information URL']

        formatted_steps = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(enroll_steps)])
        
        dispatcher.utter_message(
            text=f"To enroll, please follow these steps:\n{formatted_steps}\n\nFor more details, visit ({info_url})."
        )
        
        return []

class ActionShowSemesterChecklist(Action):

    def name(self) -> str:
        return "action_show_semester_checklist"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        checklist_items = []
        info_url = ""

        with open('useful_info.json') as f:
            data = json.load(f)

        for entry in data:
            if entry['Sub Information'] == "Before Semester Checklist":
                checklist_items.append(entry['Data'])
                info_url = entry['Information URL']

        # Format the checklist to be numbered and each on a new line
        formatted_checklist = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(checklist_items)])
        
        dispatcher.utter_message(
            text=(
                "I hope you have a great semester! To make it enjoyable, here are some tips and tricks to get started:\n"
                f"{formatted_checklist}\n\n"
                f"For more details, visit [this link]({info_url})."
            )
        )

        return []

class ActionFilterDataSciencePrograms(Action):

    def name(self) -> Text:
        return "action_filter_data_science_programs"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        with open('courses.json') as f:
            data = json.load(f)

        print("I am in Action Filter Data Science Program")
        # Filter for Data Science programs
        filtered_programs = [
            f"{program['Program Name']} - {program['University']}"
            for program in data
            if program['Program Name'] == "Master of Data Science"
        ]

        filtered_universities = [
            f"{program['University']}"
            for program in data
            if program['Program Name'] == "Master of Data Science"
        ]
       
        # Create response
        if filtered_programs and filtered_universities:
            program_list = "\n".join(f"{i + 1}. {prog}" for i, prog in enumerate(filtered_programs))
            university_list = "\n".join(f"{i + 1}. {prog}" for i, prog in enumerate(filtered_universities))
            
            response = f"Here are the programs available:\n{program_list}"
        else:
            response = "Sorry, there are no programs available for that area of interest."

        dispatcher.utter_message(
            text=(
                "Here are the program available:\n"
                f"{program_list}\n\n"
                f"Are you interested in exploring course details at a university? Please choose a university from the list below, and I will provide you with all the information you need! \n{university_list}"
            )
        )

        return []


class ActionGetCourseDetails(Action):

    def name(self) -> Text:
        return "action_get_course_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Load the data from the JSON file
        with open('courses.json') as f:
            data = json.load(f)

        # Get the user intent
        user_intent = tracker.latest_message['intent'].get('name')

        # Initialize a response message
        response = ""

        # Handle the request for Master's programs
        if user_intent == "ask_data_science_programs":
            return [SlotSet("awaiting_university_of_interest", True)]  # Set a slot to track this state


        RMIT_Overview ="Gain the skills to navigate huge volumes of data generated via social media, financial transactions, transportation and scientific discovery as a data scientist."

        RMIT_URL = 'https://www.rmit.edu.au/study-with-us/levels-of-study/postgraduate-study/masters-by-coursework/master-of-data-science-mc267'

        Deakin_Overview = "Become a data specialist capable of using data to form insights, support decision making and create a competitive advantage the business world."

        Deakin_URL = 'https://www.deakin.edu.au/course/master-data-science'
        # Check if the user specified an area of interest
        university_of_interest = tracker.get_slot("university_of_interest")
        print(university_of_interest)
        area_of_interest='Information Technology'
        program_name='Master of Data Science'
        if university_of_interest:       
         filtered_programs = [
            program for program in data if program['Main Category'].strip() == "Masters Degree" and program['Interest Area'].lower() == area_of_interest.lower()
            and program['University'].strip()=="RMIT University" and program['Program Name'].strip().lower() ==program_name.lower()
            ]
         print(filtered_programs)
        # Create response
        # Create response
        if filtered_programs:
            program_details = filtered_programs[0]  # Assuming only one program matches
            response = (
                f"Here are the programs available:\n"
                f"1. {program_details['Program Name']} - {program_details['University']}\n"
                f"   Course Overview - {RMIT_Overview}\n"
                f"   Credit Points - {program_details['Total Credit Points']}\n"                              
                f"   Location - {program_details['Location']}\n"
                f"   Fee - ${program_details['Internation Tuition Fee']}\n"
                f"   Course URL - {RMIT_URL}"

            )
        else:
            response = "Sorry, there are no programs available for that area of interest."

        dispatcher.utter_message(text=response)
        return []