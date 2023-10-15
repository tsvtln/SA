
##
# This module attempts to provide an interactive experience with the HPSA
# database that is analogous to that of the spinwrapper API.  Except this 
# module attempts to present data structures using the database's own schema,
# as opposed to super-imposing extra abstraction and naming conventions on top
# of it.
#
#   Example dbwrapper methods include things like:
#
#   Schema reflection properties.
#
#     db.tables
#     db.schemas
#     db.<schema>.tables
#     db.<schema>.<table_name>.child_tables
#     db.<schema>.<table_name>.parent_tables
#     db.<schema>.<table_name>.cols
#
#  Methods for querying for full table records.  These methods return a record
#  itterator:
#
#     db.<schema>.<table_name>.get_children(child_table)
#     db.<schema>.<table_name>.get_parents(parent_table)
#     db.<schema>.<table_name>.get_rec(k1, k2, kn, ...)
#     db.<schema>.<table_name>.get_recs(restrict, omit)
#
#  Methods for querying for specific columns of a table.  These methods return
#  an itterator:
#
#     db.<schema>.<table_name>.get_child_list(child_table, restrict, omit, cols)
#     db.<schema>.<table_name>.get_parent_list(parent_table, restrict, omit, cols)
#     db.<schema>.<table_name>.get_list(restrict, omit, cols)
#
#  Transaction semantics:
#
#     db.begin_transaction()  - return a tran_id
#     db.update(db_rec, mm_replicate=1, mm_force=0, mm_update_all=0, tran_id=None)
#     db.commit(tran_id) 
#
#  Any place a fully qualified table name would be used can be replaced with a
#  synonym.
#
