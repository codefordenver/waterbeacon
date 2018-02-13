from log import log

class nsf_water_quality_index_calc(object):


    def __init__(self):
        # REF: http://home.eng.iastate.edu/~dslutz/dmrwqn/water_quality_index_calc.htm
        pass

    def calc(self,
             dissolved_oxygen = None,
             fecal_coliform = None,
             ph = None,
             biochemical_oxygen_demand = None,
             temperature_change = None,
             total_phosphate = None,
             nitrates = None,
             turbidity = None,
             total_solids = None):
        ''' this method calculates the water quality index '''

        return 0


if __name__ == "__main__":
    nsf = nsf_water_quality_index_calc()
    log( "NSF Water Quality Index: %s" % nsf.calc(),"success")
