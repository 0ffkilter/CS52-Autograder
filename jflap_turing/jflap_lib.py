import xml.etree.ElementTree as ET

class State:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.accept = False
        self.initial = False

    def mark_as_accept(self):
        self.accept = True

    def mark_as_initial(self):
        self.initial = True

class Transition:
    def __init__(self, from_s, to_s, read, write, move):
        self.from_s = from_s
        self.to_s = to_s
        self.read = read
        self.write = write
        self.move = move

class TuringMachine:

    def __init__(self, filename):
        self.tree = ET.parse(filename)

        #structure
        root = self.tree.getroot()
        self.type = root[0]
        self.automaton = root[1]
        self.states = []
        self.transitions = []
        self.initial = ""


        for child in self.automaton:
            if child.tag == "block":
                block = State(child.attrib['id'], child.attrib['name'])
                for block_attr in child:
                    if block_attr.tag == "initial":
                        block.mark_as_initial()
                    if block_attr.tag == "final":
                        block.mark_as_accept()
                self.states.append(block)
            elif child.tag == "transition":
                trans = Transition(
                    child.find("from").text,
                    child.find("to").text,
                    child.find("read").text,
                    child.find("write").text,
                    child.find("move").text
                    )
                print(child.find("read").text)
                self.transitions.append(trans)

            print(child.tag, child.attrib)
        
        for state in self.states:
            if state.initial == True:
                self.initial = state.id

    def run_input_string(self, input_string):

        input_string = [a for a in input_string]

        current_idx = 0
        current_state = self.initial


        for i in range(1000):
            #Look through all the transitions
            for t in self.transitions:
                #If the state matches and the input matches
                if current_state == t.from_s and t.read == input_string[current_idx]:
                    #write to tape
                    input_string[current_idx] = t.write

                    #Move
                    if t.move == "L":
                        current_idx = current_idx - 1
                        #extend tape
                        if current_idx == -1:
                            current_idx = 0
                            input_string = [None] + input_string
                    elif t.move == "R":
                        #extend tape
                        current_idx = current_idx + 1
                        if current_idx == len(input_string):
                            input_string = input_string + [None]
                    current_state = t.to_s
                    for s in self.states:
                        if current_state == s.id and s.accept:
                            return True

        return False

def make_and_run(filename, string, should_pass):
    TM = TuringMachine(filename)
    if TM.run_input_string(string) == should_pass:
        return True
    return False
