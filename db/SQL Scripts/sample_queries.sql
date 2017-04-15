
-- Select all section information for every section of CMSC 202

SELECT section.course_id, course.title, section.sec_id, professor.last_name, professor.first_name, section.room_num, time_slot.days, time_slot.start_hr, time_slot.start_min, time_slot.end_hr, time_slot.end_min
FROM course
	INNER JOIN section
		ON section.course_id = course.course_id
	INNER JOIN professor
		ON section.prof_id = professor.prof_id
	INNER JOIN time_slot
		ON section.time_slot_id = time_slot.time_slot_id
WHERE section.course_id = "CMSC 202";


-- Select all section information for every section of CMSC 202 that starts at or after noon

SELECT section.course_id, course.title, section.sec_id, professor.last_name, professor.first_name, section.room_num, time_slot.days, time_slot.start_hr, time_slot.start_min, time_slot.end_hr, time_slot.end_min
FROM course
	INNER JOIN section
		ON section.course_id = course.course_id
	INNER JOIN professor
		ON section.prof_id = professor.prof_id
	INNER JOIN time_slot
		ON section.time_slot_id = time_slot.time_slot_id
WHERE section.course_id = "CMSC 202"
	AND start_hr >= 12;