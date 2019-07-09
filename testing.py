from logger import AdcsLogger , InfoLogger


InfoLogger.get_instance().write_info('Lets do it')
AdcsLogger.get_instance().write_error('Adcs is here')
InfoLogger.get_instance().write_critical('Lets do it Again')
InfoLogger.get_instance().write_info('And Again')
