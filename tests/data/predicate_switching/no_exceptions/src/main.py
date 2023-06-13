from fauxpy import fauxpy_inst


def mainFunction(a):
    if fauxpy_inst.wrap_pred_to_switch(a > 1, "Pred_1"):
        return 1
    else:
        return -1
