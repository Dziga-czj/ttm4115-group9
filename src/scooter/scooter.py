from stmpy import Machine, Driver
import paho.mqtt.client as mqtt

# states
waiting = {'name': 'waiting'}
    
reserving = {'name': 'reserving', 
              'entry': 'on_waiting; start_timer("t_reserving", 180000)', # need code for timer?
              'exit': 'stop_timer("t_reserving")'}
    
alarming = {'name': 'alarming', 
            'entry': 'start_alarm', 
            'exit': 'stop_alarm'}
    
riding = {'name': 'riding', 
          'entry': 'unlock; start_timer', 
          'exit': 'stop_timer; lock'}

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

class Scooter():
    def __init__(self, ID, broker, port):
        self.ID = ID
        self.broker = broker
        self.port = port
        self.topic = f'scooter/{self.ID}' # TBD
    
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(self.broker, self.port)
        self.mqtt_client.subscribe(f'scooter/{self.ID}')
        self.mqtt_client.loop_start()
        
        self.driver = Driver()
        self.stm = Machine(name=f'scooter_{self.ID}', 
                           transitions=[t0, t1, t2, t3, t4, t5, t6],
                           states=[waiting, reserving, alarming, riding],
                           obj=self)
        self.driver.add_machine(self.stm)
        self.driver.start()
    
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        command = msg.payload.decode() # trigger for transition
        self.stm.send(command)

    def on_waiting(self):
        self.mqtt_client.publish(self.topic, "waiting")

    def on_reserving(self):
        self.mqtt_client.publish(self.topic, "reserving")
    
    def on_riding(self):
        self.mqtt_client.publish(self.topic, "riding")
        
    def on_alarming(self):
        self.mqtt_client.publish(self.topic, "moving_when_locked")
   
    def stop_alarming(self):
        self.mqtt_client.publish(self.topic, "stop_moving")
        
    def unlock(self):
        self.mqtt_client.publish(self.topic, "unlock")

    def lock(self):
        self.mqtt_client.publish(self.topic, "lock")



