function startCount() {
	var notice = document.getElementById('ai');
	var myWriteFirebase = new Firebase("https://rpsuh16.firebaseio.com/games");

    count = 300;
    if (counter) {
    	clearInterval(counter);
    }
	var counter = setInterval(timer, 10); //10 will  run it every 100th of a secon
    function timer()
    {
    	count--;
        if (count < 0) {
				notice.innerHTML = "Shoot!"
				clearInterval(counter);
				clearInterval(timer);
				return;
			}
		else {
       		if (count > 200) {
       			notice.innerHTML = "Rock...";
       		}
       		else if (count > 100) {
       			notice.innerHTML = "Paper..."
       		}
       		else if (count == 55) {
   				time = (new Date).getTime();
			    myWriteFirebase.child(firebaseID).update({id : time});
			    console.log("Updated ID to " + time);
       		}
       		else {
       			notice.innerHTML = "Scissors..."
       		}
       }
     }
}