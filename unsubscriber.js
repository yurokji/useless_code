function youtubeUnsubscriber() {
    var count = document.querySelectorAll("ytd-channel-renderer:not(.ytd-item-section-renderer)").length;
    var randomDelay = 2000;
    if(count == 0) return false;

    function unsubscribeVisible(randomDelay) {

        if (count == 0) {
            window.scrollTo(0,document.body.scrollHeight);
            setTimeout(function() {
                youtubeUnsubscriber();
            }, 10000)
        }

        unsubscribeButton = document.querySelector('.ytd-subscribe-button-renderer');
        unsubscribeButton.click();

        setTimeout(function () {
            document.getElementById("confirm-button").click()
            count--;
            console.log("Remaining: ", count);

            setTimeout(function () {
                unsubscribedElement = document.querySelector("ytd-channel-renderer");
                unsubscribedElement.parentNode.removeChild(unsubscribedElement);
                unsubscribeVisible(randomDelay)
            }, randomDelay);
        }, randomDelay);
    }

    unsubscribeVisible(randomDelay);
}

youtubeUnsubscriber();
