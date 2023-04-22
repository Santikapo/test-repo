import sys
import random


keyintervals = {
    "major" : ['ton', 'maj2', 'maj3', 'per4', 'per5', 'maj6', 'maj7']
}

keychords = {
    "major" : ['major', 'minor', 'minor', 'major', 'major', 'minor', 'dim']
}

intervals = ['ton', 'min2', 'maj2', 'min3', 'maj3', 'per4', 'tri', 'per5', 'min6', 'maj6', 'min7', 'maj7']

chords = {

    'major' : ['maj3', 'per5'],
    'minor' : ['min3', 'per5'],
    'dim' : ['min3', 'tri']
}

pitches = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def main():
    
    ans = input("Type 1 for intervals or type 2 for progressions\n")
    print("")

    if int(ans) == 1:
        # intervals
        new = [intervals[random.randint(1, 11)]]
        print(generate_intervals(random.randint(0, 11), new))
    elif int(ans) == 2:
        # progressions
        generatekey = random.randint(0, 11)
        prog = generate_progression(generatekey, 'major', 6-1)
        print("key is " + pitches[generatekey])
        print(prog)
    else:
        # end
        x =4
    sys.exit()

def generate_intervals(start, given_intervals):

    notes = [pitches[start]]

    for interval in given_intervals:
        new = jump(start, intervals.index(interval))
        notes.append(pitches[new])
    
    return notes

def generate_progression(tonic, scale, len):

    prog = []

    # generate tonic chord
    prog.append(generate_intervals(tonic, chords[keychords[scale][0]]))

    # generate other chords
    for i in range(len):
        # generate interval to jump to
        newint = keyintervals[scale][random.randint(0, 6)]
        # find tonic of that interval
        newtonic = jump(tonic, intervals.index(newint))
        # generate new chord using new tonic and chord instructions
        prog.append(generate_intervals(newtonic, chords[keychords[scale][keyintervals[scale].index(newint)]]))

    return prog


def jump(start, end):

    for i in range(end):
        if start != 11:
            start += 1
        else:
            start = 0
    
    return start
            

def play_sound(notes, order):
    x =4


main()
