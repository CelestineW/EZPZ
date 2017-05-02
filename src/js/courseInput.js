$(document).ready(function() {
	
	var MAX_COURSES = 5;
	
	//Get the html from template
	$('<div/>', {
		'class' : 'newCourse', html: GetHtml()
    }).appendTo('#inputContainer'); 
    
	//add course fields to container, check if at max
    $('#addCourse').click(function () {
    	var len = $('.newCourse').length;
    	if(len >= MAX_COURSES){
    		//console.log("Notice course max");
    		$('#inputNotification').show();
    	} else { 
    		
    		//Get the html from template and hide and slideDown for transtion.
	        $('<div/>', {
	            'class' : 'newCourse', html: GetHtml()
	        }).hide().appendTo('#inputContainer').slideDown('slow'); 
    	}
    	console.log("len = %d", len);
    });
    
    //handle form submission
    $('#submitCourses').click(function () {
    	//formatInputData();
    });
    
    //remove course, check notification
    $(document).on("click", "#removeCourse", function() {
        $(this).parent().parent().remove();
        if($('.newCourse').length < MAX_COURSES){
        	$('#inputNotification').hide();
        }
    });
 })
 
//Get the template and update the input field names
function GetHtml() {
    var len = $('.newCourse').length;
    console.log(len);
    var $html = $('.courseInputTemplate').clone();
    
    //make field names unique
    $html.find("input[name=courseName]")[0].name="courseName"+len;
    var $priorityFields = $html.find("select[name=priority]");
    console.log($priorityFields);
    for(i = 0; i < $priorityFields.length; i++){
    	$priorityFields[i].name="priority"+len;
    }
    //$html.find("button[name=removeCourse]")[0].name="removeCourse" + len;
    
    return $html.html();    
}
    
//Form submission handling
function onSubmit(form){
  var data = JSON.stringify($(form).serializeArray() );
  //console.log(data);
  var formattedData = formatInputData(data);
  console.log("Formatted:");
  console.log(JSON.stringify(formattedData));
  
  //Handle formattedData
  return false; 
}

//Format input JSON
function formatInputData(data){
	var dataArray = JSON.parse(data);
	console.log("Raw:");
	console.log(JSON.stringify(dataArray));
	
	var result = {
	       "schedule_request" : "request",
	       "history" : 0,
	       "course_amount" : 0,
	       "desired_course_amount":0,
	       "courses_input" : []
	};
	
	//Parse JSON in order
	var len = dataArray.length;
	var desiredCourseAmount = dataArray[len-1].value;
	var totalCourseAmount = Math.ceil((dataArray.length - 1) / 2);
	
	//console.log("dataArray length: %d", len);
	//console.log("desired course amount: %d", desiredCourseAmount);
	//console.log("total course amount: %d", totalCourseAmount);
	
	result.desired_course_amount = desiredCourseAmount;
	result.course_amount = totalCourseAmount;
	for(var i = 0; i < totalCourseAmount; i++){
		var courseString = "course"+i;
		var baseIndex = i*2;
		var temp = {
			courseString : {
				"course_name" : dataArray[baseIndex].value,
				"priority" : dataArray[baseIndex+1].value
			}
		}
		result.courses_input.push(temp);
	}
	return result;
}


