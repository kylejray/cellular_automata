import random
from matplotlib import pyplot as plt

def in_binary(rule_number):
    '''
    Returns an 8 bit binary string representation of an integer. 
    
    Parameters
    ----------
    rule_number: int
        The number to be converted
        
    Returns
    -------
    out: string
        8bit binary string representation of integer
    '''
    in_binary = bin(rule_number)[2:][::-1]
    binary_length = len(in_binary)
    if binary_length != 8:
        padding = 8 - binary_length
        in_binary = in_binary + '0'*padding
    return in_binary



def random_state(length, alphabet_size):
    '''
    Parameters
    ---------
    length: int
        how many cells you want in your state
    alphabet_size: int
        how mant options for each cell
        
    Returns
    -------
    state: list
    a random list of <length> integers between 0 and <alphabet_size>-1
    '''
    return [random.randint(0,alphabet_size-1) for _ in range(length)]

def next_state(current_state, lookup_table):
    '''
    Parameters
    ----------
    current_state: list
        configuration to be iterated
    lookup_table: dict
        allows the function to look up what sylbols are associated with different neighborhoods
    Returns
    -------
    new_state: list
    a new configuaration based on the lookup table and neighborhood size
    '''
    length = len(current_state)
    new_state = []
    for i in range(len(current_state)):
    #sweeps through the state, using lookup_table to build the next state based on the ith, (i-1)th, and (i+1)th cells
        neighborhood = (current_state[(i-1)], current_state[i], current_state[(i+1)%length])
        new_state.append(int(lookup_table[neighborhood]))
    return(new_state)


    def in_ternary(number):
    '''
    Returns an 8 bit binary string representation of an integer. 
    
    Parameters
    ----------
    number: positive int <= 19682
        The number (positive integer) to be converted
        
    Returns
    -------
    out: list
        ternary represenation of a number with inverted order (smallest digits first)
    '''

    assert number >= 0 and number <= 19682, ' only converts positive integers in [0,19682], inclusive'
    out=[]

    for j in range(9):
        i=8-j
        if (number - 2*3**i) >= 0 :
            out.append(2)
            number = number - 2*3**i
        elif (number - 3**i) >= 0:
            out.append(1)
            number = number - 3**i
        elif (number- 3**i < 0):
            out.append(0)
    return(out[::-1])

default_neighborhoods = [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]

class CA_map:

    def __init__(self, neighborhoods= default_neighborhoods, alphabet_size = 2):
        '''
        Parameters
        ----------
        neighborhoods: list
            distinct neighborhoods in  lexicographical order
        alphabet_size: 2 or 3
            2 for binary, 3 for ternary CA
        Attributes
        ----------
        neighborhoods: list
            see above
        alphabet_size: list
            see above
        rule_number: string(binary) or list(ternary)
            a function that takes a rule number to a binary(ternary) representation
        '''
        self.neighborhoods = neighborhoods
        self.alphabet_size = alphabet_size
        assert alphabet_size == 2 or alphabet_size ==3, 'binary and ternary only'
        if alphabet_size == 2:
            self.rule_number = in_binary
        if alphabet_size == 3:
            self.rule_number = in_ternary
            
    def lookup_table(self, N):
        '''
        Parameters
        ----------
        N: int
            the rule number
        Returns
        ---------
        lookup_table : dict
            a dictionary that uses the rule number to generate dynamics for each neighborhood
        '''
        string = self.rule_number(N)
        assert len(string) <= len(self.neighborhoods), 'rule number too large'
        return dict(zip(self.neighborhoods, string))


def next_state_ternary(current_state, lookup_table):
    '''
    Parameters
    ----------
    current_state: list
        configuration to be iterated
    lookup_table: dict
        allows the function to look up what sylbols are associated with different neighborhoods
    
    Returns
    -------
    new_state: list
    a new configuaration based on the lookup table and neighborhood size
    '''

    length = len(current_state)
    new_state = []
    
    #sweeps through the state, using lookup_table to build the next state based on the ith and (i-1)th cells
    for i in range(len(current_state)):
        neighborhood = (current_state[(i-1)], current_state[i])
        new_state.append(int(lookup_table[neighborhood]))
    return(new_state)

def simulate_lattice(length, time, CA_map, rule):
    '''
    Parameters
    ----------
    length: int
        number of cells in a state
    time: int
        how many timesteps to run
    CA_map: class instance
        for generating the right lookup table
    rule: int
        the rule number, 0-255 for binary and 0-19682 for ternary
    Retuns
    ------
    shows a picture, returns nothing
    '''
    lookup_table = CA_map.lookup_table(rule) 
    field=[]
    current_state = random_state(length, CA_map.alphabet_size)
    field.append(current_state)
    # For each time step, we generate a new state using next_state, then append it to the field and set it to our current state
    for i in range(time):
        # We have to check if we are doing the binary ot ternary case, because they look at different neighborhoods to iterate
        if CA_map.alphabet_size == 3:
            current_state = next_state_ternary(current_state, lookup_table)
        if CA_map.alphabet_size == 2:
            current_state = next_state(current_state, lookup_table)
        field.append(current_state)
        
    #plot the field
    plt.figure(figsize=(12,12))
    plt.imshow(field, cmap=plt.cm.Greys, interpolation='nearest')
    plt.show()
    