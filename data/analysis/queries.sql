drop table tickets;
CREATE TABLE tickets (
    infraction_date date,
    time_of_infraction integer,
    infraction_code integer,
    infraction_description text,
    fine_amt integer,
    location1 varchar(10),
    location2 varchar(50),
    province varchar(5)
)
;



CREATE INDEX tickets_loc ON tickets (location2);
CREATE INDEX tickets_code ON tickets (infraction_code);

ANALYZE tickets (location2);
ANALYZE tickets (infraction_code);

select * from tickets limit 10
