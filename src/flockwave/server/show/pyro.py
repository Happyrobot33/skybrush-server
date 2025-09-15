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
    
    #print the events
    events = pyro.get("events", None)
    #print(f"Pyro events: {events}")

    event_data = None
    #for each event, iterate them and add them to a list
    #first element in the array is the time in seconds. Convert this to milliseconds, then store it as a varint
    if events:
        event_data = bytearray()
        for event in events:
            time_ms = int(event[0] * 1000)
            #encode the channel as a byte
            channel = encode_variable_length_integer(event[1])

            #encode time_ms as a varint
            event_data.extend(encode_variable_length_integer(time_ms))

            event_data.extend(channel)
    return event_data
