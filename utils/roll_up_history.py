config = {
    'table_schema': 'vldw33869_wrk',
    'table_name': 'order',
    'primary_key': ['order_rk'],
    'version_from': 'valid_from_dttm',
    'version_to': 'valid_to_dttm',
    'skipped_fields': [],
    'wrk_schema': 'vldw33869_wrk',
    'task_num': '33869',
    'columns': ['order_rk', 'order_id', 'party_rk', 'created_dttm',
    'order_status_cd', 'deleted_flg', 'confirm_dttm', 'pay_amt',
    'valid_from_dttm', 'valid_to_dttm', 'item_units_cnt',
    'application_rk', 'application_id', 'application_dttm',
    'partner_nm', 'account_rk', 'contract_number', 'open_dt',
    'close_dt', 'real_close_dt', 'cpss_create_dttm']
}

def get_roll_up_query(**kwargs):
        res = []
        skipped_fields = [
            *kwargs.get('primary_key'),
            *kwargs.get('skipped_fields'),
            kwargs.get('version_from'),
            kwargs.get('version_to')
        ]
        tracked_field_list = filter(
            lambda x: 0 if x in skipped_fields else 1,
            kwargs.get('columns')
        )
        rh_step1_table = f"rh_flg_dw{kwargs.get('task_num')}"
        primaty_keys = ','.join(kwargs.get('primary_key'))
        query = f"""create table {kwargs.get('table_schema')}.{rh_step1_table} as
select *, least("""
        res.append(query)
        for i in tracked_field_list:
            query = f"\tdecode({i}, lag({i}) over (partition by {primaty_keys} order by {kwargs.get('version_from')}), 1, 0),"
            res.append(query)
        res[-1] = res[-1][:-1]
        query = f""") as del_flg
from {kwargs.get('table_schema')}.{kwargs.get('table_name')};"""
        res.append(query)
        res.append('\n')
        rh_step2_table = f"rh_dw{kwargs.get('task_num')}"
        query = f"""create table {kwargs.get('table_schema')}.{rh_step2_table} as
select"""
        res.append(query)
        fields_wo_versioning = kwargs.get('columns')[:]
        if kwargs.get('version_from') in fields_wo_versioning:
            fields_wo_versioning.remove(kwargs.get('version_from'))
        if kwargs.get('version_to') in fields_wo_versioning:
            fields_wo_versioning.remove(kwargs.get('version_to'))
        for i in fields_wo_versioning:
            query = f"\t{i},"
            res.append(query)
        query = f"\t{kwargs.get('version_from')},"
        res.append(query)
        query = f"""\tcoalesce(lead({kwargs.get('version_from')} - interval '1 second', 1) over (partition by {primaty_keys} order by {kwargs.get('version_from')}), '5999-01-01'::timestamp) as {kwargs.get('version_to')}
from {kwargs.get('table_schema')}.{rh_step1_table}
where del_flg = 0;"""
        res.append(query)
        return '\n'.join(res)
