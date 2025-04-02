from enum import Enum, auto
from transitions import Machine

class ScooterStateMachine:
    def __init__(self):
        # Define states
        idle = {
            'name': 'idle',
            'entry': 'put_brakes_on()',
        }
        hired = {
            'name': 'hired',
            'entry': 'put_brakes_off()',
        }
        alarm = {
            'name': 'alarm',
            'entry': 'start_alarm_light()',
            'exit': 'stop_alarm_light()',
        }
        moving = {
            'name': 'moving',
            'entry': 'start_recording_timer()',
            'exit': 'stop_recording_timer()',
        }
        
        # Transitions
        transitions = [
            {'trigger': 'power_on', 'source': 'OFF', 'target': 'idle'},
            {'trigger': 'hired', 'source': 'idle', 'target': 'hired'},
            {'trigger': 'idle', 'source': 'hired', 'target': 'idle'},
            {'trigger': 'moved', 'source': 'hired', 'target': 'moving'},
            {'trigger': 'stopped', 'source': 'moving', 'target': 'hired'},
            {'trigger': 'moved', 'source': 'idle', 'target': 'alarm'},
            {'trigger': 'stopped', 'source': 'alarm', 'target': 'idle'},
        ]

        # Create the state machine
        self.stm = Machine(name='scooter', states=[idle, hired, alarm, moving], transitions=transitions, initial='idle')
    
    # Example actions
    def put_brakes_on(self):
        print("Brakes are on.")
    
    def put_brakes_off(self):
        print("Brakes are off.")
    
    def start_alarm_light(self):
        print("Alarm light started.")
    
    def stop_alarm_light(self):
        print("Alarm light stopped.")
    
    def start_recording_timer(self):
        print("Recording timer started.")
    
    def stop_recording_timer(self):
        print("Recording timer stopped.")
    

if __name__ == "__main__":
    scooter = ScooterStateMachine()
    driver = Driver() #Need to be adapted to the actual driver class!
    driver.add_machine(scooter.stm)
    driver.start()


