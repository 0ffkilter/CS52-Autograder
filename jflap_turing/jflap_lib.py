import xml.etree.ElementTree as ET


class State:
    # Defines a state or node in the jflap file
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
    # Defines a transition line from node to node
    def __init__(self, from_s, to_s, read, write=None, move=None):
        # If it is a DFA, the 'read' attribute is the char to move to next on
        self.from_s = from_s
        self.to_s = to_s
        self.read = read
        self.write = write
        self.move = move


class TuringMachine:

    def __init__(self, filename):
        self.tree = ET.parse(filename)

        # structure
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
                self.transitions.append(trans)

        for state in self.states:
            if state.initial:
                self.initial = state.id

    def run_input_string(self, input_string):
        input_string = [a for a in input_string]

        current_idx = 0
        current_state = self.initial

        # Define the maximum number of steps as 1000
        for i in range(1000):

            # Look through all the transitions
            for t in self.transitions:
                # If the state matches and the input matches
                if current_state == t.from_s and \
                   t.read == input_string[current_idx]:
                    # write to tape
                    input_string[current_idx] = t.write

                    # Move
                    if t.move == "L":
                        current_idx = current_idx - 1

                        # extend tape
                        if current_idx == -1:
                            current_idx = 0
                            input_string = [None] + input_string
                    elif t.move == "R":
                        current_idx = current_idx + 1

                        # extend tape
                        if current_idx == len(input_string):
                            input_string = input_string + [None]

                    current_state = t.to_s
                    for s in self.states:
                        if current_state == s.id and s.accept:
                            return True

        return False


class DFA:

    def __init__(self, filename):
        self.tree = ET.parse(filename)

        # structure
        root = self.tree.getroot()
        self.type = root[0]
        self.automaton = root[1]
        self.states = []
        self.transitions = []
        self.initial = ""

        for child in self.automaton:

            if child.tag == "state":
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
                )

                self.transitions.append(trans)

        for state in self.states:
            if state.initial:
                self.initial = state.id

    def run_input_string(self, input_string, start_state=None):

        current_state = None
        if start_state is None:
            current_state = self.initial
        else:
            current_state = start_state

        if len(input_string) == 0:
            for s in self.states:
                if current_state == s.id:
                    if s.accept:
                        return True
                    return False
        input_char = input_string[0]
        # Look through all the transitions
        states_to_go = []
        for t in self.transitions:
            # If the state matches and the input matches

            if current_state == t.from_s and t.read == input_char:
                states_to_go.append(t.to_s)

        for s in states_to_go:
            res = self.run_input_string(input_string[1:], start_state=s)
            if res is True:
                return True

        return False


def make_and_run(filename, string, should_pass):
    tree = ET.parse(filename)

    root = tree.getroot()
    file_type = root[0]
    if string == "{empty}":
        string = ""
    if file_type.text == "turing":
        TM = TuringMachine(filename)
        try:
            if TM.run_input_string(string) == should_pass:
                return True
            return False
        except IndexError:
            return False

    try:
        dfa = DFA(filename)
        if dfa.run_input_string(string) == should_pass:
            return True
        return False
    except IndexError:
        return False


if __name__ == "__main__":
    from os import path
    with open(path.join("..", "grading_scripts", "assignments", "asgt10", "asgt10_8.txt"), 'r') as f:
        contents = f.read()
    tests = []
    for line in contents.split("\n"):
        if line is "":
            continue
        sections = line.split(" ")
        result = ""
        if sections[1] == "true":
            result = True
        else:
            result = False
        tests.append((sections[0], result))

    print(tests)

    print(make_and_run(path.join("..", "grading_scripts", "assignments", "asgt10", "resources", "asgt10-6.jff"), "(())", True))
