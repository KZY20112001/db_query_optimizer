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

def reset_settings(query_settings):
    for rule in query_settings:
        query_settings[rule] = True

def print_stats(plan):
    startup_cost = plan['Startup Cost']
    total_cost = plan['Total Cost']
    plan_row = plan['Plan Rows']
    plan_width = plan['Plan Width']

    stats = (
        f"Estimated Startup Cost: {startup_cost}\n"
        f"Estimated Total Cost: {total_cost}\n"
        f"Estimated Plan Rows: {plan_row}\n"
        f"Estimated Tuple Size: {plan_width}"
    )

    return stats


def compare_cost(qep, aqp):

    qep_output = (
        f"QEP:\n"
        f"Estimated Startup Cost: {qep['Startup Cost']}\n"
        f"Estimated Total Cost: {qep['Total Cost']}\n"
        f"Estimated Plan Rows: {qep['Plan Rows']}\n"
        f"Estimated Tuple Size: {qep['Plan Width']}\n"
    )

    aqp_output = (
        f"AQP:\n"
        f"Estimated Startup Cost: {aqp['Startup Cost']}\n"
        f"Estimated Total Cost: {aqp['Total Cost']}\n"
        f"Estimated Plan Rows: {aqp['Plan Rows']}\n"
        f"Estimated Tuple Size: {aqp['Plan Width']}\n"
    )

    difference_output = (
        f"Difference:\n"
        f"Estimated Startup Cost: {aqp['Startup Cost'] - qep['Startup Cost']}\n"
        f"Estimated Total Cost: {aqp['Total Cost'] - qep['Total Cost']}\n"
        f"Estimated Plan Rows: {aqp['Plan Rows'] - qep['Plan Rows']}\n"
        f"Estimated Tuple Size: {aqp['Plan Width'] - qep['Plan Width']}\n"
    )
    return qep_output, aqp_output, difference_output



def compare_qp(qep, aqp):
    if qep is not None and aqp is not None:
        if qep == aqp:
            print("No modification made")
            qep_stats = print_stats(qep)
            print (qep_stats)
            return qep_stats, None, None
        else:
            qep_stats, aqp_stats, difference = compare_cost(qep, aqp)
            print(qep_stats)
            print(aqp_stats)
            print(difference)
            return qep_stats, aqp_stats, difference




        