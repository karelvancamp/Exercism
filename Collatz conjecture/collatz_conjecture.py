def collatz_steps(number):
    assert isinstance(number, int), "The input should be an integer"
    assert number > 0, "The input should be larger than 0"
    
    steps = 0
    while number > 1:
        steps += 1
        if number % 2:
            number = number*3 + 1
        else:
            number /= 2 
    
    return steps