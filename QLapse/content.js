//content.js
//TODO
// 1. Collapse answers from answer page
// 2. Collapse answers from topics

$(document).ready(function(){
var answers = [];
var answerlen = answers.length;

function poll(){
  answers = $(".feed_type_answer");
  for(var i = answerlen; i<answers.length;i++){
     answers[i].addEventListener("dblclick", hey);
  }
  answerlen = answers.length;
}

function hey(){
  //Collapses the answer
  var wah = jQuery(this).find(".Expandable.SimpleToggle.Toggle.AnswerInFeedExpandable.AnswerExpandable");
  $("#" + wah[0].id).removeClass("hidden");
  $("#" + wah[1].id).addClass("hidden");
  //var morebut = jQuery(this).find(".more_link")[0];
  this.addEventListener("click", function(){morel(wah)});
}
function morel(block){
  //expands collapsed answer
  $("#" + block[0].id).addClass("hidden");
  $("#" + block[1].id).removeClass("hidden");
}
  
var answerPolls = setInterval(poll, 2000);
});


