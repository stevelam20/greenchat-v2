import yaml
import pathlib
import logging
import pandas as pd
import time
import datetime as dt
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet, EventType, SessionStarted, ActionExecuted, ReminderScheduled
from typing import Any, Text, Dict, List, Optional
from rasa_sdk.forms import FormAction
from rasa_sdk.types import DomainDict



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


class ActionAskName(Action):
    """The action that says hi

    It expects it's name go be defined in the environment variable: MY_NAME"""

    def name(self):
        return 'action_name_form'

    def run(self, dispatcher, tracker, domain):

        name = tracker.get_slot('name')
        dispatcher.utter_message("Hi, {} how are you doing?".format(name))
        dispatcher.utter_message("How may i help you today?")

        return[SlotSet("name",name)]

class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:


        date = dt.datetime.now() + dt.timedelta(seconds=10)


        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date
        )

        return [reminder]


class ActionBoosterStory1(Action):


    def name(self):
        return 'action_booster_story1'

    def run(self, dispatcher, tracker, domain):

        date5 = dt.datetime.now() + dt.timedelta(seconds=5)

        date10 = dt.datetime.now() + dt.timedelta(seconds=10)

        dispatcher.utter_message("BOOSTER PUMP SETUP INSPECTION")
        dispatcher.utter_message(template="utter_booster_pump_setup_1")
        dispatcher.utter_message(template="utter_booster_pump_setup_2")
        dispatcher.utter_message(template="utter_booster_pump_setup_3")
        dispatcher.utter_message(template="utter_booster_pump_setup_4")
        dispatcher.utter_message(template="utter_booster_pump_setup_5")

        return []

class AskTime(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")

        return[]

##Asking For Names

names = pathlib.Path("data/names.txt").read_text().split("\n")


class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        first_name = tracker.slots.get("first_name")
        if first_name is not None:
            if first_name not in names:
                return ["name_spelled_correctly"] + slots_mapped_in_domain
        return slots_mapped_in_domain

    async def extract_name_spelled_correctly(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        intent = tracker.get_intent_of_latest_message()
        return {"name_spelled_correctly": intent == "affirm"}

    def validate_name_spelled_correctly(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""
        if tracker.get_slot("name_spelled_correctly"):
            return {"first_name": tracker.get_slot("first_name"), "name_spelled_correctly": True}
        return {"first_name": None, "name_spelled_correctly": None}

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""

        # If the name is super short, it might be wrong.
        print(f"First name given = {slot_value} length = {len(slot_value)}")
        if len(slot_value) <= 1:
            dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
            return {"first_name": None}
        else:
            return {"first_name": slot_value}

    def validate_last_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `last_name` value."""

        # If the name is super short, it might be wrong.
        print(f"Last name given = {slot_value} length = {len(slot_value)}")
        if len(slot_value) <= 1:
            dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
            return {"last_name": None}
        else:
            return {"last_name": slot_value}

## Name Asking End Here
