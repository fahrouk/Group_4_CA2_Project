$(".target").on("click", function () {
        let $button = $(this);
        let oldVal = parseInt($button.parent().find("input").val());
        let newVal = 0;

        if ($button.text() == '+') {
            newVal = oldVal + 1;
        }
