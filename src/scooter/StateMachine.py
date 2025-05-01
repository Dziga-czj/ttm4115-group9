# states
idle = {'name': 'idle', 
        'entry': 'on_idle', 
        'exit': 'exit_idle'}
    
reserving = {'name': 'reserving', 
             'entry': 'on_reserving; start_timer("t_reserving", 30000)'}

alarming = {'name': 'alarming', 
            'entry': 'on_alarming', 
            'exit': 'exit_alarming'}
    
riding = {'name': 'riding', 
          'entry': 'on_riding; stop_timer("t_reserving")', 
          'exit': 'exit_riding'}


# transitions
t0 = {'source': 'initial', 
      'target': 'idle'}

t1 = {'source': 'idle', 
      'target': 'reserving', 
      'trigger': 'reserve_from_server'}

t2 = {'source': 'reserving', 
      'target': 'idle', 
      'trigger': 't_reserving'}

t3 = {'source': 'idle', 
      'target': 'alarming', 
      'trigger': 'unexpected_movement_detected'}  
  
t4 = {'source': 'alarming', 
      'target': 'idle', 
      'trigger': 'movement_stopped'} 

t5 = {'source': 'reserving', 
      'target': 'riding', 
      'trigger': 'unlock_reserved_from_server'}

t6 = {'source': 'idle', 
      'target': 'riding', 
      'trigger': 'unlock_from_server'}

t7 = {'source': 'riding', 
      'target': 'idle', 
      'trigger': 'lock_from_server'}