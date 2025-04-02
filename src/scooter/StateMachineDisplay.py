from transitions import Machine

class ScooterStateMachine:
    def __init__(self):
        # Define states
        normal = {
            'name': 'normal',
        }
        alarmTriggeredOn = {
            'name': 'alarmTriggeredOn',
            'entry': 'trunLightsOn()',
            'exit': 'playLoudNoises()',
        }
        alarmTriggeredOff = {
            'name': 'alarmTriggeredOff',
            'entry': ['turnLightsOff()','start_timer("t2", 50)'],
        }
        displayBattery = {
            'name': 'displayBattery',
            'entry': ['showBatteryOnPiHat()', 'startTimer("t1",3000)'],
            'exit': 'stopDisplayingBattery()',
        }
        refreshBattery = {
            'name': 'refreshBattery',
            'entry': ['refreshBatteryState()','sendSignal("refreshed")'],
        }
        
        # Transitions
        transitions = [
            {'trigger': 'start_alarm_light', 'source': 'normal', 'target': 'alarmTriggeredOn',},
            {'trigger': 'stop_alarm_light', 'source': 'alarmTriggeredOn', 'target': 'normal'},
            {'trigger': 't2', 'source': 'alarmTriggeredOn', 'target': 'alarmTriggeredOff'},
            {'trigger': 't2', 'source': 'alarmTriggeredOff', 'target': 'alarmTriggeredOn'},
            {'trigger': 'start_battery_display', 'source': 'normal', 'target': 'displayBattery'},
            {'trigger': 'stop_battery_display', 'source': 'displayBattery', 'target': 'normal'},
            {'trigger': 'refresh_battery', 'source': 'displayBattery', 'target': 'refreshBattery'},
            {'trigger': 't1', 'source': 'refreshBattery', 'target': 'displayBattery'},
        ]

        # Create the state machine
        self.stm = Machine(name='scooter', states=[normal, alarmTriggeredOn, alarmTriggeredOff, displayBattery, refreshBattery], transitions=transitions, initial='normal')
    
    # Example actions
    def start_timer(self, timer_name, duration):
        print(f"Timer {timer_name} started for {duration} milliseconds.")

    def play_loud_noises(self):
        print("Dziga screaming loud noices.")

    def turn_lights_on(self):
        #TODO
        return
    
    def turn_lights_off(self):
        #TODO
        return

    def show_battery_on_pi_hat(self):
        #TODO
        return
    
    def stop_displaying_battery(self):
        #TODO
        return
    
    def refresh_battery_state(self):
        #TODO
        return

    def send_signal(self, signal):
        #TODO
        return
    

if __name__ == "__main__":
    scooter = ScooterStateMachine()
    driver = Driver() #Need to be adapted to the actual driver class!
    driver.add_machine(scooter.stm)
    driver.start()


