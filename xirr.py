'''

A single function that calculates IRR using Newton's Method

'''



from datetime import date



def xirr(transactions):



    '''

    Calculates the Internal Rate of Return (IRR) for an irregular series of cash flows (XIRR)

    Takes a list of tuples [(date,cash-flow),(date,cash-flow),...]

    Returns a rate of return as a percentage

    '''



    years = [(ta[0] - transactions[0][0]).days / 365. for ta in transactions]

    residual = 1.0

    step = 0.05

    guess = 0.05

    epsilon = 0.0001

    limit = 10000

    while abs(residual) > epsilon and limit > 0:

        limit -= 1

        residual = 0.0

        for i, trans in enumerate(transactions):

            residual += trans[1] / pow(guess, years[i])

        if abs(residual) > epsilon:

            if residual > 0:

                guess += step

            else:

                guess -= step

                step /= 2.0

    return guess - 1



tas = [(date(2006, 1, 24), -39967),

       (date(2008, 2, 6), -19866),

       (date(2010, 10, 18), 245706),

       (date(2013, 9, 14), 52142)]



if __name__ == '__main__':

    print(tas,)

    print("IRR for test data = {:.2%}".format(xirr(tas)))