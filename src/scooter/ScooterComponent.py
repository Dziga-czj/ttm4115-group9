import threading
from stmpy import Machine, Driver
import paho.mqtt.client as mqtt
from SenseHat_LED.Display import *
# from sense_hat import SenseHat
from StateMachine import *


class Scooter():
    def __init__(self, ID, broker, port, senseHat, battery):
        self.ID = ID
        self.broker = broker
        self.port = port
        self.topic = f'scooter/{self.ID}' # TBD
        self.topic_feedback = f'scooter/{self.ID}/feedback'
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
        self.mqtt_client.subscribe(f'scooter/{self.ID}')
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
        print("Scooter is idle")
        self.idle = True
        self._idle_thread = threading.Thread(target=self.detect_movement_1)
        self._idle_thread.start()

    def detect_movement_1(self):
        while self.idle:
            accel = self.sense.get_accelerometer_raw()
            if not all(round(value, 1) == 0.0 for value in accel.values()):
                self.mqtt_client.publish(self.topic, "unexpected_movement_detected")
                self.mqtt_client.publish(self.topic_feedback, "unexpected_movement_detected")
            time.sleep(1)

    def exit_idle(self):
        self.idle = False
        self._idle_thread.join()
        self._idle_thread = None
        self.sense.clear()

    def on_reserving(self):
        print("Scooter is reserved")
        
    # def start_timer(self, trigger, duration):
    #     self.driver.set_timer(self.stm.name, trigger, duration, self.timer_expiry)
    
    # def timer_expiry(self):
    #     print("Reservation expired")
    
    def on_alarming(self):
        print("Scooter is alarming")
        self.sense.show_message("STOP MOVING", text_colour=[255, 0, 0])
        self.alarming = True
            
    def detect_movement_2(self):
        accum = []
        while self.alarming:
            accel = self.sense.get_accelerometer_raw()
            if all(round(value, 1) == 0.0 for value in accel.values()):
                accum.append(0)
            else:
                accum.append(1)
            time.sleep(1)
            if accum.size > 5:
                if all(i == 0 for i in accum[-5:]):
                    self.mqtt_client.publish(self.topic, "movement_stopped")
                    self.mqtt_client.publish(self.topic_feedback, "movement_stopped")
                    break
   
    def exit_alarming(self):
        print("Scooter stopped alarming")
        self.alarming = False
        self.sense.clear()
    
    def on_riding(self):
        self.mqtt_client.publish(self.topic_feedback, "scooter_unlocked")
        print("Scooter is riding")
        self.riding = True
        self._riding_thread = threading.Thread(target=self.riding_display)
        self._riding_thread.start()
        
    # def stop_timer(self, trigger):
    #     self.driver.cancel_timer(self.stm.name, trigger)
    
    def riding_display(self):
        while self.riding:
            display(self.sense, self.battery.get_battery())
        
    def exit_riding(self):
        self.mqtt_client.publish(self.topic_feedback, "scooter_locked")
        print("Scooter stopped riding")
        self.riding = False
        self._riding_thread.join()
        self._riding_thread = None
        self.sense.clear()


class Battery:
    def __init__(self, ID, battery_level):
        self.ID = ID
        self.battery_level = battery_level # battery 0.0 - 8.0
        
    def get_battery(self):
        return self.battery_level
    
    def charge(self, battery_level):
        self.battery_level += 0.1



class Scooter_test(): #without senseHat
    def __init__(self, ID, broker, port, battery):
        self.ID = ID
        self.broker = broker
        self.port = port
        self.topic = f'scooter/{self.ID}'
        self.topic_feedback = f'scooter/{self.ID}/feedback'
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
        self.mqtt_client.subscribe(f'scooter/{self.ID}')
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
        print("Scooter is idle")
        self.idle = True
        self._idle_thread = threading.Thread(target=self.detect_movement_1)
        self._idle_thread.start()

    def detect_movement_1(self):
        # while self.idle:
        #     accel = self.sense.get_accelerometer_raw()
        #     if not all(round(value, 1) == 0.0 for value in accel.values()):
        #         self.mqtt_client.publish(self.topic, "unexpected_movement_detected")
        #         self.mqtt_client.publish(self.topic_feedback, "unexpected_movement_detected")
        #     time.sleep(1)
        return None

    def exit_idle(self):
        self.idle = False
        self._idle_thread.join()
        self._idle_thread = None
        # self.sense.clear()

    def on_reserving(self):
        print("Scooter is reserved")
        
    # def starttimer(self, trigger, duration):
    #     self.driver.set_timer(self.stm.name, trigger, duration, self.timer_expiry)
    
    # def timer_expiry(self):
    #     print("Reservation expired")
    
    def on_alarming(self):
        print("Scooter is alarming")
        # self.sense.show_message("STOP MOVING", text_colour=[255, 0, 0])
        self.alarming = True
        
    def detect_movement_2(self):
        # accum = []
        # while self.alarming:
        #     accel = self.sense.get_accelerometer_raw()
        #     if all(round(value, 1) == 0.0 for value in accel.values()):
        #         accum.append(0)
        #     else:
        #         accum.append(1)
        #     time.sleep(1)
        #     if accum.size > 5:
        #         if all(i == 0 for i in accum[-5:]):
        #             self.mqtt_client.publish(self.topic, "movement_stopped")
        #             self.mqtt_client.publish(self.topic_feedback, "movement_stopped")
        #             break
        return None
   
    def exit_alarming(self):
        print("Scooter stopped alarming")
        self.alarming = False
        # self.sense.clear()
    
    def on_riding(self):
        self.mqtt_client.publish(self.topic_feedback, "scooter_unlocked")
        print("Scooter is riding")
        self.riding = True
        self._riding_thread = threading.Thread(target=self.riding_display)
        self._riding_thread.start()
        
    # def stoptimer(self, trigger):
    #     self.driver.cancel_timer(self.stm.name, trigger)

    def riding_display(self):
        # while self.riding:
        #     display(self.sense, self.battery.get_battery())
        return None
        
    def exit_riding(self):
        self.mqtt_client.publish(self.topic_feedback, "scooter_locked")
        print("Scooter stopped riding")
        self.riding = False
        self._riding_thread.join()
        self._riding_thread = None
        # self.sense.clear()