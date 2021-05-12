# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,EventType
from datetime import datetime as dt


time = Tracker.get_slot("time")
time_object = dt.strptime(time, "%H:%M")

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict 
    ) -> List[EventType]:
        required_slots = ["number", "section","time"]
        last = tracker.slots_to_validate()

        if "time" in last.keys():
            time2 = last["time"]
            print(time2)
            time2 = time2.split(":")
            hour = int(time2[0].split("T")[1])
            minutes = (int(int(time2[1])/30.0))*30

            if hour<19 or hour>21:
                time = None
                dispatcher.utter_message(text="We are not open at that time. We are only open from 7pm to 10pm")
                return[SlotSet("requested_slot","time"),SlotSet("time",time)]

            else:
                hour = hour-12
                if minutes==0:
                    time = str(hour)+"pm"
                else:
                    time = str(hour)+":"+str(minutes)+"pm"
                for slot_name in required_slots:
                    if tracker.slots.get(slot_name) is None:
                    # if time se set and all other are filled 
                        return [SlotSet("requested_slot", slot_name),SlotSet("time",time)]

                return [SlotSet("requested_slot", None),SlotSet("time", time)]
                
        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]


class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_summary",number=tracker.get_slot("number"),time=tracker.get_slot("time"),section=tracker.get_slot("section"))
        return [SlotSet("time",None),SlotSet("number",None),SlotSet("section",None)]
