query_settings = {
    'enable_async_append': True,
    'enable_bitmapscan': True,
    'enable_gathermerge': True,
    'enable_group_by_reordering': True,
    'enable_hashagg': True,
    'enable_hashjoin': True,
    'enable_incremental_sort': True,
    'enable_indexscan': True,
    'enable_indexonlyscan': True,
    'enable_material': True,
    'enable_memoize': True,
    'enable_mergejoin': True,
    'enable_nestloop': True,
    'enable_parallel_append': True,
    'enable_parallel_hash': True,
    'enable_partition_pruning': True,
    'enable_partitionwise_join': True,
    'enable_partitionwise_aggregate': True,
    'enable_presorted_aggregate': True,
    'enable_seqscan': True,
    'enable_sort': True,
    'enable_tidscan': True,
}

scan_join_nodes = ['Seq Scan', 'Index Only Scan', 'Index Scan', 'Bitmap Heap Scan', 'Bitmap Index Scan']

def print_stats(plan):
    startup_cost = plan['Startup Cost']
    total_cost = plan['Total Cost']
    plan_row = plan['Plan Rows']
    plan_width = plan['Plan Width']

    print(f"Startup Cost: {startup_cost}")
    print(f"Total Cost: {total_cost}")
    print(f"Plan Rows: {plan_row}")
    print(f"Tuple Size: {plan_width}")  

def compare_cost(qep, aqp):
    qep_startup_cost = qep['Startup Cost']
    qep_total_cost = qep['Total Cost']
    qep_plan_row = qep['Plan Rows']
    qep_plan_width = qep['Plan Width']

    aqp_startup_cost = aqp['Startup Cost']
    aqp_total_cost = aqp['Total Cost']
    aqp_plan_row = aqp['Plan Rows']
    aqp_plan_width = aqp['Plan Width']

    print("QEP:")
    print(f"Startup Cost: {qep_startup_cost}")
    print(f"Total Cost: {qep_total_cost}")
    print(f"Plan Rows: {qep_plan_row}")
    print(f"Tuple Size: {qep_plan_width}") 

    print("AQP:")
    print(f"Startup Cost: {aqp_startup_cost}")
    print(f"Total Cost: {aqp_total_cost}")
    print(f"Plan Rows: {aqp_plan_row}")
    print(f"Tuple Size: {aqp_plan_width}")

    print("Difference:")
    print(f"Startup Cost: {aqp_startup_cost - qep_startup_cost}")
    print(f"Total Cost: {aqp_total_cost - qep_total_cost}")
    print(f"Plan Rows: {aqp_plan_row - qep_plan_row}")
    print(f"Tuple Size: {aqp_plan_width - qep_plan_width}")



def compare_qp(qep, aqp):
    if qep is not None and aqp is not None:
        if qep == aqp:
            print("No modification made")
            qep_plan = qep[0][0][0]['Plan']
            print_stats(qep_plan)

            sub_plan = qep_plan['Plans'][0]
            print_stats(sub_plan)

        else:
            qep_plan = qep[0][0][0]['Plan']
            aqp_plan = aqp[0][0][0]['Plan']
            compare_cost(qep_plan, aqp_plan)
            print(aqp_plan)




        