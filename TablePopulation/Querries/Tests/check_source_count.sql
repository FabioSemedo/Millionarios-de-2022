--Queck if Source was atomised correctly
select a.num,b.num, c.num, d.num, s.num, s.num - a.num - b.num - c.num
From (select count(*) as num from test) a
    ,(select count(*) as num from test where source like "%,%") b
    ,(select count(*) as num from test where source like "%,%,%") c
    ,(select count(*) as num from test where source like "%,%,%,%") d
    ,(select count(*) as num from Sources) s