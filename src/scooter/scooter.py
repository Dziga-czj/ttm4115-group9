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
      'target': 'waiting'}

t3 = {'source': 'reserving', 
      'target': 'riding'}

t4 = {'source': 'riding', 
      'target': 'reserving'}

t5 = {'source': 'waiting', 
      'target': 'alarming'}  
  
t6 = {'source': 'alarming', 
      'target': 'waiting'} 


#states
waiting = {'name': 'waiting', 
           'entry': 'on_waiting'}
    
reserving = {'name': 'reserving', 
              'entry': 'on_waiting; start_timer("t", 180000)'}
    
alarming = {'name': 'alarming', 
            'entry': 'on_alarm', 
            'exit': ''}
    
riding = {'name': 'riding', 
          'entry': 'on_riding'}