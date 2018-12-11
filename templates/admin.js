'use strict';
function saveResponse()
{
	console.log('SaveResponse Entry');
	var feedbackA = JSON.parse(localStorage.getItem('Feedback'));
	if (feedbackA == null)
	{
		feedbackA = [];
	}
	var idx=parseInt(document.getElementById('tx_index').value);
	if (idx <0 || idx >= feedbackA.length)
	{
		alert('Error');
		return;
	}
	var item = feedbackA[idx];
	item.Response = document.getElementById('tx_response').value;
	feedbackA[idx]=item;
	localStorage.setItem('Feedback',JSON.stringify(feedbackA));
	DisplayFeedbacks();
	console.log('SaveResponse Exit');
}

function setRes(idx)
{
	document.getElementById('tx_index').value = idx;
	document.getElementById('tx_response').focus();
}

function saveMe()
{
	console.log('SaveMe Entry');
	var feedbackA = JSON.parse(localStorage.getItem('Feedback'));
	if (feedbackA == null)
	{
		feedbackA = [];
	}
	var tempO = { Feedback : document.getElementById('tx_feedback').value, Response : '' };
	feedbackA.push(tempO);
	console.log('arraylen='+feedbackA.length);
	localStorage.setItem('Feedback',JSON.stringify(feedbackA));
	DisplayFeedbacks();
	console.log('SaveMe Exit');
}
function displayFeedbacks()
{
	console.log('DisplayFeedbacks Entry');
	var feedbackA = JSON.parse(localStorage.getItem('Feedback'));
	if (feedbackA == null)
	{
		feedbackA = [];
	}
	console.log('arraylen='+feedbackA.length);
	var tempS = "";
	tempS += "<table border='1' class='faq_table_design'>";
	for(var i=0 ; i < feedbackA.length; i++)
	{
		var item = feedbackA[i];
		tempS += "<tr><td>";
		tempS += "Feedback:<br/>"+item.Feedback+"<br/><br/>Resposne<br/>"+item.Response;
		tempS += "<input type='button' value='res' onclick='setRes("+i+")'/>";
		tempS += "</td></tr>";
	}
	tempS += "</table>";
	console.log("tempS="+tempS);
	document.getElementById('span_table').innerHTML = tempS;
	console.log('DisplayFeedbacks Exit');
	
}


var qnArray = []; //save admin-added questions
/*
* Question object to add new questions
*/
function Question(qnText, possibleAnswers, correctAnswers, type){
	this.qnText = qnText;
	this.possibleAnswers = possibleAnswers;
	this.correctAnswers = correctAnswers;
	this.whatType = type;
}
function generate(){
	var number = document.getElementById("optionsNumber").value;
	console.log("pass1");
	document.getElementById("qn_input").innerHTML = "";
	for(var i=0; i<number; i++){
		console.log("pass loop" + i);
		var t = document.createElement("input");
		t.setAttribute("id", "box_" + i);
		//t.setAttribute("required", "required");
		t.append(document.createTextNode("[" + i + "]"));
		var s = document.createElement("input");
		s.setAttribute("type", document.getElementById("qnTypeSelect").value);
		s.setAttribute("id", "inputType_" + i);
		s.setAttribute("name", "rycbar");
		document.getElementById("qn_input").append(t);
		document.getElementById("qn_input").append(s);
		document.getElementById("qn_input").append(document.createElement("br"));
	}
	var confirm = document.createElement("input");
	confirm.setAttribute("type", "button");
	confirm.setAttribute("value", "Add questions");
	confirm.setAttribute("onclick", "saveQuestions()");
	document.getElementById("qn_input").append(confirm);
}
function saveQuestions(){
	var number = document.getElementById("optionsNumber").value;
	var possibleAns = [];
	var correctAns = [];
	for(var i=0; i<number; i++){
		possibleAns.push(document.getElementById("box_" + i).value);
		if(document.getElementById("inputType_" + i).checked){
			correctAns.push(i);
		}
	}
	var qnText = document.getElementById("qnTextBox").value;
	var type = document.getElementById("qnTypeSelect").value;
	var newQn = new Question(qnText, possibleAns, correctAns, type);
	qnArray.push(newQn);
	localStorage.setItem("qnArray", JSON.stringify(qnArray));
	document.getElementById("qn_input").innerHTML = "Added";
	document.getElementById("qnTextBox").value = "";
	document.getElementById("optionsNumber").value = "";
}