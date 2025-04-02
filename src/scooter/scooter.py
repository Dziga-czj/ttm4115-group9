from stmpy import Machine, Driver
import paho.mqtt.client as mqtt

broker, port = 'test.mosquitto.org', 1883


class SCOOTER():
    
    def on_init(self):
        
        
    def on_waiting():
        
        
    def on_reserving():
        
        
    def on_riding():
        
        
    def on_alarm():
        
#transitions
t0 = {'sourse': 'initial', 
      'target': 'waiting'}

t1 = {'source': 'waiting', 
      'target': 'reserving'}

t2 = {'source': 'reserving', 
      'target': 'waiting', 
      'trigger': 't_reserving'}

t3 = {'source': 'reserving', 
      'target': 'riding'}

t4 = {'source': 'riding', 
      'target': 'reserving'}

t5 = {'source': 'waiting', 
      'target': 'alarming', 
      'trigger': 'moving_when_locked'}  
  
t6 = {'source': 'alarming', 
      'target': 'waiting', 
      'trigger': 'stop_moving'} 


#states
waiting = {'name': 'waiting', 
           'entry': ''}
    
reserving = {'name': 'reserving', 
              'entry': 'on_waiting; start_timer("t_reserving", 180000)'}
    
alarming = {'name': 'alarming', 
            'entry': '', 
            'exit': ''}
    
riding = {'name': 'riding', 
          'entry': ''}