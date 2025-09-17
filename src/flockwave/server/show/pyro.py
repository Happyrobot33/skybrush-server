from base64 import b64decode
from typing import Dict

from flockwave.server.show.utils import encode_variable_length_integer

__all__ = ("get_pyro_program_from_show_specification",)


def get_pyro_program_from_show_specification(show: Dict) -> bytes:
    #print out all the keys of the show
#    for key in show.keys():
#        print(f"Show key: {key}")
    
    #print whats in the pyro key
    pyro = show.get("pyro", None)
    if not pyro:
        return None
    
#    for key in pyro.keys():
#        print(f"Pyro key: {key}")
    
    #we need to get the real events list after my fuckery dealing with the studio server software
    #get the first payload
    payloads = pyro.get("payloads", None)
    if not payloads:
        return None
    
    #print(f"Pyro payloads: {payloads}")
    
    #get the name in the first payload
    payload1 = payloads.get("payload1", None)
    if not payload1:
        return None
    
    #print(f"Pyro payload1: {payload1}")
    name = payload1.get("name", None)
    if not name:
        return None
    
    #the name is ACTUALLY a array of events

    #print the events
    events = eval(name)
    #events = pyro.get("events", None)
    #print(f"Pyro events: {events}")

    event_data = None
    #for each event, iterate them and add them to a list
    #first element in the array is the time in seconds. Convert this to milliseconds, then store it as a varint
    if events:
        event_data = bytearray()
        for event in events:
            #print(f"Event: {event}")
            #subtract the prefire time from the event time
            time_ms = int(event[0] * 1000) - int(event[5] * 1000)

            #encode time_ms as a varint
            event_data.extend(encode_variable_length_integer(time_ms))

            event_data.extend(encode_variable_length_integer(event[1]))

            #encode the signs of pitch yaw roll in a single byte
            signs = 0
            if event[2] < 0:
                signs |= 0b100
            if event[3] < 0:
                signs |= 0b010
            if event[4] < 0:
                signs |= 0b001
            
            event_data.append(signs)

            #pitch yaw roll
            event_data.extend(encode_variable_length_integer(abs(event[2])))
            event_data.extend(encode_variable_length_integer(abs(event[3])))
            event_data.extend(encode_variable_length_integer(abs(event[4])))
    return event_data
