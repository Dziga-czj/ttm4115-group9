import threading
from stmpy import Machine, Driver
import paho.mqtt.client as mqtt
from SenseHat_LED.Display import *
from StateMachine import *


class Scooter():
    def __init__(self, ID, broker, port, senseHat, battery):
        self.ID = ID
        self.broker = broker
        self.port = port
        self.topic = f'ttm4115/group09/v3/scooter/{self.ID}' 
        self.topic_feedback = f'ttm4115/group09/v3/scooter/{self.ID}/feedback'
        self.sense = senseHat
        self.battery = battery
        self.idle = False
        self._idle_thread = None
        self.riding = False
        self._riding_thread = None
        self.alarming = False
        self._alarming_thread = None
    
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(self.broker, self.port)
        # self.mqtt_client.subscribe(self.topic)
        self.mqtt_client.loop_start()
        
        self.driver = Driver()
        self.stm = Machine(name=f'scooter_{self.ID}', 
                           transitions=[t0, t1, t2, t3, t4, t5, t6, t7],
                           states=[idle, reserving, alarming, riding],
                           obj=self)
        self.driver.add_machine(self.stm)
        self.driver.start()
    
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        command = msg.payload.decode() # trigger for transition
        self.stm.send(command)

    def on_idle(self):
        print(f"Scooter{self.ID} is idle")
        self.idle = True
        self._idle_thread = threading.Thread(target=self.detect_movement_1)
        self._idle_thread.start()

    def detect_movement_1(self): # detect weather scooter is moving or not
        while self.idle:
            accel = self.sense.get_accelerometer_raw()
            if not all(round(value, 1) == 0.0 for value in accel.values()): # check accelometer data is 0.0
                self.mqtt_client.publish(self.topic, "unexpected_movement_detected")
                self.mqtt_client.publish(self.topic_feedback, "unexpected_movement_detected")
            time.sleep(1) # once per second 

    def exit_idle(self):
        self.idle = False
        self._idle_thread.join()
        self._idle_thread = None
        self.sense.clear() # stop detecting

    def on_reserving(self):
        print(f"Scooter{self.ID} is reserved")
        self.sense.show_message("RESERVED", text_colour=[255, 0, 0]) # display on LED matrix
    
    # timer function not needed, already intergrated in stmpy
    # def start_timer(self, trigger, duration):
    #     self.driver.set_timer(self.stm.name, trigger, duration, self.timer_expiry)
    # def timer_expiry(self):
    #     print("Reservation expired")
    
    def on_alarming(self):
        print(f"Scooter{self.ID} is alarming")
        self.sense.show_message("STOP MOVING", text_colour=[255, 0, 0]) # display on LED matrix
        self.alarming = True
            
    def detect_movement_2(self):
        accum = []
        while self.alarming:
            accel = self.sense.get_accelerometer_raw()
            if all(round(value, 1) == 0.0 for value in accel.values()):
                accum.append(0) # if scooter is not moving, append 0 to accum
            else:
                accum.append(1)
            time.sleep(1)
            if accum.size > 5:
                if all(i == 0 for i in accum[-5:]): # check scooter is idle for 5 seconds
                    self.mqtt_client.publish(self.topic, "movement_stopped")
                    self.mqtt_client.publish(self.topic_feedback, "movement_stopped")
                    break
   
    def exit_alarming(self):
        print(f"Scooter{self.ID} stopped alarming")
        self.alarming = False
        self.sense.clear() # clear LED matrix
    
    def on_riding(self):
        self.mqtt_client.publish(self.topic_feedback, "scooter_unlocked")
        print(f"Scooter{self.ID} is riding")
        self.riding = True
        self._riding_thread = threading.Thread(target=self.riding_display) # having LED matrix on
        self._riding_thread.start()
        
    # def stop_timer(self, trigger):
    #     self.driver.cancel_timer(self.stm.name, trigger)
    
    def riding_display(self):
        while self.riding:
            display(self.sense, self.battery.get_battery()) # shouw speed and battery level on LED matrix
        
    def exit_riding(self):
        self.mqtt_client.publish(self.topic_feedback, "scooter_locked")
        print(f"Scooter{self.ID} stopped riding")
        self.riding = False
        self._riding_thread.join()
        self._riding_thread = None
        self.sense.clear() # turn off LED matrix


class Battery:
    def __init__(self, ID, battery_level):
        self.ID = ID
        self.battery_level = battery_level # battery 0.0 - 8.0
        
    def get_battery(self):
        return self.battery_level
    
    def charge(self, battery_level):
        if self.battery_level < 8.0:
            self.battery_level += 0.1
        else:
            print("Battery is full")
        
    def discharge(self, battery_level):
        if self.battery_level > 0.0:
            self.battery_level -= 0.1
        else:
            print("Battery is empty")


    
# exactly the same as Scooter class, but without senseHat functions, can be tested on pc
class Scooter_test():
    def __init__(self, ID, broker, port, battery):
        self.ID = ID
        self.broker = broker
        self.port = port
        self.topic = f'ttm4115/group09/v3/scooter/{self.ID}' 
        self.topic_feedback = f'ttm4115/group09/v3/scooter/{self.ID}/feedback'
        # self.sense = senseHat
        self.battery = battery
        self.idle = False
        self._idle_thread = None
        self.riding = False
        self._riding_thread = None
        self.alarming = False
        self._alarming_thread = None
    
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(self.broker, self.port)
        # self.mqtt_client.subscribe(self.topic)
        self.mqtt_client.loop_start()
        
        self.driver = Driver()
        self.stm = Machine(name=f'scooter_{self.ID}', 
                           transitions=[t0, t1, t2, t3, t4, t5, t6, t7],
                           states=[idle, reserving, alarming, riding],
                           obj=self)
        self.driver.add_machine(self.stm)
        self.driver.start()
    
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        command = msg.payload.decode() # trigger for transition
        self.stm.send(command)

    def on_idle(self):
        print(f"Scooter{self.ID} is idle")
        self.idle = True
        self._idle_thread = threading.Thread(target=self.detect_movement_1)
        self._idle_thread.start()

    def detect_movement_1(self): # detect weather scooter is moving or not
        # while self.idle:
        #     accel = self.sense.get_accelerometer_raw()
        #     if not all(round(value, 1) == 0.0 for value in accel.values()): # check accelometer data is 0.0
        #         self.mqtt_client.publish(self.topic, "unexpected_movement_detected")
        #         self.mqtt_client.publish(self.topic_feedback, "unexpected_movement_detected")
        #     time.sleep(1) # once per second 
        return None

    def exit_idle(self):
        self.idle = False
        self._idle_thread.join()
        self._idle_thread = None
        # self.sense.clear() # stop detecting

    def on_reserving(self):
        print(f"Scooter{self.ID} is reserved")
        # self.sense.show_message("RESERVED", text_colour=[255, 0, 0]) # display on LED matrix
    
    # timer function not needed, already intergrated in stmpy
    # def start_timer(self, trigger, duration):
    #     self.driver.set_timer(self.stm.name, trigger, duration, self.timer_expiry)
    # def timer_expiry(self):
    #     print("Reservation expired")
    
    def on_alarming(self):
        print(f"Scooter{self.ID} is alarming")
        # self.sense.show_message("STOP MOVING", text_colour=[255, 0, 0]) # display on LED matrix
        self.alarming = True
            
    def detect_movement_2(self):
        # accum = []
        # while self.alarming:
        #     accel = self.sense.get_accelerometer_raw()
        #     if all(round(value, 1) == 0.0 for value in accel.values()):
        #         accum.append(0) # if scooter is not moving, append 0 to accum
        #     else:
        #         accum.append(1)
        #     time.sleep(1)
        #     if accum.size > 5:
        #         if all(i == 0 for i in accum[-5:]): # check scooter is idle for 5 seconds
        #             self.mqtt_client.publish(self.topic, "movement_stopped")
        #             self.mqtt_client.publish(self.topic_feedback, "movement_stopped")
        #             break
        return None
   
    def exit_alarming(self):
        print(f"Scooter{self.ID} stopped alarming")
        self.alarming = False
        # self.sense.clear() # clear LED matrix
    
    def on_riding(self):
        self.mqtt_client.publish(self.topic_feedback, "scooter_unlocked")
        print(f"Scooter{self.ID} is riding")
        self.riding = True
        self._riding_thread = threading.Thread(target=self.riding_display) # having LED matrix on
        self._riding_thread.start()
        
    # def stop_timer(self, trigger):
    #     self.driver.cancel_timer(self.stm.name, trigger)
    
    def riding_display(self):
        # while self.riding:
        #     display(self.sense, self.battery.get_battery()) # shouw speed and battery level on LED matrix
        return None
    
    def exit_riding(self):
        self.mqtt_client.publish(self.topic_feedback, "scooter_locked")
        print(f"Scooter{self.ID} stopped riding")
        self.riding = False
        self._riding_thread.join()
        self._riding_thread = None
        # self.sense.clear() # turn off LED matrix
