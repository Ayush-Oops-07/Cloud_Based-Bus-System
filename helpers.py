import random, string

def generate_pnr(n=8):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=n))

def seat_map(total_seats, per_row=4):
    # returns list of seat numbers as strings: 1..total_seats
    return [str(i) for i in range(1, total_seats + 1)]
