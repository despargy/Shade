from logger import AdcsLogger , InfoLogger



for i in range(4):
    AdcsLogger.get_instance().write_warning('Line '+str(i))

unset_data = AdcsLogger.get_instance().get_unsend_data()

for data in unset_data:
    print(data)

for i in range(5):
    AdcsLogger.get_instance().write_warning('Line '+str(i))

unset_data = AdcsLogger.get_instance().get_unsend_data()

for data in unset_data:
    print(data)


for i in range(4):
    InfoLogger.get_instance().write_warning('Line '+str(i))

unset_data = InfoLogger.get_instance().get_unsend_data()

for data in unset_data:
    print(data)

for i in range(5):
    InfoLogger.get_instance().write_warning('Line '+str(i))

unset_data = InfoLogger.get_instance().get_unsend_data()

for data in unset_data:
    print(data)


for i in range(5):
    InfoLogger.get_instance().write_warning('Line '+str(i))

unset_data = InfoLogger.get_instance().get_unsend_data()
    
print(InfoLogger.get_instance().last_sended_index)
print(InfoLogger.get_instance().log_id)
