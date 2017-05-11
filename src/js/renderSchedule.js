$(document).ready(function() {
	var regenCount = 0;
	$('#regenerate').hide();
	$('#regenExhausted').hide();
	
	$('#submitCourses').click(function(){
		console.log("regenCount: %d", regenCount);
		$('#calendar').fullCalendar(renderSchedule(makeDummy()));
		$('#regenerate').show().slideDown(); 
	});
	
	$('#regenerate').click(function(){
		regenCount++;
		//console.log("regenCount: %d", regenCount);
		$('#calendar').fullCalendar('removeEvents');
		
		//Callback to scheduling function simulated by below
		if (regenCount >= 9){
			$('#regenExhausted').show();
			regenCount -= 9;
			regenCount++;
		}
		switch(regenCount){
			case 1:
				$('#calendar').fullCalendar('addEventSource', renderSchedule(makeDummy2()).events);
				break;
			case 2:
				$('#calendar').fullCalendar('addEventSource', renderSchedule(makeDummy3()).events);
				break;
			case 3:
				$('#calendar').fullCalendar('addEventSource', renderSchedule(makeDummy4()).events);
				break;
			case 4:
				$('#calendar').fullCalendar('addEventSource', renderSchedule(makeDummy5()).events);
				break;
			case 5:
				$('#calendar').fullCalendar('addEventSource', renderSchedule(makeDummy6()).events);
				break;
			case 6:
				$('#calendar').fullCalendar('addEventSource', renderSchedule(makeDummy7()).events);
				break;
			case 7:
				$('#calendar').fullCalendar('addEventSource', renderSchedule(makeDummy8()).events);
				break;
			case 8:
				$('#calendar').fullCalendar('addEventSource', renderSchedule(makeDummy9()).events);
				break;
			case 9:
				$('#calendar').fullCalendar('addEventSource', renderSchedule(makeDummy10()).events);
				break;
			default:
				$('#calendar').fullCalendar('removeEvents');
		}
		//$('#calendar').fullCalendar( 'refetchEvents' );
	});
});

//START AND END DATE FOR SEMESTER HARDCODED, need identifier to make this automatic
function renderSchedule(scheduleObj){
	
	//var testObj = makeDummy();
	
	/*
	//Will have to modify if semester changes
	var baseDate = new Date("September 1, 2016 00:00:00");
	var endDate = new Date("December 16, 2016 00:00:00");
	*/
	
	 //Spring Semester Values Below
	 var baseDate = new Date("January 30, 2017 00:00:00");
	 var endDate = new Date("May 15, 2017 00:00:00");
	 
	
	var baseYear = baseDate.getFullYear();
	var baseMonth = baseDate.getMonth() + 1;
	var baseNum = baseDate.getDate();
	var baseDay = baseDate.getDay();
	var baseDateString = buildDateString(baseYear, baseMonth, baseNum, "13:00");
	
	//Consumed by fullCalendar
	var displayObj = {
			header: {
				left: 'prev,next today',
				center: 'title',
				right: 'month,agendaWeek,agendaDay,listWeek'
			},
			defaultDate: '2017-01-30',
			minTime: "07:00:00",
			maxTime: "21:00:00",
			allDaySlot: false,
			navLinks: true, // can click day/week names to navigate views
			editable: false,
			eventLimit: true, // allow "more" link when too many events
			events: []
	}
	
	//Finish building, add events
	var allCounter = 0;
	
	for(var i = 0; i < scheduleObj.course_amount; i++){
		// Find all days for a course through end of semester
		// Fall End: Dec 16th
		// Spring End: May 16th
		
		//Render scheduled courses only
		if(scheduleObj.course_result[i].course_scheduled == 1){
			var currentCourse = scheduleObj.course_result[i].course_title;
			var currentCourseDays = scheduleObj.course_result[i].day_of_week;
			var currentCourseStart = scheduleObj.course_result[i].start_time;
			var currentCourseEnd = scheduleObj.course_result[i].end_time;
			
			console.log(currentCourse);
			console.log(currentCourseDays);
			console.log(currentCourseStart);
			console.log(currentCourseEnd);
			
			var meetingDates = findAllClassDates(currentCourseDays, baseDate, endDate);
	
			for(var j = 0; j < meetingDates.length; j++){
				
				//console.log("Meeting date:");
				//console.log(meetingDates[i]);
				
				//Add each as an event
				tempStartStr = buildDateString(meetingDates[j].getFullYear(), meetingDates[j].getMonth()+1,
											   meetingDates[j].getDate(), currentCourseStart);
				tempEndStr = buildDateString(meetingDates[j].getFullYear(), meetingDates[j].getMonth()+1,
						                     meetingDates[j].getDate(), currentCourseEnd);
				temp = {
						title: currentCourse,
						start: tempStartStr,
						end: tempEndStr
					   }
				//console.log(temp);
				
				//Add date to calendar
				displayObj.events[allCounter] = temp;
				allCounter++;
			}
		}
	}
	
	console.log("Schedule object is:");
	console.log(JSON.stringify(scheduleObj));
	return displayObj;
}

//Before:      2016, 9, 1, 1:00 
//After:	   2016-09-01T13:00:00
function buildDateString(year, monthNum, dayNum, timeString){
	var result = "";
	var yearStr = "";
	var monthStr = "";
	var dayStr = "";
	var timeStr = "";
	
	//Trivial build year
	yearStr = year.toString();

	//Build Month
	if(monthNum < 10){
		monthStr += "0";
	} 
	monthStr += monthNum.toString();
	
	//console.log("monthStr is:");
	//console.log(monthStr);
	
	//Build day
	if(dayNum < 10){
		dayStr += "0";
	}
	dayStr += dayNum.toString();
	//console.log("dayStr is:");
	//console.log(dayStr);
	
	//Build Time, might change depending on how AM/PM is represented
	/*
	//Presently, anything before 8:00 is considered PM, will be converted
	var timeParts = timeString.split(':');
	var timeValue = parseInt(timeParts[0])
	if( timeValue < 8){
		timeValue += 12;
	}

	timeStr += timeValue.toString();
	timeStr += ":";
	timeStr += timeParts[1];
	timeStr += ":00";
	console.log("timeStr is:");
	*/
	
	//If timeSting is already in military time
	timeStr += timeString;
	timeStr += ":00" 
	 
	//console.log(timeStr);
	
	result += yearStr;
	result += "-";	
	result += monthStr;
	result += "-";
	result += dayStr;
	result += "T";
	result += timeStr;
	
	//console.log("Total:");
	//console.log(result);
	
	return result;
}

//Return list of all dates in time period for particular day
//ex findDayNums(1, baseDate obj, endDateObj)
//Finds all Mondays in date range
function findDates(dayOfWeek, baseDate, endDate){
	var datesFound = [];
	//var firstDay = new Date(baseDate.getTime());
	var tempDay = new Date(baseDate.getTime());
	
	//Find first day
	while(tempDay <= endDate){
		if(tempDay.getDay() == dayOfWeek){
			var firstDay = new Date(tempDay.getTime());
			datesFound.push(firstDay);
			break;
		}
		var nextDay = tempDay.setDate(tempDay.getDate() + 1);
		tempDay = new Date(tempDay);
	}
	
	var tempDay = new Date(firstDay.getTime());
	
	//Find the rest by looping through by week
	while(tempDay <= endDate){
		datesFound.push(tempDay);
		var nextDay = tempDay.setDate(tempDay.getDate() + 7);
		tempDay = new Date(nextDay);
	}
	
	//Remove last beyond range, not sure why bound check isn't working...
	datesFound.pop();
	
	console.log(datesFound);
	
	return datesFound;
}

//'MTWRF' -> corresponding number matching date.getDay()
function dateChar2Num(char){
	switch(char){
		case "M":
			return 1;
			break;
		case "T":
			return 2;
			break;
		case "W":
			return 3;
			break;
		case "R":
			return 4;
			break;
		case "F":
			return 5;
			break;
		default:
			return -1;
	}
}

//Find all meeting dates & time by dayString in range
function findAllClassDates(dayString, baseDate, endDate){
	var dayArray = dayString.split('');
	var totalDates = [];
	var tempDates = [];
	
	//Validate dayString ideally
	if(/^[FMRTW]{1,5}$/.test(dayString) == false){
		console.log("Regex mismatch in dayString");
		return totalDates;
	}
		
	//For each day of the week in string, find all dates in range
	for(var i = 0; i < dayArray.length; i++){
		tempDates = findDates(dateChar2Num(dayArray[i]), baseDate, endDate);
		totalDates = totalDates.concat(tempDates);
	}
	return totalDates;
}