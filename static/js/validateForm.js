
function validateMobileNumber(){
    var mobileNumber = document.getElementById('settingsForm');
    
    var theNumber = mobileNumber.value;

    if(isNaN(theNumber)||theNumber.indexOf(" ")!=-1)
    {
       alert("Enter numeric value")
       mobileNumber.value = "";
       mobileNumber.focus();
       return false; 
    }
        if (theNumber.charAt(0)!="+")
    {
      alert("Cell no should start with +");
      mobileNumber.value = "";
      mobileNumber.focus();
      return false
    }
        
        if(theNumber.length < 13) 
        {
       alert("You have entered wrong number");
       mobileNumber.value = "";
       mobileNumber.focus();
       return false;
       }
        
        if(theNumber.length==0) 
        {
            alert("Please enter cell number");
            mobileNumber.value = "";
            mobileNumber.focus();
            return false;
        }
        
     return true;         
}

function validateSubdomain(){
	var elem = document.getElementById('subdomain');
	var thesubdomain = elem.value;
	if(thesubdomain.indexOf('.') == -1)
	{
	  elem.value = "";
	  elem.focus();
	  alert("the subdomain must contain a dot(.)");
	  return false;
	}
	return true;
}

function validateCreateEvent(){
	
	var eventTitleElem = document.getElementById('event_title');
	var audienceElem = document.getElementById('target_audience');
	var venueElem = document.getElementById('venue');
	var descriptionElem = document.getElementById('description');
	
	var eventTitle = eventTitleElem.value;
	var audience = audienceElem.value;
	var venue = venueElem.value;
	var description = descriptionElem.value;
	
	
	if (eventTitle.length < 1){
		alert("You must enter the event title")
		return false;
	}
	
	if (audience.length < 1){
		alert("You must specify the expected audience")
		return false;
	}
	
	if (venue.length < 1){
		alert("You must specify the venue")
		return false;
	}
	
	if (description.length < 1){
		alert("You must describe the event")
		return false;
	}
	
}

function searchEvents(){
	var searchElem = document.getElementById('search-box');
	var searchValue = searchElem.value;
	
	window.location = "/view/search_events/?q=" + searchValue;
}