call create_database('feature', 'vasya');
call create_tables();
call insert_order(1, 1,1);
call insert_delivery(1,'rublevka',1890);
call insert_picture(1,'gek','rapka',1250);
select * from output_orders();
select * from output_delivery();
select * from output_pictures();
select * from find('gek');
call delete_record('orders',2);
call delete_by_name('gek');
call clear('delivery');
call clear_all_tables();
call delete_database('feature','vasya');
select * from current_database();
drop extension dblink
