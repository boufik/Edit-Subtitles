# 1. Open the file
filepath = "/content/1.srt"
with open(filepath, 'r', encoding='ISO-8859-7') as file:
    lines = file.readlines()

print(f"Lines = {lines}\nLength = {len(lines)}")

# 2. Inspect the contents of the file
print("******** Let's see how the .srt file looks like ********")
for i, line in enumerate(lines):
    if i < 8:
        print(f"{i}: {line}")
    else:
        break
print("********************************************************")



# AUXILIARY FUNCTIONS
def is_to_edit(line):
    # Edittable lines length = 30 (12 + 12 for each timestamp, 5 for ' --> ' AND 1 FOR THE FINAL NEW-LINE CHARACTER '\n')
    LEN = len(line)
    arrow = ' --> '
    return (LEN == 30) and (arrow in line)



def translate(timestamp):
    # Input example = '02:10:40,950'
    LEN = len(timestamp)
    ch1 = timestamp[2]
    ch2 = timestamp[5]
    ch3 = timestamp[8]
    # Check if is a valid timestamp
    if (LEN != 12) or (ch1+ch2+ch3 != '::,'):
        return False
    # Separate the values
    hours = timestamp[:2]
    minutes = timestamp[3:5]
    seconds = timestamp[6:8]
    ms = timestamp[9:]
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)
    ms = int(ms)
    vector = [hours, minutes, seconds, ms]
    return vector



def add_time(vector, secs_to_add):
    # Example (Hard case) = '06:59:59:800' and add = 2.7 secs ----> '07:00:02:500'
    hours, minutes, seconds, ms = vector
    ms_to_add = int(1000 * secs_to_add)
    ms += ms_to_add
    while ms >= 1000:                   # ms = 3500, in the 1st try of the loop
        ms -= 1000
        seconds += 1
    while seconds >= 60:                # seconds = 62 = 59 + 3, in the 1st try of the loop
        seconds -= 60
        minutes += 1
    while minutes >= 60:                # minutes = 60 = 59 + 1, in the 1st try of the loop
        minutes -= 60
        hours += 1
    return [hours, minutes, seconds, ms]



def retranslate(vector):
    h, m, s, ms = vector
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"




def edit_subtitles(lines, secs_to_add):
    counter = 0
    for i, line in enumerate(lines):
        if is_to_edit(line):
            timestamp1 = line[:12]
            timestamp2 = line[-13:-1]
            vector1 = translate(timestamp1)
            vector2 = translate(timestamp2)
            new1 = add_time(vector1, secs_to_add)
            new2 = add_time(vector2, secs_to_add)
            new_time1 = retranslate(new1)
            new_time2 = retranslate(new2)
            lines[i] = new_time1 + ' --> ' + new_time2 + '\n'
            counter += 1
    print(f"Edited {counter} lines")
    return lines



# MAIN FUNCTION
secs_to_add = 1.2
editted_lines = edit_subtitles(lines, secs_to_add)
with open('editted_subtitles.srt', 'w', encoding='ISO-8859-7') as file:
    for line in editted_lines:
        file.write(line)
