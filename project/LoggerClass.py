import logging


# LOGGING --

class Logger:

                            
    # CRITICAL 	50
    # ERROR 	40
    # WARNING 	30
    # INFO 	20
    # DEBUG 	10
    # NOTSET 	0


    def __init__(self, module_name, class_name, set_consolle_log_level = logging.DEBUG, set_file_log_level = logging.ERROR, name = None,  ):  

        if not( module_name and class_name ):
            raise Exception("Invalid parameters! Logger not istantiate.")
                          
        self._name = None
        self._module_name = module_name
        self._class_name = class_name
        self._set_consolle_log_level =  set_consolle_log_level
        self._set_file_log_level =  set_file_log_level        

        if not class_name:
            self._name = General.setName('Logger_Name')
        else:
            self._name = name

        logging.basicConfig( level = logging.DEBUG )
        # Create a custom logger
        self.logger = logging.getLogger( self._module_name )

        # Create handlers
        self.c_handler = logging.StreamHandler()
        self.f_handler = logging.FileHandler( 'Log_' + self._class_name + '.log' )
        self.c_handler.setLevel( self._set_consolle_log_level )
        self.f_handler.setLevel( self._set_file_log_level )

        # Create formatters and add it to handlers
        self.c_format = logging.Formatter('%(name)s - %(levelname)s - %(funcName)s - %(message)s')
        self.f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
        self.c_handler.setFormatter(self.c_format)
        self.f_handler.setFormatter(self.f_format)

        # Add handlers to the logger
        self.logger.addHandler(self.c_handler)
        self.logger.addHandler(self.f_handler)

    
    def getLogger(self):
        return self.logger

    