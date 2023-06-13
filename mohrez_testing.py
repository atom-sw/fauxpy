from fauxpy.fauxpy_inst import predicate_switching as ps

# print(ps._PREDICATE_NAME)
# print(ps._INSTANCE_NUMBER)

retEvl = ps.wrap_pred_to_switch(1 == 2, "Pred1")
print(retEvl)

retEvl = ps.wrap_pred_to_switch(1 == 2, "Pred2")
print(retEvl)

retEvl = ps.wrap_pred_to_switch(1 == 2, "Pred1")
print(retEvl)

retEvl = ps.wrap_pred_to_switch(1 == 2, "Pred3")
print(retEvl)

retEvl = ps.wrap_pred_to_switch(1 == 2, "Pred1")
print(retEvl)

retEvl = ps.wrap_pred_to_switch(1 == 2, "Pred1")
print(retEvl)

retEvl = ps.wrap_pred_to_switch(1 == 2, "Pred1")
print(retEvl)

retEvl = ps.wrap_pred_to_switch(1 == 2, "Pred0")
print(retEvl)

# ps._incrementInstanceForPredicate("Pred1")
# ps._incrementInstanceForPredicate("Pred0")
# ps._incrementInstanceForPredicate("Pred3")
# ps._incrementInstanceForPredicate("Pred3")
# ps._incrementInstanceForPredicate("Pred3")
# ps._incrementInstanceForPredicate("Pred3")
# ps._incrementInstanceForPredicate("Pred3")
# ps._incrementInstanceForPredicate("Pred3")
# ps._incrementInstanceForPredicate("Pred2")
# ps._incrementInstanceForPredicate("Pred0")
# ps._incrementInstanceForPredicate("Pred1")
# ps._incrementInstanceForPredicate("Pred4")


