import numpy as np
import datetime
import calculations.common as common

number_of_samples = 10
cycle_slip_threshold = 0.1
gap_threshold = 60 # 60 secs
length_threshold = 15 * 60 # 15 minut 


def gap_detector(epochs, out=None):
    if out == None:
        out = []
    arc_beg = epochs[0]
    for i in range(len(epochs)-1):
        if epochs[i+1] - epochs[i] > gap_threshold:
            out.append((arc_beg, epochs[i]))
            gap_detector(epochs[i+1:], out)
            break
        elif i == len(epochs) - 2:
            out.append((arc_beg, epochs[i+1]))
            break
    return out
        
            
def cycle_slip_detector(epochs, values, out=None):
    
    if out == None:
        out = []
    for i in range(1, len(epochs) - number_of_samples):
        end_i = i + number_of_samples
        current_epoch = epochs[end_i]
        poly = np.polyfit(epochs[i:end_i], values[i:end_i], deg=2)
        calculated_value = np.polyval(poly, current_epoch)
        if abs(values[end_i] - calculated_value) > cycle_slip_threshold:
            out.append(current_epoch)
            out.append(epochs[end_i+1])
            cycle_slip_detector(epochs[end_i+1:], values[end_i+1:], out)
            break
    return out
        
        
def length_detector(arcs):
    return [arc for arc in arcs if arc[1] - arc[0] > length_threshold]
            
            
def arc_detector(L4, MWWL):
    arcs = []
    values = []
    out = []
    epochs = sorted(L4)
    for epoch in epochs:
        values.append(L4[epoch])
    epochs_secs = [common.datetime_to_secs_of_day(x) for x in epochs]
    
    # Podziel ze względu na luki w danych
    gap_arcs = gap_detector(epochs_secs)
    # Podziel ze względy na cycle slip
    for gap_arc in gap_arcs:
        new_arcs = []
        new_arcs.append(gap_arc[0])
        new_arcs.append(gap_arc[1])
        arc_beg_i = epochs_secs.index(gap_arc[0])
        arc_end_i = epochs_secs.index(gap_arc[1])
        cycle_slips = cycle_slip_detector(epochs_secs[arc_beg_i:arc_end_i], values[arc_beg_i:arc_end_i])
        new_arcs += cycle_slips
        new_arcs.sort()
        new_arcs = [(new_arcs[i], new_arcs[i+1]) for i in range(len(new_arcs)-1)]
        arcs += new_arcs
    # Sprawdz długość łuków
    arcs = length_detector(arcs)

    # Zmian sekundy tygodnia na datetime
    current_day = datetime.datetime(year=epochs[0].year, month=epochs[0].month, day=epochs[0].day)
    for arc in arcs:
        arc_beg = arc[0]
        arc_end = arc[1]
        new_arc = (current_day + datetime.timedelta(seconds=arc_beg), current_day + datetime.timedelta(seconds=arc_end))
        out.append(new_arc)
    return out
     