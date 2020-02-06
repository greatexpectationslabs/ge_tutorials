



select count(*)
from (

    select
        id

    from "demo_db"."public"."my_first_dbt_model"
    where id is not null
    group by id
    having count(*) > 1

) validation_errors

