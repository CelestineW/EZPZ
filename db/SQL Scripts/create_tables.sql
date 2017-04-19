use ScheduleMe;

create table course
	(course_id		varchar(9), 
	 title			varchar(150) not null, 
	 primary key (course_id)
	);

create table professor
	(prof_id	int, 
	 last_name	varchar(50) not null,
	 first_name varchar(50) not null,
	 primary key (prof_id)
	);

create table time_slot
	(time_slot_id	int,
	 days			varchar(7) not null,
	 start_hr		numeric(2) not null check (start_hr >= 0 and start_hr < 24),
	 start_min		numeric(2) not null check (start_min >= 0 and start_min < 60),
	 end_hr			numeric(2) not null check (end_hr >= 0 and end_hr < 24),
	 end_min		numeric(2) not null check (end_min >= 0 and end_min < 60),
	 primary key (time_slot_id)
	);
	
create table section
	(course_id		varchar(9),
     sec_id			int,
	 semester		varchar(6)
	 check (semester in ('Fall', 'Winter', 'Spring', 'Summer')), 
	 year			numeric(4) check (year > 2000 and year < 2100),
	 time_slot_id	int,
	 prof_id		int default 0,
	 room_num		varchar(10) default 'UNKWN',
	 primary key (course_id, sec_id, semester, year),
	 foreign key (course_id) references course (course_id) on delete cascade,
	 foreign key (time_slot_id) references time_slot (time_slot_id) on delete set null,
	 foreign key (prof_id) references professor (prof_id) on delete set null
	);