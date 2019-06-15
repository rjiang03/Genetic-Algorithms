import random

#first define the weight and value of each box
X = [[20, 6], [30, 5], [60, 8], [90, 7], [50, 6], [70, 9], [30, 4]]

#define the limit of weight is 120
WEIGHT_LIMIT = 120

#define the chromosome class, each chromosome will have its own state, value and weight
class chromosome():
    def __init__(self):
        self.state = '0000000'
        self.value = 0
        self.weight = 0

#define 3 gloable value
#max_last is the max value until now
#diff_last is the difference bitween last two crossovers
#chromosome_max is the max chromosome
#times is the times of satisfy the finish condition, if it is the first time, using mutation
max_last = 0
max_g = 0
diff_last = 0
chromosome_max = chromosome()


#initialize the state with random state
def init():
    c1 = chromosome()
    c2 = chromosome()
    c3 = chromosome()
    c4 = chromosome()
    c5 = chromosome()
    c6 = chromosome()
    c1.state = '0100010'
    c2.state = '0010010'
    c3.state = '1100000'
    c4.state = '0100100'
    c5.state = '1010010'
    c6.state = '1100100'
    chromosome_states = [c1, c2, c3, c4, c5, c6]
    return chromosome_states

#calculate the values and weight for each chromosome
def fitness(chromosome_states):
    for chromosome_state in chromosome_states:
        value_sum = 0
        weight_sum = 0
        k = 0

        for i in chromosome_state.state:
            if int(i) == 1:
                weight_sum += X[k][0]
                value_sum += X[k][1]
            k = k + 1
            chromosome_state.value = value_sum
            chromosome_state.weight = weight_sum

    return chromosome_states

#filter the chromosome we don't want
#if its weight is larger than 120, change its value to zero
#sort the class based on it values, and discard last 50%
def filter(chromosome_states):
    global chromosome_max
    for i in chromosome_states:
        if i.weight > 120:
            i.value = 0

    chromosome_states = sorted(chromosome_states, key=lambda chromosome: chromosome.value)
    chromosome_states.reverse()

    chromosome_states = chromosome_states[0:6]
    if chromosome_states[0].value > chromosome_max.value:
        chromosome_max = chromosome_states[0]

    return chromosome_states

#define crossove
#each timem the chromosome in the list will randomly choose another chromosome to crossover
#each time will produce a random value as position, and change wither each other
#finally return a list with 12 chromosome, including the father generation and child generation
def crossover(chromosome_states):
    chromosome_states_new = chromosome_states
    idex = [1,2,3,4,5]
    c1 = chromosome()
    c2 = chromosome()
    c3 = chromosome()
    c4 = chromosome()
    c5 = chromosome()
    c6 = chromosome()

    i = random.randint(1, 5)
    idex.remove(i)
    idex2 = idex[random.randint(0, 3)]
    idex.remove(idex2)
    idex3 = idex[random.randint(0, 2)]
    idex.remove(idex3)

    j = random.randint(0, 6)
    k = random.randint(0, 6)
    l = random.randint(0, 6)

    c1.state = chromosome_states[0].state[0:j] + chromosome_states[i].state[j:7]
    c2.state = chromosome_states[i].state[0:j] + chromosome_states[0].state[j:7]
    c3.state = chromosome_states[idex[0]].state[0:k] + chromosome_states[idex[1]].state[k:7]
    c4.state = chromosome_states[idex[1]].state[0:k] + chromosome_states[idex[0]].state[k:7]
    c5.state = chromosome_states[idex2].state[0:l] + chromosome_states[idex3].state[l:7]
    c6.state = chromosome_states[idex3].state[0:l] + chromosome_states[idex2].state[l:7]

    c_w =  [c1, c2, c3, c4, c5, c6]
    chromosome_states_new = chromosome_states_new + c_w
    return chromosome_states_new

#judge whether it has finished
def is_finished(chromosome_states):
    global max_last
    global max_g
    global diff_last
    global chromosome_max_a

    max_current = 0
    for v in chromosome_states:
        if v.value > max_current:
            max_current = v.value
            #record the current max value
            if max_current > max_g:
                #update the gloable max value
                max_g = max_current
                chromosome_max_a = v.state
                # update the gloable max chromosome

    diff = abs(max_current - max_last)
    if diff <= 1 and diff_last <= 1:
        return True
    else:
        diff_last = diff
        max_last = max_current
        return False

#---------------------------------------------------------------------------------------------------------------------

chromosome_states = init()
#get the initialized chromosome
times = 0
#the times it meet the finish condition
while (1):
    chromosome_states = crossover(chromosome_states)
    chromosome_states = fitness(chromosome_states)
    chromosome_states = filter(chromosome_states)
    #keep doing the steps above, until it satify the follwoing requirement

    if is_finished(chromosome_states) and times == 1:
        print(chromosome_max_a)
        print(max_g)
        break

    elif is_finished(chromosome_states) and times == 0:
        #if it is the first time meet the requirement, doing mutation
        times = times + 1
        j = random.randint(0, 6)
        a = chromosome_states[0].state
        b = int(a[j])
        b = 1 - b
        b = str(b)
        #randomly choose a gene and change it
        chromosome_states[0].state = chromosome_states[0].state[0:j] + b + chromosome_states[0].state[j+1:7]
        filter(chromosome_states)

