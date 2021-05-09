import os
from typing import Any, Text, Dict, List
import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet, EventType, SessionStarted, ActionExecuted
import pandas as pd

class ActionHi(Action):
    """The action that says hi

    It expects it's name go be defined in the environment variable: MY_NAME"""

    def name(self) -> Text:
        return "action_hi"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hi, from custom action 'action_hi' !")
        dispatcher.utter_message(text="How are you?")

        # get my name from an environment variable
        my_name = os.environ.get("MY_NAME")
        if my_name:
            dispatcher.utter_message(text=f"My name is {my_name}")
        else:
            dispatcher.utter_message(
                text=(
                    "I do not know my name, "
                    "please set it in the environment variable 'MY_NAME'"
                )
            )

        return []

class IncidentStatus(Action):

    def name(self):
        return 'action_incident_status'

    def run(self, dispatcher, tracker, domain):

        data = pd.read_csv('workshop_data.csv')
        user_id = tracker.get_slot('number')

        find_user = data.loc[data['user_id']==user_id]

        status = find_user.incident_number_status.values[0]
        email = find_user.email.values[0]

        dispatcher.utter_message("The status of your ticket is : {}".format(status))

        return [SlotSet("email",email)]
