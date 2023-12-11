$(".target").on("click", function () {
        let $button = $(this);
        let oldVal = parseInt($button.parent().find("input").val());
        let newVal = 0;

        if ($button.text() == '+') {
            newVal = oldVal + 1;
        }
        else {
            if (oldVal > 0) {
                newVal = oldVal - 1;
            }
            else {
                newVal = 0;
            }
        }

        $button.parent().find("input").val(newVal);
    });
