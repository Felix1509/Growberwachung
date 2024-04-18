import os

# Funktion zum generieren eines
def create_schedule(schedule_string):
    schedule = [False] * (24 * 60)
    if schedule_string == '' or schedule_string == 'AUS':
        return schedule
    elif schedule_string == 'AN':
        return [True] * (24*60)
    lines = schedule_string.split('\n')

    for line in lines:
        if line == '': next
        action, time = line.split()
        hours, minutes = map(int, time.split(':'))

        if action == 'EIN':
            start_index = hours * 60 + minutes
        elif action == 'AUS':
            end_index = hours * 60 + minutes

            # Setze die Werte im Array für den Zeitraum zwischen EIN und AUS
            if end_index < start_index:
                for i in range(0, end_index):
                    schedule[i] = True
                for i in range(start_index, 24*60):
                    schedule[i] = True
            else:
                for i in range(start_index, end_index):
                    schedule[i] = True
    return schedule

def load_schedule_from_file(zelt_id=0, aktor_id=0):
    filename = f'{zelt_id}_{aktor_id}_zeitplan.txt'
    file_path = f'zeitplaene/{filename}'
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            schedule_string = file.read()
            return create_schedule(schedule_string)
    else:
        with open(file_path, 'w') as file:
            file.write('')
        return [False] * (24 * 60)

def save_schedule_to_file(schedule_string, zelt_id=0, aktor_id=0):
    filename = f'{zelt_id}_{aktor_id}_zeitplan.txt'
    file_path = f'zeitplaene/{filename}'
    
    # Überprüfen, ob die Datei bereits existiert und versuchen sie zu löschen
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Fehler beim Löschen der Datei: {e}")
            return False
    
    # Datei schreiben
    with open(file_path, 'w') as file:
        file.write(schedule_string)
    
    return True


# Test Routine as main of this file!
print("Successfully imported 'entities_zeitplan.py\n------------------------------------")