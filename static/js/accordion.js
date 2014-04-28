// JavaScript Document
$(document).ready(function(){
	
	$(".accordion h3:first").addClass("active");
	$(".accordion form:not(:first)").hide();

	$(".accordion h3").click(function(){
		$(this).next("form").slideToggle("slow")
		.siblings("form:visible").slideUp("slow");
		$(this).toggleClass("active");
		$(this).siblings("h3").removeClass("active");
	});

});