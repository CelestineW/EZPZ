$(document).ready(function() {
    $("#getStarted").click(function() {
        $('html, body').animate({
            scrollTop: $("#inputArea").offset().top
        }, 500);
    });
    
    $("#addCourse").click(function() {
    	//$("#inputContainer").append($("#baseForm").html());
    });
    
});