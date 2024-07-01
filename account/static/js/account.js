// Set a timeout to redirect the user to the other page after 10 seconds
    
$(document).ready(function() {
    // Set the initial timer value
    var timerValue = 7;
    $('#timer').html(timerValue);
    
    // Start a timer that updates the timer every second
    setInterval(function() {
        // Update the timer value
        timerValue--;

        // Display the timer value
        $('#timer').html(timerValue);

        // If the timer value reaches 0, stop the timer
        if (timerValue === 0) {
            window.location.href = '/shop/';
        }
    }, 1000);
});