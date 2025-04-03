from stmpy import Machine, Driver
import paho.mqtt.client as mqtt

broker, port = 'test.mosquitto.org', 1883


class SCOOTER():
    
    def on_init(self):
       pass
        
    def on_waiting(self):
       pass
        
    def on_reserving(self):
       pass
        
    def on_riding(self):
       pass
        
    def on_alarm(self):
       pass

   
        
# transitions
t0 = {'sourse': 'initial', 
      'target': 'waiting'}

t1 = {'source': 'waiting', 
      'target': 'reserving', 
      'trigger': 'reserved'}

t2 = {'source': 'reserving', 
      'target': 'waiting', 
      'trigger': 't_reserving'}

t3 = {'source': 'waiting', 
      'target': 'alarming', 
      'trigger': 'moving_when_locked'}  
  
t4 = {'source': 'alarming', 
      'target': 'waiting', 
      'trigger': 'stop_moving'} 

t5 = {'source': 'reserving', 
      'target': 'riding', 
      'trigger': 'unlock'}

t6 = {'source': 'riding', 
      'target': 'waiting', 
      'trigger': 'lock'}


# states
# trigger
# effect 
# cinditions
# guard
waiting = {'name': 'waiting'}
    
reserving = {'name': 'reserving', 
              'entry': 'on_waiting; start_timer("t_reserving", 180000)', 
              'exit': 'stop_timer("t_reserving")'}
    
alarming = {'name': 'alarming', 
            'entry': 'start_alarm', 
            'exit': 'stop_alarm'}
    
riding = {'name': 'riding', 
          'entry': 'unlock; start_timer', 
          'exit': 'stop_timer; lock'}