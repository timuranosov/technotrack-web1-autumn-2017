$(document).ready(

    function() {

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", $('meta[name=csrf]').attr("content"));
                }
            }
        });

        $('select').chosen();

        $(document).on('click', '.postLikeLink', function(e) {
            e.preventDefault();
            var link = $(this);
            $.ajax({url: link.attr('href'), method: 'post'}).done(function(data, state, response) {
                if (state == 'success') {
                    link.text(data);
                }
            });
        });

    }
);